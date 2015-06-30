#!/usr/bin/python2
import sys, os

def run(cmd):
    return os.system('bash -c "%s"' % cmd) == 0

if __name__ == '__main__':
    curdir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.abspath(os.path.join(curdir, ".."))

    WORKING_DIR = sys.argv[1]

    run("python %s/ubuntu-1404-minimal/create.py %s" % (path, WORKING_DIR)) or exit(1)
    run("cat %s/ubuntu-1404-minimal.tar.xz | docker import - ubuntu-1404-minimal" % WORKING_DIR) or exit(1)

    run("docker build -t vivado-2015_1 %s/vivado-2015_1/" % path) or exit(1)
    print "build completed"

    print "saving to %s/docker_containers.tar.xz" % WORKING_DIR
    run("docker save ubuntu-1404-minimal vivado-2015_1 | xz > %s/docker_containers.tar.xz" % WORKING_DIR)
