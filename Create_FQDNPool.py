
# This function will create pools who has FQDN as members 

# Steps are :
# 1. Create a FQDN node first
# 2. Add that node to the pool

# Good link for creating FQDN nodes
# https://devcentral.f5.com/articles/creating-fqdn-nodes-via-icontrol-rest-24889
# 

def Create_FQDNPool(f5_mgmt,pool_payload):

	# Create a FQDN node first if doesn't exists
	if f5_mgmt.tm.ltm.nodes.node.exists(name=pool_payload['members'][0]['tmName']):
		print ("Node >> {} << exist ... skipping NODE creation  !!! ".format(pool_payload['members'][0]['tmName'] ))
	else:
		f5_mgmt.tm.ltm.nodes.node.create(name=pool_payload['members'][0]['tmName'] , \
			address='any6' , \
			fqdn={'tmName': pool_payload['members'][0]['tmName'] },\
			partition='Common')

	# Create a pool 
	if f5_mgmt.tm.ltm.pools.pool.exists(name=pool_payload['name']):
		print ("Pool >> {} << exist ... skipping !!! ".format(pool_payload['name']))
	else:
		f5_mgmt.tm.ltm.pools.pool.create(**pool_payload)
		print ("Pool >> {} << Created !!! ".format(pool_payload['name']))
