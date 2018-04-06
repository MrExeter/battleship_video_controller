'''
Description - Utility class for sending ssh commands to Nodes
@author - John Sentz
@date - 04-Apr-2018
@time - 3:33 PM
'''

import paramiko

kill_command = 'sudo killall omxplayer.bin'
loop_command = 'omxplayer -o local --loop --aspect-mode stretch /home/pi/node_kiosk_B/app/static/videos/'

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())


class Uecker(object):

    @classmethod
    def loop_video(cls, network_address, username, password, filename):
        command = loop_command + filename
        ssh.connect(network_address, port=22, username=username, password=password)
        ssh.exec_command(kill_command)
        ssh.exec_command(command)
        ssh.close()

    @classmethod
    def stop_video(cls, network_address, username, password):
        ssh.connect(network_address, port=22, username=username, password=password)
        ssh.exec_command(kill_command)
        ssh.close()
