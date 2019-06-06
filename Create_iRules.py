# This module will create iRules

# TODO : 

import sys
from pprint import pprint

def Create_iRules(s_f5_mgmt,d_f5_mgmt,irules):

	# Extract the irule name from the list virtual.rules coming as irules
	rule_name = irules[0].split('/')[2]

	# Check if iRule exists on the destination BigIP
	if (d_f5_mgmt.tm.ltm.rules.rule.exists(name=rule_name)):
		#input("iRules {} exists ... ".format(rule_name))
		pass

	# Rule Doesn't exist
	# Load it from source BigIP and Create it on the destination BigIP
	else:
		r = s_f5_mgmt.tm.ltm.rules.rule.load(name=rule_name)
		# Create a payload and then do python unpacking
		rule_payload = {
			'name' : r.name,
			# rule contents 
			'apiAnonymous' : r.apiAnonymous,
			# Hard coded the partition as it is needed for to create iRules
			# It is also not part of load operation above to make it more generic
			'partition' : 'Common'
		}
		# Create a iRule on destination bigip
		#print("Creating iRule on the destination BigIP as well as saving a copy under data folder... ")
		d_f5_mgmt.tm.ltm.rules.rule.create(**rule_payload)

		# Save iRules in the data folder to scan for data groups
		with open('data/' + rule_name,'w') as file:
			file.write(rule_payload['apiAnonymous'])
