FROM centos:7

RUN \
	yum -y install sudo ; \
	\
	yum -y groupinstall "X Window System" ; \
	yum -y groupinstall "Fonts" ; \
	yum -y install gnome-classic-session ; \
	\
	yum -y install mesa-libGLU ; \
	\
	yum -y groupinstall development ; \
	yum -y install zlib-dev openssl-devel sqlite-devel bzip2-devel wget ; \
	\
	cd /tmp/ ; \
	wget http://www.python.org/ftp/python/3.4.3/Python-3.4.3.tar.xz ; \
	tar xf Python-3.4.3.tar.xz ; \
	cd Python-3.4.3 ; \
	./configure --prefix=/usr/local ; \
	make -j4 ; \
	make altinstall ; \
	ln -s /usr/local/bin/python3.4 /usr/local/bin/python3 ; \
	\
	yum -y install ncurses-devel ; \
	pip3.4 install readline ; \
	\
	yum -y install strace ; \
	\
	yum -y install libstdc++ libstdc++.i686 ; \
	yum -y install bc ; \
	\
	yum -y clean all ; \
	rm -rf /tmp/* ; \
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


# ncurses-devel ->python-readline
# pyton-readline, strace -> reconos development kit
# mesa-libGLU -> xps guide ikon cikmama problemi


#------------------------------

# eklenmesi gereken
# 	yum remove $(rpm -qa "*-devel") ;


# kurulabilecek diger paketler
# 	yum -y swap -- remove systemd-container systemd-container-libs -- install systemd systemd-libs ; \
#	yum -y groupinstall "Base" ; \

# java-1.7.0-openjdk -> ?????

