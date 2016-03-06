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
	\
	DEBIAN_FRONTEND=noninteractive apt-get install -y bind9 ; \
	\
	apt-get clean ; \
	find /var -name "*-old" -exec rm -f {} \; ; \
	rm -rf /var/lib/apt/lists/* /var/log/* /var/cache/apt/* ; \
	rm -rf /var/cache/man ; \
	rm -rf /usr/share/locales ;
