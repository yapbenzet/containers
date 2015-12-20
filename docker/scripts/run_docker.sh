#!/bin/bash

source default.conf
source $1

error() {
	echo $1
	exit 1
}

[ "$(id -u)" == "0" ] || error "run as root"
[ -d "${WORKING_DIR}" ] || error "working directory not found"
[ "${CONTAINER}" != "" ] || error "CONTAINER variable empty"

clean() {
	rm -rf ${WORKING_DIR}/tmp/*
	umountlist $WORKING_DIR | sh
	echo "clean()"
}
trap clean EXIT

if [ "$PARAM_USER" == "" ]; then
	PARAM_USER=$SANDBOX_USER
fi

if [ "$PARAM_RO" == "" ]; then
	PARAM_RO=true
fi

HOME=${WORKING_DIR}/home

mkdir -p $HOME || exit
# cp -u files/vivado_docker/bashrc $HOME/.bashrc
chown -R $PARAM_USER $HOME

## /tmp ##
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
## ##

if [ "$PARAM_X_DISPLAY" != "" ]; then
	sudo -u $HOST_USER xhost +SI:localuser:$PARAM_USER
fi

docker run --rm \
	   --read-only=$PARAM_RO \
	   -u $PARAM_USER \
	   -v ${WORKING_DIR}/tmp:/tmp \
	   -v $HOME:/home/$PARAM_USER \
	   $PARAM_DEVICES \
	   $PARAM_PORTS \
	   $PARAM_X_DISPLAY \
	   $PARAM_OTHER \
	   -it $CONTAINER \
	   bash
