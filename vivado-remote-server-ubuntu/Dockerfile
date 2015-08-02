FROM vivado-ubuntu

USER root
ENV HOME /root

RUN apt-get update ; \
	apt-get install -y --no-install-recommends --no-install-suggests openssh-server git ; \
	sed -i 's/UsePAM yes/UsePAM no/' /etc/ssh/sshd_config ; \
	echo "PasswordAuthentication no" >> /etc/ssh/sshd_config ; \
	\
	apt-get clean ; \
	find /var -name "*-old" -exec rm -f {} \; ; \
	rm -rf /var/lib/apt/lists/* /var/log/* /var/cache/apt/* ; \
	rm -rf /var/cache/man ; \
	rm -rf /usr/share/locales ; \
	\
	mkdir /var/run/sshd ;

CMD /usr/sbin/sshd -D
