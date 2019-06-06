# Purpose : Migrate all Virtuals from s_BigIP to d_BigIP

# This module will :
# 1. Load all Virtuals from Source BigIP
# 2. Fill up virtual_payload with name, profiles, irules  etc.
# 3. Create them on the destination bigip ... wait ... there is more 

# This module will use python 'unpacking' to create components on the dest bigip

# TODO : create a data file for all the virtuals created with their payload 

# TODO : 
# Manually transferred the following 
# 1. SSL Certificates
# 2. SSL Profiles ( Client / Server Side )
# 3. Stream Profile
# 4. http > X_ForwardedFor

import sys
import json
from pprint import pprint
from Create_Virtual import Create_Virtual
from Create_PersistenceProfile import Create_PersistenceProfile
from Create_iRules import Create_iRules
from Search_Datagroups import Search_Datagroups
from Create_DataGroups import Create_DataGroups
from Extract_DataGroup import Extract_DataGroup
from Create_Internal_DataGroup import Create_Internal_DataGroup


def migrate_virtuals(s_f5_mgmt,d_f5_mgmt):
	# Temp dictonary to hold virtual specific information
	virtual_payload = {}
	datagroup_list = ['False']

	# Extract all Virtuals from Source BigIP
	all_virtuals = s_f5_mgmt.tm.ltm.virtuals.get_collection()

	print ("You are in Migrate_Virtuals ...")

	# Iterate each and every Virtual and prepare to create on Destination BigIP
	for virtual in all_virtuals:


		print ("\n ====== {}  ===== ".format(virtual.name))

		# Grab Basic attributes :- name, destination, AutoMap, parition, Protocol
		# Fill the virtual_payload dict 
		virtual_payload['name'] = virtual.name
		virtual_payload['destination'] = virtual.destination.split('/')[2]
		virtual_payload['sourceAddressTranslation'] = virtual.sourceAddressTranslation
		virtual_payload['partition'] = virtual.partition
		virtual_payload['ipProtocol'] = virtual.ipProtocol

		# Now look for if a defaul poolt assigned to virtual 
		if 'pool' in virtual.raw.keys():
			virtual_payload['pool'] = virtual.pool

		# Check for description and update the payload
		if 'description' in virtual.raw.keys():
			virtual_payload['description'] = virtual.description

		# if any virtual server is in disabled state then disable it on the dest bigip too
		if 'disabled' in virtual.raw.keys():
			virtual_payload['disabled'] = virtual.disabled


		# Look for persistence profile attached, if it does then call a function to create a persistence profile		
		if 'persist' in virtual.raw.keys():
			#input ("Persist --- ")
			Create_PersistenceProfile(s_f5_mgmt,d_f5_mgmt,virtual.persist[0]['name'])
			virtual_payload['persist'] =  virtual.persist

		# Look for rules if attached to the Virtual, if does then call a function to create one
		if 'rules' in virtual.raw.keys():

			Create_iRules(s_f5_mgmt,d_f5_mgmt,virtual.rules)

			# iRule downloaded and saved locally under data folder
			# Scan it to find out if data groups are used 
			# Sample use of data group in iRules :  
			#	[class search -value apigateway-devirtual.company.info_datagroup contains $clientid ]
			#   [class match $LINKID equals qfnq.company.info_MD ]

			# Return a list of Data Groups used in the iRule
			datagroup_list = Search_Datagroups(d_f5_mgmt,virtual.rules)

			# TODO : Create a Data Groups using F5 SDK ... 

			if not 'False' in datagroup_list:
				# Now we have a list of Data Group Names
				for dg in datagroup_list:
					
					# Check if data group is an Internal then create one 

					if s_f5_mgmt.tm.ltm.data_group.internals.internal.exists(name=dg):
						#print ("This is an internal data group {} ... creating ".format(dg))
						Create_Internal_DataGroup(s_f5_mgmt,d_f5_mgmt,dg)
						continue

					# Its an external Data Group, extract its contents. 
					Extract_DataGroup(s_f5_mgmt,dg)


				# Now all external data groups are extracted and saved under data folder 
				# Call create data group to create on the destination bigip 	

				# Faced problems creating datagroups using f5-sdk 
				# hence ansible is used 
				# create ansible config file and then run it separatly 
				Create_DataGroups(d_f5_mgmt,datagroup_list,virtual.name)


			virtual_payload['rules'] = virtual.rules

		# Now look for profiles attached to this Virtual
		# List to contains profiles information 
		tmp_prof_list = []
		for prof in virtual.profiles_s.get_collection():
			#pprint (prof.raw)
			tmp_prof_dict = {}

			tmp_prof_dict['name'] = prof.name
			tmp_prof_dict['context'] = prof.context

			tmp_prof_list.append(tmp_prof_dict)
			#input("Press any key for next profile !!! ")

		#print (tmp_prof_list)
		virtual_payload['profiles'] = tmp_prof_list
		#pprint("Virtual Payload is  {}".format(virtual_payload))
		#input("Press Any Key to Create Virtual !!! xxxx ")


		Create_Virtual(d_f5_mgmt,virtual_payload)
		print ("Virtual Server created {}".format(virtual_payload['name']))

		virtual_payload.clear()


	

