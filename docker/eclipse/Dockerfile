FROM ubuntu:14.04

RUN apt-get update ; \
 	apt-get -y install --no-install-recommends --no-install-suggests eclipse openjdk-7-jdk; \
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
