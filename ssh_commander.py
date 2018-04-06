'''
Description - Script to execute ssh commands on PI
@author - John Sentz
@date - 04-Apr-2018
@time - 5:34 PM
'''

import paramiko

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

kill_command = 'sudo killall omxplayer.bin'
loop_command = 'omxplayer -o local --loop --aspect-mode stretch /home/pi/node_kiosk_B/app/static/videos/'


def loop_video(server, username, password, video_filename):

    command = loop_command + video_filename

    ssh.connect(server, port=22, username=username, password=password)
    ssh.exec_command(kill_command)
    ssh.exec_command(command)
    ssh.close()


def stop_video(server, username, password):

    ssh.connect(server, port=22, username=username, password=password)
    ssh.exec_command(kill_command)
    ssh.close()
