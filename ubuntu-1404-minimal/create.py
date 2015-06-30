#!/usr/bin/python2
import sys, os, subprocess, glob

def run(cmd):
    return os.system('bash -c "%s"' % cmd) == 0

APT_SOURCES = """
deb http://archive.ubuntu.com/ubuntu/ trusty main restricted
deb http://archive.ubuntu.com/ubuntu/ trusty-updates main restricted
deb http://archive.ubuntu.com/ubuntu/ trusty-security main restricted
"""

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print "wrong parameter"
        exit(1)

    WORKING_DIR = sys.argv[1]

    SOURCE_DIR = os.path.dirname(os.path.abspath(__file__))
    CHROOT_NAME = os.path.basename(SOURCE_DIR)
    CHROOT_DIR = "%s/%s" % (WORKING_DIR, CHROOT_NAME)

    run("debootstrap trusty %s http://archive.ubuntu.com/ubuntu/" % CHROOT_DIR)
    run("rm -rf %s/dev/*" % CHROOT_DIR)
    run("chroot %s apt-get clean" % CHROOT_DIR)
    run("rm -rf %s/{var/lib/apt/lists/*,var/log/*,var/cache/apt/*}" % CHROOT_DIR)
    open("%s/etc/apt/sources.list" % CHROOT_DIR, "w").write(APT_SOURCES)

    print "tar started"
    debootstrap_output_tar = "%s/%s.chroot.tar.xz" % (WORKING_DIR, CHROOT_NAME)
    run("tar -C %s -cJp . > %s" % (CHROOT_DIR, debootstrap_output_tar)) or exit(1)
    run("rm -rf %s" % CHROOT_DIR) or exit(1)

    print "[docker] import %s as %s" % (debootstrap_output_tar, CHROOT_NAME)
    run("cat %s | docker import - %s" % (debootstrap_output_tar, CHROOT_NAME)) or exit(1)

    print "rm %s" % debootstrap_output_tar
    run("rm -f %s" % debootstrap_output_tar)

    print "[docker] build %s:update" % CHROOT_NAME
    run("docker build -t %s:update %s" % (CHROOT_NAME, SOURCE_DIR))

    docker_output_tar = "%s/%s.tar.xz" % (WORKING_DIR, CHROOT_NAME)
    print "[docker] export %s:update to %s" % (CHROOT_NAME, docker_output_tar)
    run("docker run --name=tmp-%s %s:update bash" % (CHROOT_NAME, CHROOT_NAME))
    run("docker export tmp-%s | xz > %s" % (CHROOT_NAME, docker_output_tar))

    print "[docker] rm old %s" % CHROOT_NAME
    run("docker rm tmp-%s" % CHROOT_NAME)
    run("docker rmi %s:update" % CHROOT_NAME)
    run("docker rm %s" % CHROOT_NAME)
