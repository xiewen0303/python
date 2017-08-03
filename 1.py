#!/usr/bin/env Python
#coding=utf-8

import paramiko
import select
import sys
import argparse

reload(sys)
sys.setdefaultencoding("utf8")


hostname="172.24.3.5"
port=22
username="developer"
password="b90d1666e0859371bd744cd45fea7b8c"



class RemoteHandler:

	def test_remote_disk(self):
		s=paramiko.SSHClient()
		s.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
		s.connect(hostname,port,username,password) 
		stdin,stdout,sterr=s.exec_command("df -Th") 
		print stdout.read() 
		s.close()
		
	def cmd_remote(self,commandStr):
		s=paramiko.SSHClient()
		s.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
		s.connect(hostname,port,username,password) 
		stdin,stdout,sterr=s.exec_command(commandStr) 
		
		while not stdout.channel.exit_status_ready(): 
			if stdout.channel.recv_ready():
				rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
				if len(rl) > 0:
					# Print data from stdout
					#stdout.read()
					try:
						print (stdout.channel.recv(1024).decode("utf8"))
					except UnicodeDecodeError:
						print ("---------UnicodeDecodeError-----------")
					
		channel = stdout.channel
		status = channel.recv_exit_status()
		print status
		#print stdout.read() 
		s.close()
	
	


if __name__=="__main__": 
		parser = argparse.ArgumentParser(description="This is a description of [%(prog)s]", epilog="This is a epilog of [%(prog)s]", fromfile_prefix_chars='@', prefix_chars="-", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
		parser.add_argument('-restart', nargs='?', dest='type', choices=['test','banshu','kf','kf_match','gm'], default='game', help='Select the actions in the choices')
		
		#print parser.print_help()
		print 'you can enter:  python 1.py -restart=test '
		
		command_str =""
		if len(sys.argv) == 1:
			print "\n"
			print parser.print_help()
		else:
			args = parser.parse_args()
			if(args.type == 'test'):
				command_str = "sh /data/server/runfile/soft/stop.sh;sleep 10;sh /data/server/runfile/soft/start.sh;sleep 40"
			elif(args.type == 'banshu'):
				command_str = "sh /data/server/runfile_bs/soft/stop.sh;sleep 10;sh /data/server/runfile_bs/soft/start.sh;sleep 40"
			elif(args.type == 'kf'):
				command_str = "sh /data/server/runfile_kf/soft/stop.sh;sleep 10;sh /data/server/runfile_kf/soft/start.sh;sleep 40"
			elif(args.type == 'kf_match'):
				command_str = "sh /data/server/runfile_kf_match/soft/stop.sh;sleep 10;sh /data/server/runfile_kf_match/soft/start.sh;sleep 40"
			else:
				print "\n\033[41;30mError:\033[0m invalid type \033[47;30m%s\033[0m\n" % (args.type)
				print parser.print_help()
				exit(1)
				
			print  "cmd ====" + command_str
			
			remoteHandler = RemoteHandler()
			remoteHandler.cmd_remote(command_str)
			
	#remoteHandler = RemoteHandler()
	#remoteHandler.cmd_remote("sh /data/server/runfile_bs/soft/stop.sh;sleep 10;sh /data/server/runfile_bs/soft/start.sh;sleep 30")
	
	
	#remoteHandler.cmd_remote("sh /data/server/runfile_game/nizhuan_server_1/soft/stop.sh;sleep 10;sh /data/server/runfile_game/nizhuan_server_1/soft/start.sh;sleep 40")
	#remoteHandler.cmd_remote(")
