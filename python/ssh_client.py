import paramiko

class SSHClient:
    """Run commands on remote Linux server interactively. Initiate with host, usernmae & key file path. then call run_command()"""
    def __init__(self, hostname, username, keyfile):
        self.hostname = hostname
        self.username = username
        self.shell_command = ''
        self.ssh_key_file = keyfile
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.command_output = ''
        
    def _connect_open(self):
        try:
            self.client.connect(self.hostname, username=self.username, key_filename=self.ssh_key_file)
            # print("SSH connection established")
            return True
        except Exception as ex:
            print({ex})
            return False
        
    def _connect_close(self):
        self.client.close()
        
    def _execute_command_interactively(self):
        commands = ['ls', 'whoami', 'date']
        try:     
            for command in commands:
            #     print(f"Executing command: {command}")
                
            #     # Execute the command
            #     stdin, stdout, stderr = self.client.exec_command(command, get_pty=True)
                
            #     # Check if command execution is done
            #     while not stdout.channel.exit_status_ready():
            #         # Ready to read
            #         if stdout.channel.recv_ready():
            #             rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
            #             if len(rl) > 0:
            #                 # Print data from stdout
            #                 print(stdout.channel.recv(1024).decode('utf-8'), end='')
                            
            #         time.sleep(1)  # Wait a bit for output to accumulate

                print("\nCommand execution completed.\n")
        except Exception as e:
            print(f"An error occurred: {e}")

    def _execute_command(self):
        try:
            stdin, stdout, stderr = self.client.exec_command(self.shell_command)
            self.command_output = stdout.read().decode()
            print(self.command_output)
            print(stderr.read().decode())
        except Exception as ex:
            print(f"An error occurred: {ex}")
            
    def run_command(self,execute_command = ''):
        """Include the command you wan to run via SSH interactively"""
        if execute_command == '':
            print("No command passed to SSHclient")
        else:
            self.shell_command = execute_command
            if self._connect_open():
                self._execute_command()
                self._connect_close()
