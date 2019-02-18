from dataclasses import dataclass
from entity.BaseLink import BaseLink
import paramiko
import re


@dataclass
class Linux(BaseLink):

    def __post_init__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)

    def connect(self):
        try:
            self.ssh.connect(self.host, username=self.user, password=self.password, timeout=30)
            return True
        except:
            return False

    def run(self, cmd):
        retstdin, stdout, stderr = self.ssh.exec_command(cmd)
        return stdout.readlines()

    def cpu(self):
        cpu_list = self.run("sed -n '1,1p' /proc/stat")[0].split(" ")
        used = int(cpu_list[2]) + int(cpu_list[3]) + int(cpu_list[4])
        return (100 * used)//(used + int(cpu_list[5]))

    def mem(self):
        mem_list = self.run('head /proc/meminfo')
        pattern = re.compile('\d+')
        total = int(re.search(pattern, mem_list[0]).group()) if re.search(pattern, mem_list[0]) else 0
        free = int(re.search(pattern, mem_list[2]).group()) if re.search(pattern, mem_list[2]) else 0
        return (100 * (total - free))//total