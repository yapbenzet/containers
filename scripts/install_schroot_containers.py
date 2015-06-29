#!/usr/bin/python2
import sys, os

def run(cmd):
    return os.system('bash -c "%s"' % cmd) == 0

if __name__ == '__main__':
    print "NOT TESTED!"
    exit(1)

    if len(sys.argv) != 2:
        print "wrong parameter"
        exit(1)

    WORKING_DIR = sys.argv[1]

    curdir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.abspath(os.path.join(curdir, ".."))

    run("python ubuntu-1404-minimal/create.py %s" % WORKING_DIR) or exit(1)

    run("python create_chroot_from_docker.py %(tar)s %(docker)s %(wd)s %(name)s" % (
        "tar": "%s/ubuntu-1404-minimal.schroot.tar.xz" % WORKING_DIR,
        "docker" : "%s/vivado-2015_1/Docker" % path,
        "wd" : WORKING_DIR,
        "name" : "vivado-2015_1"
    ))
