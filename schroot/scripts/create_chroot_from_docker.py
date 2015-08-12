#!/usr/bin/python2
import sys, os

def run(cmd):
    return os.system('bash -c "%s"' % cmd) == 0

def run_chroot(d, cmd):
    cmd = 'chroot %s bash -c "%s"' % (d, cmd)
    return os.system(cmd) == 0

if __name__ == '__main__':

    if len(sys.argv) != 5:
        print "wrong parameter"
        exit(1)

    BASE_TAR, DOCKER_FILE, WORKING_DIR, CHROOT_NAME = sys.argv[1:5]
    CHROOT_DIR = "%s/%s" % (WORKING_DIR, CHROOT_NAME)
    runch = lambda x : run_chroot(CHROOT_DIR, x)

    print "extracting %s -> %s" % (BASE_TAR, CHROOT_DIR)
    run("mkdir -p %s" % CHROOT_DIR)
    run("tar xfp %s -C %s" % (BASE_TAR, CHROOT_DIR)) or exit(1)

    f = open(DOCKER_FILE).read().replace('\\\n', '')
    i = 0
    for line in f.split('\n'):
        if line.startswith("RUN "):
            line = line[len("RUN "):]
            i += 1
            print "run", i
            runch(line) or exit(1)

    print "tar started"
    run("tar -C %s -cJp . > %s/%s.chroot.tar.xz" % (CHROOT_DIR, WORKING_DIR, CHROOT_NAME)) or exit(1)
    run("rm -rf %s" % CHROOT_DIR) or exit(1)
