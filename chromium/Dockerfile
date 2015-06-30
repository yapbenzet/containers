FROM ubuntu-1404-minimal

RUN echo "deb http://us.archive.ubuntu.com/ubuntu/ trusty universe" > /etc/apt/sources.list.d/universe.list ; \
	echo "deb http://us.archive.ubuntu.com/ubuntu/ trusty-updates universe" >> /etc/apt/sources.list.d/universe.list ; \
	echo "deb http://us.archive.ubuntu.com/ubuntu/ trusty multiverse" > /etc/apt/sources.list.d/multiverse.list ; \
	echo "deb http://us.archive.ubuntu.com/ubuntu/ trusty-updates multiverse" >> /etc/apt/sources.list.d/multiverse.list ; \
	apt-get update ; \
	apt-get -y install --no-install-recommends --no-install-suggests chromium-browser ; \
	apt-get -y install pepperflashplugin-nonfree ; \
	update-pepperflashplugin-nonfree --install ; \
	rm -rf /var/cache/pepperflashplugin-nonfree ; \
	\
	apt-get -y install --no-install-recommends --no-install-suggests pulseaudio ; \
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
