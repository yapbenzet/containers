FROM vivado-ubuntu

USER root
ENV HOME /root

RUN apt-get update ; \
	apt-get install -y --no-install-recommends --no-install-suggests ssh sshfs git ; \
	echo "user_allow_other" >> /etc/fuse.conf ; \
	\
	apt-get clean ; \
	find /var -name "*-old" -exec rm -f {} \; ; \
	rm -rf /var/lib/apt/lists/* /var/log/* /var/cache/apt/* ; \
	rm -rf /var/cache/man ; \
	rm -rf /usr/share/locales ;

USER sandbox
ENV HOME /home/sandbox
CMD bash
