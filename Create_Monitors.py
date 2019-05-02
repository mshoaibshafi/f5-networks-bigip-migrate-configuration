# This module will :
# 1. Read all http monitors from source BigIP 
# 2. Skip the default_monitors as defined in the list below 
# 3. and will create all custom ones to the destination bigip

# This module will use python 'unpacking' to create components on the dest bigip

# TODO : create a data file for all the monitors created with their payload 

import sys

def Create_Monitors(s_bigip_mgmt,d_bigip_mgmt):
	# print ("You are in Create_Monitors .... ")

	# List of defaul monitors that will be skipped below
	default_monitors = ['http','gateway_icmp','https','http_head_f5','icmp','tcp']

	# Read all monitors from Source BigIP
	monitor = s_bigip_mgmt.tm.ltm.monitor.https.get_collection()

	for m in monitor:
		# tmp monitor payload dict
		http_monitor = {}
		# Skip if its a default monitor from the list above
		if m.name in default_monitors:
			continue

		# Skip if monitor already exists	
		elif (d_bigip_mgmt.tm.ltm.monitor.https.http.exists(name=m.name)):
			continue

		else:
			# prepare the payload
			http_monitor = { 
			    'name': m.name,
			    'partition': m.partition,
			    'interval' : m.interval,
			    'send' : m.send,
			    'timeUntilUp' : m.timeUntilUp,
			    'timeout' : m.timeout,
				}

			# python unpacking
			d_bigip_mgmt.tm.ltm.monitor.https.http.create(**http_monitor)
			print ("Monitor created >> {}".format(m.name))
			#input("Press Any Key ...")
