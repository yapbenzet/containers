#!/bin/bash

source default.conf
SOURCE_FILE=$1
source $SOURCE_FILE

error() {
	echo $1
	exit 1
}

[ "$(id -u)" == "0" ] || error "run as root"
[ -d "${WORKING_DIR}" ] || error "working directory not found"
[ "${CONTAINER}" != "" ] || error "CONTAINER variable empty"

[ "$(realpath ${WORKING_DIR})" != "/" ] || error "working directory is /"

HOME_DIR=${WORKING_DIR}/home
clean() {
	docker kill "${CONTAINER}_$$" &> /dev/null
	docker rm "${CONTAINER}_$$" &> /dev/null
	rm -rf ${WORKING_DIR}/tmp/*
	if [ "$TMP_HOME_SIZE" != "" ]; then
		tmpfs_compressed.py umount $HOME_DIR
	fi

	umountlist $WORKING_DIR | sh

	if [ "$ENABLE_AUDIO" == "true" ]; then
		sudo -u $HOST_USER -- bash -c "\
			export XDG_RUNTIME_DIR=/run/user/\`id -u\` && \
			pulseaudio --kill && \
			pulseaudio --start "
	fi
	echo "clean()"
}
trap clean EXIT

if [ "$PARAM_USER" == "" ]; then
	PARAM_USER=$SANDBOX_USER
fi

if [ "$PARAM_RO" == "" ]; then
	PARAM_RO=true
fi

create_tmp_dir() {
	rm -rf ${WORKING_DIR}/tmp
	mkdir -p ${WORKING_DIR}/tmp
	if [ "$TMP_SIZE" == "0" ]; then
		chown root:root ${WORKING_DIR}/tmp
		chmod 777 ${WORKING_DIR}/tmp
	elif [ "$TMP_SIZE" == "" ]; then
		mount -t tmpfs tmpfs -o size=256M ${WORKING_DIR}/tmp
	else
		mount -t tmpfs tmpfs -o size=$TMP_SIZE ${WORKING_DIR}/tmp
	fi
}

create_home_dir() {
	mkdir -p $HOME_DIR || exit
	if [ "$TMP_HOME_SIZE" != "" ]; then
		tmpfs_compressed.py mount $HOME_DIR $TMP_HOME_SIZE || exit
	fi
	chown -R $PARAM_USER $HOME_DIR
}

display_config() {
	if [ "$ENABLE_DISPLAY" == "true" ]; then
		PARAM_X_DISPLAY="-v /tmp/.X11-unix:/tmp/.X11-unix -e DISPLAY=:0"
	fi
	if [ "$PARAM_X_DISPLAY" != "" ]; then
		sudo -u $HOST_USER xhost +SI:localuser:$PARAM_USER
	fi
}

audio_config() {
	if [ "$ENABLE_AUDIO" == "true" ]; then
		cp /home/$HOST_USER/.config/pulse/cookie $HOME_DIR/pulse_cookie
		sudo chown $PARAM_USER:$PARAM_USER $HOME_DIR/pulse_cookie
		sudo -u $HOST_USER -- bash -c "\
			export XDG_RUNTIME_DIR=/run/user/\`id -u\` && \
			pulseaudio --kill && \
			pulseaudio --start --load=\"module-native-protocol-tcp auth-ip-acl=127.0.0.1;172.17.42.0/24\" "
		PARAM_AUDIO="\
		-e PULSE_SERVER=tcp:172.17.42.1:4713 \
		-e PULSE_COOKIE=/home/$PARAM_USER/pulse_cookie "
	fi
}

mount_config() {

	PARAM_MOUNTS=""
	if [ "MOUNT_LIST" != "" ]; then
		for mnt in "${MOUNT_LIST[@]}"; do
			IFS=';' read -ra MNT <<< "$mnt"
			mount_dir=${WORKING_DIR}/${MNT[1]}
			mount_parameters=${MNT[2]}
			mount_device=${MNT[0]}

			echo "mounting ${MNT[1]} ( $mount_device )"

			mkdir -p $mount_dir
			mount -o $mount_parameters $mount_device ${WORKING_DIR}/${MNT[1]}
			PARAM_MOUNTS="$PARAM_MOUNTS -v $mount_dir:${MNT[1]}"
		done
	fi

}

get_usb_device_path() {
	vendor_product=$1
	device_list=`lsusb -d $vendor_product`
	[ "$device_list" != "" ] || error "usb device $vendor_product not found"
	[ "$(wc -l <<< $device_list)" == "1" ] || error "usb device $vendor_product count != 1"
	bus=$(cut -d ' ' -f 2 <<< $device_list)
	devnum=$(cut -d ' ' -f 4 <<< $device_list)
	echo "/dev/bus/usb/$bus/${devnum::-1}"
	exit 0
}

devices_config() {
	for DEVICE_ID in "${ADD_DEVICE_WITH_VENDOR_PRODUCT_ID[@]}"; do
		device=$(get_usb_device_path ${DEVICE_ID})
		if [ "$?" == "0" ]; then
			PARAM_DEVICES="${PARAM_DEVICES} --device=$device"
		else
			echo "[WARNING] ${DEVICE_ID} device not found"
		fi
	done
}

start() {
	create_tmp_dir
	create_home_dir
	mount_config
	display_config
	audio_config
	devices_config

	[ "$PARAM_PORTS" == "" ] || echo "[PORTS] $PARAM_PORTS"
	[ "$PARAM_DEVICES" == "" ] || echo "[DEVICES] $PARAM_DEVICES"
	[ "$PARAM_X_DISPLAY" == "" ] || echo "[DISPLAY] enabled"
	[ "$PARAM_AUDIO" == "" ] || echo "[AUDIO] enabled"
	[ "$PARAM_OTHER" == "" ] || echo "[PARAMETERS] $PARAM_OTHER"

	if [ -f "${SOURCE_FILE}.startup" ]; then
		sudo -u $PARAM_USER HOME_DIR=$HOME_DIR -- bash ${SOURCE_FILE}.startup
	fi

	docker run --rm --name="${CONTAINER}_$$" \
		   --read-only=$PARAM_RO \
		   -u $PARAM_USER \
		   -v ${WORKING_DIR}/tmp:/tmp \
		   -v $HOME_DIR:/home/$PARAM_USER \
		   $PARAM_DEVICES \
		   $PARAM_PORTS \
		   $PARAM_X_DISPLAY \
		   $PARAM_AUDIO \
		   $PARAM_OTHER \
		   $PARAM_MOUNTS \
		   -it $CONTAINER \
		   bash
}

start
