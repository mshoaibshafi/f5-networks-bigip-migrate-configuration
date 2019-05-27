# This module will download the following configuration from both Source and Destination bigips in the "data" folder
# It needs to be compared manually

# TODO : add some logic to catch differences between the configuration if misssed

import sys


def Compare_Configs(s_f5_mgmt,d_f5_mgmt):

	print ("You are in Compare Config Function {} !!!")

	# Download pools info
	s_pool_info=s_f5_mgmt.tm.util.bash.exec_cmd("run",\
	 utilCmdArgs='-c "tmsh list /ltm pool"')
	#print (s_pool_info.commandResult)

	with open('data/' + "s_pools.txt",'w') as s_pools:
		s_pools.write(s_pool_info.commandResult)

	d_pool_info=d_f5_mgmt.tm.util.bash.exec_cmd("run",\
	 utilCmdArgs='-c "tmsh list /ltm pool"')

	with open('data/' + "d_pools.txt",'w') as d_pools:
		d_pools.write(d_pool_info.commandResult)


	# Donwload Virtuals Info
	s_virt_info=s_f5_mgmt.tm.util.bash.exec_cmd("run",\
	 utilCmdArgs='-c "tmsh list /ltm virtual"')

	with open('data/' + "s_virt.txt",'w') as s_virt:
		s_virt.write(s_virt_info.commandResult)

	d_virt_info=d_f5_mgmt.tm.util.bash.exec_cmd("run",\
	 utilCmdArgs='-c "tmsh list /ltm virtual"')

	with open('data/' + "d_virt.txt",'w') as d_virt:
		d_virt.write(d_virt_info.commandResult)

	# Download Users' info

	s_users_info=s_f5_mgmt.tm.util.bash.exec_cmd("run",\
	 utilCmdArgs='-c "tmsh list auth user"')

	with open('data/' + "s_users.txt",'w') as s_users:
		s_users.write(s_users_info.commandResult)

	d_users_info=d_f5_mgmt.tm.util.bash.exec_cmd("run",\
	 utilCmdArgs='-c "tmsh list auth user"')

	with open('data/' + "d_users.txt",'w') as d_users:
		d_users.write(d_users_info.commandResult)



