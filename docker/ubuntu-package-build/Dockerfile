FROM ubuntu:14.04

RUN \
	echo "deb ftp://cz.archive.ubuntu.com/pub/ubuntu/ trusty main restricted universe multiverse" > /etc/apt/sources.list ; \
	echo "deb-src ftp://cz.archive.ubuntu.com/pub/ubuntu/ trusty main restricted universe multiverse" >> /etc/apt/sources.list ; \
	echo "deb ftp://cz.archive.ubuntu.com/pub/ubuntu/ trusty-security main restricted universe multiverse" >> /etc/apt/sources.list ; \
	echo "deb-src ftp://cz.archive.ubuntu.com/pub/ubuntu/ trusty-security main restricted universe multiverse" >> /etc/apt/sources.list ; \
	echo "deb ftp://cz.archive.ubuntu.com/pub/ubuntu/ trusty-updates main restricted universe multiverse" >> /etc/apt/sources.list ; \
	echo "deb-src ftp://cz.archive.ubuntu.com/pub/ubuntu/ trusty-updates main restricted universe multiverse" >> /etc/apt/sources.list ; \
	echo "deb ftp://cz.archive.ubuntu.com/pub/ubuntu/ trusty-backports main restricted universe multiverse" >> /etc/apt/sources.list ; \
	echo "deb-src ftp://cz.archive.ubuntu.com/pub/ubuntu/ trusty-backports main restricted universe multiverse" >> /etc/apt/sources.list ; \
	\
	apt-get update ; \
	apt-get -y autoremove vim-common ; \
	apt-get -y install nano ; \
	apt-get -y install devscripts dh-make build-essential ; \
	\
	apt-get clean ; \
	find /var -name "*-old" -exec rm -f {} \; ; \
	rm -rf /var/lib/apt/lists/* /var/log/* /var/cache/apt/* ; \
	rm -rf /var/cache/man ; \
	rm -rf /usr/share/locales ; \
	\
	export uid=1001 gid=1001 ; \
	mkdir -p /home/sandbox ; \
	echo "sandbox:x:${uid}:${gid}:sandbox,,,:/home/sandbox:/bin/bash" >> /etc/passwd ; \
	echo "sandbox:x:${uid}:" >> /etc/group ; \
	chown ${uid}:${gid} -R /home/sandbox ;

USER sandbox
ENV HOME /home/sandbox
CMD bash
