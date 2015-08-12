FROM phusion/baseimage:0.9.17

# ignores my_init stderr


RUN exec bash -c '( \
	\
	my_init &> /dev/null & MY_INIT_PID=$! ; \
	echo "[Dockerfile] my_init started, PID=$MY_INIT_PID" ; \
	\
	echo "[Dockerfile] kill all processes" ; \
	killall5 -9 ; \
	echo "[Dockerfile] exiting (exec pkill -U root)" ; \
	exec pkill -U root ; \
)'

CMD my_init -- bash
