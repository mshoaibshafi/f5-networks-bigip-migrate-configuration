# Purpose : Migrate all Pools from one s_BigIP to d_BigIP

# This module will :
# 1. Load all pools from Source BigIP
# 2. Fill up pool_payload with name, monitor, load balancing etc.
# 3. Create a pool if its empty else load all members from the pool 
# 4. Check if pool has "FQDN" members and call Create_FQDNPool function to create one
# 5. Call Create_Pool for non-FQDN pools

# This module will use python 'unpacking' to create components on the dest bigip

# TODO : create a data file for all the pools created with their payload 
# TODO : add member / node description 

import sys,json
from pprint import pprint
from Create_Pool import Create_Pool
from Create_FQDNPool import Create_FQDNPool

def Migrate_Pools(s_f5_mgmt,d_f5_mgmt):
	# Load all the pool names from the Source BigIP
	# print ("You are in Migrate_Pools function")

	# Temp dictonary to hold pool specific information
	pool_payload = {}
	all_pools = s_f5_mgmt.tm.ltm.pools.get_collection()
	for pool in all_pools:

		pool_payload['name'] = pool.name
		pool_payload['monitor'] = pool.monitor
		pool_payload['loadBalancingMode'] = pool.loadBalancingMode

		# Add description if exist 
		if 'description' in pool.raw.keys():
			pool_payload['description'] = pool.description


		# tmp List to contains all members in the pool
		m2 = []

		# Create a pool if its empty or has no members 
		if (len(pool.members_s.get_collection())) == 0:
			print ("This pool has no members ... empty pool >> {}".format(pool.name))
			Create_Pool(d_f5_mgmt,pool_payload)
			pool_payload.clear()
			continue

		# Look for members 
		for member in pool.members_s.get_collection():
			# Temp Dict to contain individual member's info
			m1 = {}

			# Split between FQDN or non-FQDN pools creation
			# FQDN Pools
			if member.fqdn['autopopulate'] == 'enabled':
				#print ("\nFQDN members >>> {}".format(pool.name))

				# this variable will be used while calling Create Pool fuction below 
				FQDN = True
				#print ("{} is a FQDN pool".format(pool.name))

				pool_payload['fqdn'] = 'enabled'
				pool_payload['address'] = member.address

				# Fill up FQDN pool member specifics 
				m1['name'] = member.name
				m1['tmName'] = member.fqdn['tmName']
				m2.append(m1)
				pool_payload['members'] = m2

				# Don't search for FQDN nodes as they will be dynamically added automatically by BigIP
				break


			# non FQDN pools	
			else:
				# this variable will be used while calling Create Pool fuction below 
				FQDN = False

				# Fill up non FQDN pool member specifics 
				m1['name'] = member.name
				m1['address'] = member.address
				m1['connectionLimit'] = member.connectionLimit

				# If member disabled then add it as disabled node
				# by default all added members are enabled
				if member.session == "user-disabled":
					m1['session'] = member.session

				# Add into the tmp pool members list
				m2.append(m1)
				# Add tmp pool list into a pool pay load
				pool_payload['members'] = m2

		if FQDN:
			#print("\n FQDN  ------- pool_payload >> {}".format(pool_payload))			
			Create_FQDNPool(d_f5_mgmt ,pool_payload)

		else :
			#print("\n non FQDN ------- pool_payload >> {}".format(pool_payload))
			Create_Pool(d_f5_mgmt,pool_payload)
		print ("Pool Created {}".format(pool_payload['name']))

		# Clear variables for the next pool
		m1.clear()
		pool_payload.clear()



