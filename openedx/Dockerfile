FROM phusion/baseimage:0.9.17

ENV DEBIAN_FRONTEND noninteractive

RUN \
	apt-get -y update ; \
	apt-get install -y git ; \
	apt-get install -y python-dev python-setuptools python-apt gcc ; \
	easy_install pip ; \
	\
	git clone https://github.com/appsembler/configuration.git -b appsembler_docker/release /configuration ; \
	cd /configuration ; \
	pip install -r requirements.txt ; \
	\
	apt-get clean ; rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /var/log/* /var/cache/apt/* ;


# ignore my_init output stderr
RUN exec bash -c '( \
	\
	my_init &> /dev/null & MY_INIT_PID=$! ; \
	echo "[Dockerfile] my_init started, PID=$MY_INIT_PID" ; \
	\
	echo "[Dockerfile] install started" ; \
	cd /configuration/playbooks ; \
	ansible-playbook -vv -c local -i "127.0.0.1," docker_lite.yml || exit 1 ; \
	echo "[Dockerfile] install ok" ; \
	\
	echo "[Dockerfile] stoping edx services" ; \
	/edx/app/supervisor/venvs/supervisor/bin/supervisorctl stop all ; \
	\
	echo "[Dockerfile] cleaning" ; \
	apt-get clean ; rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /var/log/* /var/cache/apt/* ; \
	\
	echo "[Dockerfile] kill all processes" ; \
	killall5 -9 ; \
	echo "[Dockerfile] exiting (exec pkill -U root)" ; \
	exec pkill -U root ; \
)'

CMD my_init
