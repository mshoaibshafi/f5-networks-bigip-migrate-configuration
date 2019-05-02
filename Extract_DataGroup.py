# Extract Data Groups from the source BigIP

import sys
from pprint import pprint

def Extract_DataGroup(s_f5_mgmt,dg_name):

	#print ("You are in Extract_DataGroups to extract {} !!!".format(dg_name))

	if s_f5_mgmt.tm.ltm.data_group.externals.external.exists(name=dg_name):
		#print ("DG {} exists on Source BigIP ".format(dg_name))
		#dg_info = s_f5_mgmt.tm.ltm.data_group.externals.external.load(name=dg_name)
		dg_name_local = s_f5_mgmt.tm.util.bash.exec_cmd('run',\
		 utilCmdArgs='-c "ls /config/filestore/files_d/Common_d/data_group_d/:Common:{}*"'.format(dg_name))

		extracted_filename = str(dg_name_local.commandResult.split(':')[2])

		#print ("{} \n {}".format(dg_name_local.commandResult,extracted_filename))

		dgshow = s_f5_mgmt.tm.util.bash.exec_cmd('run',\
			utilCmdArgs='-c "cat /config/filestore/files_d/Common_d/data_group_d/:Common:{0} " '.format(extracted_filename))
		print (dgshow.commandResult)
		with open('data/' + dg_name,'w') as dg_file:
			dg_file.write(dgshow.commandResult)

		# Download to data group contents 

	else:
		print ("DG {} Doesn't exists on Source BigIP ".format(dg_name))


	
