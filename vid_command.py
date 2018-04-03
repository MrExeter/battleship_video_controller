from time import sleep

import paramiko

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()

server = '10.0.1.13'
username = 'pi'
password = 'dingleberry'

ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(server, port=22, username=username, password=password)

# command = 'ls /'
# (stdin, stdout, stderr) = ssh.exec_command(command)
# for line in stdout.readlines():
#     print line

command = 'omxplayer -o local --loop --aspect-mode stretch /home/pi/node_kiosk_B/app/static/videos/Iowa_Launch.mp4'
ssh.exec_command(command)
# sleep(10)

ssh.close()
