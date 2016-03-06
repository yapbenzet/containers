FROM centos:7

RUN \
	yum -y install libX11 libXext libXrender libXtst ; \
	yum -y install gtk2 xorg-x11-fonts-* ; \
	yum -y install gcc ; \
	\
	yum clean all ; \
	\
	export uid=1001 gid=1001 ; \
	mkdir -p /home/sandbox ; \
	echo "sandbox:x:${uid}:${gid}:sandbox,,,:/home/sandbox:/bin/bash" >> /etc/passwd ; \
	echo "sandbox:x:${uid}:" >> /etc/group ; \
	chown ${uid}:${gid} -R /home/sandbox ; \
	\
	echo plugdev:x:46 >> /etc/group ; \
	usermod -a -G plugdev sandbox ;

USER sandbox
ENV HOME /home/sandbox
CMD bash
