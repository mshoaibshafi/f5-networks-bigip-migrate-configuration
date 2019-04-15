# This module will be called to create non FQDN pools

# It will check if pool exists otherwise will create one

# This will use python unpacking 

# TODO : add member / node description 

import sys


def Create_Pool(f5_mgmt,pool_payload):

	# Check if pool exist
	# print ("You are in Create Pool Function !!!")
	if f5_mgmt.tm.ltm.pools.pool.exists(name=pool_payload['name']):
		print ("Pool >> {} << exist ... skipping !!! ".format(pool_payload['name']))

	else:
		f5_mgmt.tm.ltm.pools.pool.create(**pool_payload)
		print ("Pool >> {} << Created !!! ".format(pool_payload['name']))
