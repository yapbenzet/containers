## https://forum.unity3d.com/threads/unity-on-linux-release-notes-and-known-issues.350256/#post-2429209

FROM ubuntu:14.04

WORKDIR unity3d
ADD unity-editor-5.3.5f1+20160525_amd64.deb unity3d.deb

RUN apt-get update; \
	dpkg -i unity3d.deb || apt-get -f install -y ; \
	dpkg -i unity3d.deb ; \
	apt-get clean ; \
	rm unity3d.deb ; \
	\
	mkdir -p /usr/share/icons/hicolor && \
	apt-get update && apt-get install -y \
	ca-certificates \
	fonts-liberation \
	gconf-service \
	hicolor-icon-theme \
	libappindicator1 \
	libasound2 \
	libcanberra-gtk-module \
	libcurl3 \
 	libdrm-intel1 libdrm-nouveau2 libdrm-radeon1 \
	libexif-dev \
	libgconf-2-4 \
	libgl1-mesa-dri \
	libgl1-mesa-glx \
	libnspr4 \
	libnss3 \
	libpango1.0-0 \
	libv4l-0 \
	libxcb1 \
	libxcb-render0 \
	libxcb-shm0 \
	libxss1 \
	libxtst6 \
	mono-complete \
	monodevelop \
	wget \
	xdg-utils \
	--no-install-recommends ; \
	\
	apt-get clean ; \
	find /var -name "*-old" -exec rm -f {} \; ; \
	rm -rf /var/lib/apt/lists/* /var/log/* /var/cache/apt/* ; \
	rm -rf /var/cache/man ; \
	rm -rf /usr/share/locales ;

## sandbox user ##
RUN \
	export uid=1001 gid=1001 ; \
	mkdir -p /home/sandbox ; \
	echo "sandbox:x:${uid}:${gid}:sandbox,,,:/home/sandbox:/bin/bash" >> /etc/passwd ; \
	echo "sandbox:x:${uid}:" >> /etc/group ; \
	chown ${uid}:${gid} -R /home/sandbox ; \
	usermod -a -G plugdev sandbox ; \
	usermod -a -G video sandbox ;

## chrome ##
ADD google-chrome-stable_current_amd64.deb /tmp/google-chrome.deb

RUN \
	dpkg -i /tmp/google-chrome.deb ; \
	rm -f /tmp/google-chrome.deb ; \
	apt-get clean ; \
	find /var -name "*-old" -exec rm -f {} \; ; \
	rm -rf /var/lib/apt/lists/* /var/log/* /var/cache/apt/* ; \
	rm -rf /var/cache/man ; \
	rm -rf /usr/share/locales ;

## android studio ##
RUN \
	apt-get update ; \
	apt-get -y install --no-install-recommends --no-install-suggests lib32z1 lib32ncurses5 lib32bz2-1.0 g++-multilib ; \
	apt-get -y install --no-install-recommends --no-install-suggests openjdk-7-jdk  ; \
	\
	apt-get -y install --no-install-recommends --no-install-suggests libgl1-mesa-dri kvm  ; \
	groupdel kvm ; \
	groupadd -g 122 kvm ; \
	\
	usermod -a -G kvm sandbox ; \
	\
	apt-get clean ; \
	find /var -name "*-old" -exec rm -f {} \; ; \
	rm -rf /var/lib/apt/lists/* /var/log/* /var/cache/apt/* ; \
	rm -rf /var/cache/man ; \
	rm -rf /usr/share/locales ;



USER sandbox
ENV HOME /home/sandbox
WORKDIR /home/sandbox
CMD bash
