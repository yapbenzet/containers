#!/bin/bash
FS_IMAGE=$1

export KVM_MEMORY=256
export KVM_KERNEL_PARAMETERS="rootflags=compress-force=zlib console=ttyS0"

REDIRECT="\
	-redir tcp:111::111 \
	-redir tcp:2049::2049 \
	-redir tcp:4002::4002 \
	-redir udp:111::111 \
	-redir udp:2049::2049 \
	-redir udp:4002::4002 \
"

export KVM_PARAMETERS=" \
	-nographic \
	$REDIRECT \
"

KVM_COPY_FILES=(
	files/entry_point.sh:/entry_point.sh
)
export EVAL_KVM_COPY_FILES=$(declare -p KVM_COPY_FILES)

kvm_fsimg.sh $FS_IMAGE
