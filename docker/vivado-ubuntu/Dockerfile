FROM ubuntu:14.04

RUN apt-get update ; \
	apt-get install -y --no-install-recommends --no-install-suggests libgtk2.0-0 libxtst6 ; \
	apt-get install -y --no-install-recommends --no-install-suggests make gcc libc-dev ; \
	\
	dpkg --add-architecture i386; apt-get update ; \
	apt-get install -y --no-install-recommends --no-install-suggests libc6:i386 libstdc++6:i386 fontconfig:i386 libxtst6:i386 libxrender1:i386 libglib2.0-0:i386 libsm6:i386 libxi6:i386 ; \
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
	chown ${uid}:${gid} -R /home/sandbox ; \
	usermod -a -G plugdev sandbox ; \
	\
	ln -sf /bin/bash /bin/sh ;

USER sandbox
ENV HOME /home/sandbox
CMD bash

# libxi6:i386 -> installer icin gerekli
# *:i386 -> docnav icin gerekli
# gcc, libc-dev -> simulation
