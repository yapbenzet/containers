FROM vivado-ubuntu1404

USER root
ENV HOME /root

RUN apt-get update ; \
	apt-get install -y --no-install-recommends --no-install-suggests openssh-server ; \
	sed -i 's/UsePAM yes/UsePAM no/' /etc/ssh/sshd_config ; \
	echo "PasswordAuthentication no" >> /etc/ssh/sshd_config ; \
	\
	apt-get clean ; \
	find /var -name "*-old" -exec rm -f {} \; ; \
	rm -rf /var/lib/apt/lists/* /var/log/* /var/cache/apt/* ; \
	rm -rf /var/cache/man ; \
	rm -rf /usr/share/locales ; \
	\
	/etc/init.d/ssh start ; \
	\
	echo "if [ -f ~/.bashrc ]; then . ~/.bashrc fi" > /home/sandbox/.bash_profile ; \
	mkdir -p /home/sandbox/.ssh ; \
	chown ${uid}:${gid} -R /home/sandbox ; \
	cd /home/sandbox ;

CMD bash

#
# /home/sandbox/.bash_profile -> https://stackoverflow.com/questions/820517/bashrc-at-ssh-login
#
