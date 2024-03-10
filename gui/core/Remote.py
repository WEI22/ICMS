import paramiko

class Remote:
    def __init__(self):

        hostname = "192.168.100.86"
        username = "pi"
        password = "20010622"

        self.ssh = paramiko.SSHClient()

        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.ssh.connect(hostname=hostname, username=username, password=password)

        self.run_command("python streaming.py")

    def run_command(self, command):
        command = "cd playground && " + command
        stdin, stdout, sterr = self.ssh.exec_command(command)

    def close_ssh(self):
        self.ssh.close()

if __name__ == "__main__":
    r = Remote()
    r.close_ssh()