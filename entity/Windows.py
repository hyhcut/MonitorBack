from dataclasses import dataclass
from winrm.protocol import Protocol
from base64 import b64encode
from entity.BaseLink import BaseLink


@dataclass
class Windows(BaseLink):

    def __post_init__(self):
        self.session = Protocol(
            endpoint='http://' + self.host + ':5985/wsman',
            transport='ntlm',
            username=self.user,
            password=self.password,
            server_cert_validation='ignore')

    def connect(self):
        try:
            shell_id = self.session.open_shell()
            self.session.run_command(shell_id, 'echo 123')
            self.session.close_shell(shell_id)
            return True
        except:
            return False

    def run(self, scripts):
        shell_id = self.session.open_shell()
        encoded_ps = b64encode(scripts.encode('utf_16_le')).decode('ascii')
        command_id = self.session.run_command(shell_id, 'powershell -encodedcommand {0}'.format(encoded_ps))
        std_out, std_err, status_code = self.session.get_command_output(shell_id, command_id)
        self.session.close_shell(shell_id)
        return std_out, std_err, status_code

    def cpu(self):
        ps_script = """$Server = $env:computername
            $cpu = Get-WMIObject –computername $Server win32_Processor
            "{0:0.0}" -f $cpu.LoadPercentage"""
        std_out, std_err, status_code = self.run(ps_script)
        result = str(std_out, encoding='utf-8')
        cpu_used = float(result.strip('\n').strip('\r'))
        return cpu_used

    def mem(self):
        script = """$mem = gwmi win32_OperatingSystem
            "{0:0.0}" -f ((($mem.TotalVisibleMemorySize-$mem.FreePhysicalMemory)/$mem.TotalVisibleMemorySize)*100)"""
        std_out, std_err, status_code = self.run(script)
        result = str(std_out, encoding='utf-8')
        mem_used = float(result.strip('\n').strip('\r'))
        return mem_used
