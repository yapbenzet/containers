FROM ubuntu:14.04

RUN \
	dpkg --add-architecture i386; \
	apt-get update ; \
	\
	apt-get -y install mesa-utils ; \
	apt-get -y install libgl1-mesa-glx:i386 libopenal1:i386 ; \
	apt-get -y install pulseaudio ; \
	\
	echo "deb http://deb.playonlinux.com/ trusty main" > /etc/apt/sources.list.d/playonlinux.list ; \
	apt-get update ; \
	apt-get -y --force-yes install gettext libfreetype6:i386 playonlinux ; \
	\
	echo "deb http://repo.steampowered.com/steam/ precise steam" > /etc/apt/sources.list.d/steam_tmp.list ; \
	apt-get update ; \
	apt-get -y --force-yes install --no-install-suggests steam ; \
	rm -f /etc/apt/sources.list.d/steam_tmp.list ; \
	\
	apt-get clean ; \
	find /var -name "*-old" -exec rm -f {} \; ; \
	rm -rf /var/lib/apt/lists/* /var/cache/apt/* ;

RUN export uid=1001 gid=1001 ; \
	mkdir -p /home/sandbox ; \
	echo "sandbox:x:${uid}:${gid}:sandbox,,,:/home/sandbox:/bin/bash" >> /etc/passwd ; \
	echo "sandbox:x:${uid}:" >> /etc/group ; \
	chown ${uid}:${gid} -R /home/sandbox ; \
	usermod -a -G plugdev sandbox ; \
	usermod -a -G audio sandbox ; \
	usermod -a -G video sandbox ; \
	\
	ln -sf /bin/bash /bin/sh ;

USER sandbox
ENV HOME /home/sandbox
CMD bash

# dpkg --add-architecture i386; apt-get update ; \
# 	apt-get install -y --no-install-recommends --no-install-suggests libc6:i386 libstdc++6:i386 fontconfig:i386 libxtst6:i386 libxrender1:i386 libglib2.0-0:i386 libsm6:i386 libxi6:i386 ;


