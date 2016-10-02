#!/usr/bin/env python2
import sys, os
import hashlib

sys.path.append("/usr/local/lib/taner/")
from ipcsh import ipcsh as sh
import fsimg
from util import check_command, exit_error

_DEPENDENCY_PROGRAMS_ = ("debootstrap",)

def parse_dockerfile(dockerfile_str):
    commands = [] # (TYPE, CMD)
    dockerfile_str = dockerfile_str.replace('\\\n', '')
    i = 0
    for line in dockerfile_str.split('\n'):
        if line == "":
            continue
        pos = line.find(' ')
        if pos < 0:
            TYPE = line
            CMD = ""
        else:
            TYPE = line[:pos]
            CMD = line[len(TYPE)+1:]

        commands.append((TYPE, CMD))
    return commands

class DockerBuildKvm:

    def __init__(self, FS_FILE, FS_FILE_SIZE, HOST_KERNEL_PARAMETERS=""):
        self.image_created = False
        self.FS_FILE = FS_FILE
        self.FS_FILE_SIZE = FS_FILE_SIZE
        self.FS_FILE_FORMAT = "ext2"
        self.FS_FILE_MOUNT_FLAGS=""
        self.HOST_KERNEL_PARAMETERS = HOST_KERNEL_PARAMETERS
        self.KERNEL_PARAMETERS = ""
        self.DIR = "%s.dockerbuild-kvm" % self.FS_FILE

        self.functions = {
            "DEBOOTSTRAP": lambda x: self.DEBOOTSTRAP(*x.split()),
            "ADD": lambda x: self.ADD(*x.split()),
            "RUN": self.RUN
        }

    def mount(self, ro=False):
        if ro:
            options = "-o ro"
        else:
            options = "-o rw"
        if self.FS_FILE_MOUNT_FLAGS != "":
            options += ",%s" % self.FS_FILE_MOUNT_FLAGS
        fsimg.mount(self.FS_FILE, self.DIR, options=options)

    def umount(self):
        DIR = self.DIR
        sh << "umountlist %(DIR)s | sh" > None

    def ADD(self, source, dst):
        DIR = self.DIR
        self.mount()
        sh << "cp -rf %(source)s %(DIR)s/%(dst)s" > None
        self.umount()

    def RUN(self, cmd):

        FS_FILE, DIR, HOST_KERNEL_PARAMETERS = self.FS_FILE, self.DIR, self.HOST_KERNEL_PARAMETERS

        cmd_hash = hashlib.sha256()
        cmd_hash.update(cmd)
        cmd_hash = cmd_hash.hexdigest()

        self.mount()

        sh << "cp -rf kvm_dockerfile_build.files/entry_point/serial-getty@ttyS0.service.d/ %(DIR)s/etc/systemd/system/" > None

        open("%s/entry_point.sh" % DIR, "w").write(
            "#!/bin/bash\n%(cmd)s\necho -n '%(cmd_hash)s' > /entry_point.last_run\npoweroff"
            % {"cmd": cmd, "cmd_hash": cmd_hash}
        )
        sh << "chmod +x %(DIR)s/entry_point.sh" > None

        vm_kernel_list = sh << "find %(DIR)s/boot -name 'vmlinuz-*'" > str
        vm_initrd_list = sh << "find %(DIR)s/boot -name 'initrd.img-*'" > str

        kernel_parameters = "%s" % self.KERNEL_PARAMETERS
        if self.FS_FILE_MOUNT_FLAGS != "":
            kernel_parameters += " rootflags=%s" % self.FS_FILE_MOUNT_FLAGS
        if vm_kernel_list != "":
            kernel = vm_kernel_list.split('\n')[0]
        else:
            kernel = "/vmlinuz"
            kernel_parameters += " %s" % HOST_KERNEL_PARAMETERS

        if vm_initrd_list != "":
            initrd = vm_initrd_list.split('\n')[0]
        else:
            initrd = "/initrd.img"

        self.umount()

        self.mount(ro=True)
        print "--------------"
        print "running kvm"
        print "kernel: %s" % kernel
        print "initrd: %s" % initrd
        print "kernel parameters: %s" % kernel_parameters
        sh << "kvm -smp $(nproc) -m 1024 -nographic -serial mon:stdio -kernel " \
            "%(kernel)s -initrd %(initrd)s -drive file=%(FS_FILE)s,if=virtio " \
            "-append '%(kernel_parameters)s root=/dev/vda rw console=ttyS0 quiet'" > None
        self.umount()

        self.mount(ro=True)
        success = open("%s/entry_point.last_run" % DIR).read() == cmd_hash
        assert success
        self.umount()


    def create_image(self):
        fsimg.create(self.FS_FILE, self.FS_FILE_SIZE, self.FS_FILE_FORMAT)

    def DEBOOTSTRAP(self, suite, mirror):
        DIR = self.DIR
        self.create_image()
        self.mount()

        sh << "debootstrap %(suite)s %(DIR)s %(mirror)s" > None

        sh << "cp -rf kvm_dockerfile_build.files/entry_point/serial-getty@ttyS0.service.d/ %(DIR)s/etc/systemd/system/" > None
        assert sh.r == 0
        sh << "cp -rf kvm_dockerfile_build.files/interfaces %(DIR)s/etc/network/interfaces" > None
        assert sh.r == 0
        open("%s/build_stage.txt" % DIR, "w").write("0")

        self.umount()
        self.image_created = True

    def build(self, file_str):

        for cmd_no, cmd in enumerate(parse_dockerfile(file_str)):
            print "cmd:", cmd[0]
            print "parameters:", cmd[1]
            if cmd[0] == "#EXIT":
                print "EXIT command"
                exit(0)
            elif cmd[0] == "#FS_FILE_FORMAT":
                assert not self.image_created
                assert cmd[1] != "" and cmd[1] in ('ext2', 'ext3', 'ext4', 'btrfs')
                print "fs file format: %s" % cmd[1]
                self.FS_FILE_FORMAT = cmd[1]
            elif cmd[0] == "#FS_FILE_MOUNT_FLAGS":
                self.FS_FILE_MOUNT_FLAGS = cmd[1]
                print "fs file mount flags: %s" % cmd[1]
            elif cmd[0] == "#ADD_KERNEL_PARAMETER":
                print "add kernel parameter: %s" % cmd[1]
                self.KERNEL_PARAMETERS += " %s " % cmd[1]
            elif cmd[0][0] == '#':
                pass
            elif cmd[0] not in self.functions:
                print "command not supperted: %s" % cmd[0]
                exit(1)
            else:
                f = self.functions[cmd[0]]
                cmd_params = cmd[1]
                f(cmd_params)

        self.mount()
        DIR = self.DIR
        open("%s/entry_point.sh" % DIR, "w").write("#!/bin/bash\nexec /bin/bash")
        sh << "chmod +x %(DIR)s/entry_point.sh" > None
        self.umount()


if __name__ == '__main__':
    check_command(*(fsimg._DEPENDENCY_PROGRAMS_ + _DEPENDENCY_PROGRAMS_)) or exit_error("check dependency programs and run as root")

    dockerfile, fs_file, fs_file_size, kernel_parameters = sys.argv[1:5]

    dockerbuild = DockerBuildKvm(fs_file, fs_file_size, kernel_parameters)

    not os.path.exists(dockerbuild.DIR) or exit_error("ERROR: %s directory exists" % dockerbuild.DIR)

    os.mkdir(dockerbuild.DIR)
    try:
        dockerbuild.build(open(dockerfile).read())
    finally:
        DIR = dockerbuild.DIR
        sh << "umountlist %(DIR)s | sh" > None
        os.rmdir(dockerbuild.DIR)
