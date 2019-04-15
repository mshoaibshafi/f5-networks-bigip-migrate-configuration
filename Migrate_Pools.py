# Purpose : Migrate all Pools from one s_BigIP to d_BigIP

# This module will :
# 1. Load all pools from Source BigIP
# 2. Fill up pool_payload with name, monitor, load balancing etc.
# 3. Load all members from the pool and create one if its empty 
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
	# Load all the pool names from Source BigIP s_f5_mgmt
	# print ("You are in Migrate_Pools function")
	# Temp dictonary to hold pool specific information
	pool_payload = {}
	all_pools = s_f5_mgmt.tm.ltm.pools.get_collection()
	for pool in all_pools:
		#pprint (pool.raw)
		pool_payload['name'] = pool.name
		pool_payload['monitor'] = pool.monitor
		pool_payload['loadBalancingMode'] = pool.loadBalancingMode

		if 'description' in pool.raw.keys():
			pool_payload['description'] = pool.description


		# List to contains members information 
		m2 = []

		# Check if Pool is empty
		if (len(pool.members_s.get_collection())) == 0:
			print ("This pool has no members ... empty pool >> {}".format(pool.name))
			Create_Pool(d_f5_mgmt,pool_payload)
			pool_payload.clear()
			continue

		for member in pool.members_s.get_collection():
			# Temp Dict to contains member data
			m1 = {}

			# split between FQDN or non-FQDN pools creation

			# FQDN Pools
			if member.fqdn['autopopulate'] == 'enabled':
				print ("\nFQDN members >>> {}".format(pool.name))
				FQDN = True
				print ("{} is a FQDN pool".format(pool.name))
				pool_payload['fqdn'] = 'enabled'
				pool_payload['address'] = member.address

				m1['name'] = member.name
				m1['tmName'] = member.fqdn['tmName']
				m2.append(m1)
				pool_payload['members'] = m2
				# don't pick up nodes which are dynamically added nodes for FQDN pools
				break


			# non FQDN pools	
			else:
				FQDN = False
				m1['name'] = member.name
				m1['address'] = member.address
				m1['connectionLimit'] = member.connectionLimit

				# If member disabled then add it as disabled node
				# by default all added members are enabled
				if member.session == "user-disabled":
					m1['session'] = member.session

				m2.append(m1)
				pool_payload['members'] = m2


		if FQDN:
			print("\n FQDN  ------- pool_payload >> {}".format(pool_payload))			
			Create_FQDNPool(d_f5_mgmt ,pool_payload)
			#input("Next Pool  .... ")
		else :

			print("\n non FQDN ------- pool_payload >> {}".format(pool_payload))
			#input("Ready to Create Pool  .... ")
			Create_Pool(d_f5_mgmt,pool_payload)
			#input("Next Pool  .... ")

		# Clear variables for the next element
		m1.clear()
		pool_payload.clear()
