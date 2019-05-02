# This module will be called to create Virtuals
# It will check if virtual exists otherwise will create one

import sys

def Create_Virtual(f5_mgmt,virt_payload):

	# Check if pool exist
	print ("You are in Create Virtual Function !!!")
	print ("Creating Virtual {}".format(virt_payload['name']))
	if f5_mgmt.tm.ltm.virtuals.virtual.exists(name=virt_payload['name']):
		#print ("Virtual >> {} << exist ... skipping !!! \n".format(virt_payload['name']))
		pass

	else:
		f5_mgmt.tm.ltm.virtuals.virtual.create(**virt_payload)
		print ("Virtual >> {} << Created !!! \n".format(virt_payload['name']))

