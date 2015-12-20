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

HOME_DIR=${WORKING_DIR}/home
clean() {
	rm -rf ${WORKING_DIR}/tmp/*
	if [ "$TMP_HOME_SIZE" != "" ]; then
		sudo /taner/scripts/tmpfs_compressed.py umount $HOME_DIR
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
		/taner/scripts/tmpfs_compressed.py mount $HOME_DIR $TMP_HOME_SIZE || exit
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

start() {
	create_tmp_dir
	create_home_dir
	display_config
	audio_config

	[ "$PARAM_PORTS" == "" ] || echo "[PORTS] $PARAM_PORTS"
	[ "$PARAM_DEVICES" == "" ] || echo "[DEVICES] $PARAM_DEVICES"
	[ "$PARAM_X_DISPLAY" == "" ] || echo "[DISPLAY] enabled"
	[ "$PARAM_AUDIO" == "" ] || echo "[AUDIO] enabled"
	[ "$PARAM_OTHER" == "" ] || echo "[PARAMETERS] $PARAM_OTHER"

	if [ -f "${SOURCE_FILE}.startup" ]; then
		sudo -u $PARAM_USER HOME_DIR=$HOME_DIR -- bash ${SOURCE_FILE}.startup
	fi

	docker run --rm \
		   --read-only=$PARAM_RO \
		   -u $PARAM_USER \
		   -v ${WORKING_DIR}/tmp:/tmp \
		   -v $HOME_DIR:/home/$PARAM_USER \
		   $PARAM_DEVICES \
		   $PARAM_PORTS \
		   $PARAM_X_DISPLAY \
		   $PARAM_AUDIO \
		   $PARAM_OTHER \
		   -it $CONTAINER \
		   bash
}

start
