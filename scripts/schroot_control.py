#!/usr/bin/python2
import sys, os, subprocess, glob

def run(cmd, stdin=None):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return p.communicate()

def run_exec(cmd):
    args = cmd.split()
    os.execvp(args[0], args)

def get_sessions():
    sessions, _ = run("schroot --all-sessions --list")
    return sessions.split('\n')

def find_sessions(name):
    l = []
    for session in get_sessions():
        if session.startswith("session:%s" % name):
            l.append(session)
    return l

def cmd_new(user, module_dir):
    module_dir = os.path.abspath(module_dir)
    module_name = os.path.split(module_dir)[-1]
    if module_name == "schroot":
        # [path]/[module_name]/schroot/schroot.conf seklinde isimlendirildiyse
        module_name = os.path.basename(os.path.split(module_dir)[-2])

    run("rm -f /etc/schroot/chroot.d/%s.conf" % module_name)
    with open("/etc/schroot/chroot.d/%s.conf" % module_name, "w") as f:
        f.write("[%s]\n" % module_name)
        f.write("profile=tnr/%s\n" % module_name)
        f.write("type=directory\n")
        f.write("directory=/tmp\n")
        f.write(open("%s/schroot.conf" % module_dir).read())

    run("rm -rf /etc/schroot/tnr/%s" % module_name)
    run("mkdir -p /etc/schroot/tnr/%s" % module_name)
    run("cp %s/profile/nssdatabases /etc/schroot/tnr/%s/" % (module_dir, module_name))

    with open("/etc/schroot/tnr/%s/copyfiles" % module_name, "w") as f:
        copyfiles = open("%s/profile/copyfiles" % module_dir).read()
        copyfiles = copyfiles % { "DIR" : module_dir }
        f.write(copyfiles)

    with open("/etc/schroot/tnr/%s/fstab" % module_name, "w") as f:
        fstab = open("%s/profile/fstab" % module_dir).read()
        fstab = fstab % { "DIR" : module_dir }
        f.write(fstab)

    session_name, _ = run("sudo -u %s schroot --begin-session -c %s" % (user, module_name))
    if session_name:
        print "schroot session started: %s" % session_name


def cmd_lsusb(name):
    out, err = run("lsusb")
    device_list = {}
    schroot = "/var/lib/schroot/mount/%s" % name[len("session:"):]
    for line in out.split('\n'):
        if line:
            addr, name = line.split(": ")
            _, bus, _, dev = addr.split()
            device_list["%s%s" % (bus, dev)] = name

    l = glob.glob("%s/dev/bus/usb/*/*" % schroot)
    print "USB devices:"
    for f in l:
        bus, dev = f.split("/")[-2:]
        name = device_list.get(bus+dev, "")
        if not name.endswith("hub"):
            print bus+"/"+dev, name
    print
    print "USB hubs:"
    for f in l:
        bus, dev = f.split("/")[-2:]
        name = device_list.get(bus+dev, "")
        if name.endswith("hub"):
            print bus+"/"+dev, name

def cmd_usb_mount(name, dev):
    schroot = "/var/lib/schroot/mount/%s" % name[len("session:"):]
    bus, dev = dev.split("/")
    dev_path = "/dev/bus/usb/%s/%s" % (bus, dev)

    run("mkdir -p %s/dev/bus/usb/%s" % (schroot, bus))
    run("touch %s/%s" % (schroot, dev_path))
    run("mount --bind %s %s/%s" % (dev_path, schroot, dev_path))

def cmd_usb_umount(name, dev):
    schroot = "/var/lib/schroot/mount/%s" % name[len("session:"):]
    if dev == "all":
        print "umounting all usb on %s" % schroot
        run("umountlist %s/dev/bus/usb/ | sh" % schroot)
        run("rm -rf %s/dev/bus/usb/" % schroot)
    else:
        run("umountlist %s/dev/bus/usb/%s | sh" % (schroot, dev))
        run("rm -f %s/dev/bus/usb/%s" % (schroot, dev))
    print "umount ok"


def find_session_and_run(session_name, f):
    session_list = find_sessions(session_name)
    if len(session_list) == 0:
        print "session not found: %s" % session_name
    elif len(session_list) == 1:
        f(session_list[0])
    else:
        print "multiple sessions found: "
        for session in session_list:
            print session

def print_usage_exit():
    print "usage: %s list" % sys.argv[0]
    print "       %s new [user] [schroot_conf_dir] " % sys.argv[0]
    print "       %s run [schroot]" % sys.argv[0]
    print "       %s end [schroot]" % sys.argv[0]
    print "       %s lsusb [schroot]" % sys.argv[0]
    print "       %s usb_mount [schroot] [bus/dev]" % sys.argv[0]
    print "       %s usb_umount [schroot] [bus/dev]" % sys.argv[0]
    exit(1)


if __name__ == '__main__':
    # FIXME: return code

    if len(sys.argv) > 1:
        command = sys.argv[1]
    else:
        command = ""

    if command == "new":
        if len(sys.argv) != 4:
            print_usage_exit()
        cmd_new(sys.argv[2], sys.argv[3])

    elif command == "list":
        for session in get_sessions():
            print session[len("session:"):]

    elif command == "run":
        if len(sys.argv) < 3:
            print_usage_exit()
        find_session_and_run(
            sys.argv[2], lambda x: run_exec("schroot --run-session -c %s" % x)
        )

    elif command == "end":
        if len(sys.argv) < 3:
            print_usage_exit()
        find_session_and_run(
            sys.argv[2], lambda x: run("schroot --end-session -c %s" % x)
        )

    elif command == "lsusb":
        if len(sys.argv) < 3:
            print_usage_exit()
        find_session_and_run(
            sys.argv[2], lambda x: cmd_lsusb(x)
        )

    elif command == "usb_mount":
        if len(sys.argv) < 4:
            print_usage_exit()
        find_session_and_run(
            sys.argv[2], lambda x: cmd_usb_mount(x, sys.argv[3])
        )

    elif command == "usb_umount":
        if len(sys.argv) < 4:
            print_usage_exit()
        find_session_and_run(
            sys.argv[2], lambda x: cmd_usb_umount(x, sys.argv[3])
        )

    else:
        print_usage_exit()
