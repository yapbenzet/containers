FROM ubuntu-1404-minimal

RUN apt-get update; \
	apt-get -y dist-upgrade ; \
	SUDO_FORCE_REMOVE=yes apt-get -y autoremove --purge sudo ; \
	apt-get -y autoremove --purge dh-python python3.4 python3.4-minimal xkb-data netcat-openbsd \
	    net-tools keyboard-configuration vim-common isc-dhcp-common less locales perl mime-support eject ; \
	\
	apt-get clean ; \
	find /var -name "*-old" -exec rm -f {} \; ; \
	rm -rf /var/lib/apt/lists/* /var/log/* /var/cache/apt/* ; \
	rm -rf /var/cache/man ; \
	rm -rf /usr/share/locales ;
