#!/usr/bin/python2
import sys, os, subprocess, glob

def run(cmd):
    return os.system(cmd) == 0

def run_chroot(d, cmd):
    cmd = "chroot %s %s" % (d, cmd)
    return os.system(cmd) == 0

remove_packages = [
    "dh-python", "python3.4", "python3.4-minimal", "xkb-data", "netcat-openbsd",
    "net-tools", "keyboard-configuration", "vim-common", "isc-dhcp-common",
    "less", "locales", "perl", "mime-support", "eject"
]

if __name__ == '__main__':

    if len(sys.argv) != 2:
        print "wrong parameter"
        exit(1)

    WORKING_DIR = sys.argv[1]
    CHROOT_NAME = os.path.basename(os.path.dirname(os.path.abspath(__file__)))

    CHROOT_DIR = "%s/%s" % (WORKING_DIR, CHROOT_NAME)
    runch = lambda x : run_chroot(CHROOT_DIR, x)

    run("debootstrap trusty %s http://archive.ubuntu.com/ubuntu/" % CHROOT_DIR)

    runch("apt-get update") or exit(1)
    runch('bash -c "SUDO_FORCE_REMOVE=yes apt-get -y autoremove --purge sudo"')
    runch("apt-get -y autoremove --purge %s" % (" ".join(remove_packages)))
    runch("apt-get clean")
    runch("find /var -name \"*-old\" -exec rm -f {} \;")
    runch("rm -rf /var/lib/apt/lists/* /var/log/* /var/cache/apt/*")
    runch("rm -rf /var/cache/man")
    runch("rm -rf /usr/share/locales")
    runch("rm -rf /dev/*")

    print "tar started"
    run("tar -C %s -cJp . > %s/%s.chroot.tar.xz" % (CHROOT_DIR, WORKING_DIR, CHROOT_NAME)) or exit(1)
    run("rm -rf %s" % CHROOT_DIR) or exit(1)
