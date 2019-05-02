
# This module will create persistence profiles if needed

import sys
from pprint import pprint


def Create_PersistenceProfile(s_f5_mgmt,d_f5_mgmt,persist_profile_name):

	#print ("You are in Create Persistence Profile  Function !!!")

	# Check if persistence profile already exist then do nothing 
	if (d_f5_mgmt.tm.ltm.persistence.cookies.cookie.exists(name=persist_profile_name)):
		return

	else:
		# Get the cookie informaiont from source BigIP
		for c in s_f5_mgmt.tm.ltm.persistence.cookies.get_collection():
			if persist_profile_name == c.name:
				Cookie_payload = {
					'name' : c.name,
					'defaultsFrom' : c.defaultsFrom,
					'method': c.method,
					'httponly': c.httponly,
					'secure': c.secure,
					'alwaysSend' : c.alwaysSend,
					'expiration': c.expiration,
					'overrideConnectionLimit': c.overrideConnectionLimit,
					'timeout': c.timeout
				}

				d_f5_mgmt.tm.ltm.persistence.cookies.cookie.create(**Cookie_payload)
				
