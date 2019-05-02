# This module will scan iRules and find if any data groups are used 

# TODO : 

import sys
from pprint import pprint

def Search_Datagroups(d_f5_mgmt,irules):
	#print ("You are in Search_Datagroups   Function !!!")

	# Extract the irule name from the list v.rules coming as irules
	rule_name = irules[0].split('/')[2]

	# Check if iRule exists on the destination BigIP
	# Load the irules
	# Search for all data groups
	# Put them in a list and return the list
	datagroup_list = []
	if (d_f5_mgmt.tm.ltm.rules.rule.exists(name=rule_name)):
		print ("Rule Exist on destination bigip ")
		r = d_f5_mgmt.tm.ltm.rules.rule.load(name=rule_name)

		# [class search -value apigateway-dev.company.info_linkIDs contains $LINKID ]
		# OR  
		# [class match $LINKID equals qfnq.company.info_MD ]

		if "class search -value" in r.apiAnonymous or "class match " in r.apiAnonymous:
			#print ("Data Group exist in rule {}".format(r.name))
			with open ('data/' + r.name,'r') as file2:
				line2 = []
				for line in file2.readlines():
					if "class search -value " in line:
						# Split the line [class search -value apigateway-dev.data_group_linkIDs contains $LINKID ]
						# first with [ and then ] and then by space to pick up the data group name
						# Output : apigateway-dev.data_group_linkIDs
						line = line.split('[')[1].split(']')[0].split(' ')[3]
						datagroup_list.append(line)

					if "class match " in line:
						# Sample :  [class match $LINKID equals qfnq.company.info_MD ]
						# Split the line [class match $LINKID equals qfnq.company.info_MD ]
						# first with [ and then ] and then by space to pick up the data group name
						# Output : qfnq.company.info_MD
						line = line.split('[')[1].split(']')[0].split(' ')[5]
						datagroup_list.append(line)

			#print (datagroup_list)
			# make it a set and then list to drop off any duplicate entries
			return list(set(datagroup_list))

		# Rule doesn't exist any Data groups
		# Return False 
		else:
			print ("Data Group Doesn't exisit ")
			return ['False']

	# Rule Doesn't exist
	else:
		#print ("Rule Doesn't Exist on destination bigip ")
		return ['False']

		