# This module migrate users from source BigIP to destination bigip
# It will migrate their role as well as encrypted passwords
# No need to reset password or set role for the users on the destination bigip

def Migrate_Users(s_bigip_mgmt,d_bigip_mgmt):
	#print ("You are in Migrate Users .... ")

	# Users' list to skip during migration 
	users_to_skip = ['admin','ansible']
	# tmp user payload dict
	user_payload = {}

	# Get the list of users from source bigip
	users = s_bigip_mgmt.tm.auth.users.get_collection()

	for user in users:
		if user in users_to_skip:
			continue
		if d_bigip_mgmt.tm.auth.users.user.exists(name=user.name):
			continue

		# Remove the "nameReference" key from partition Access
		user.partitionAccess[0].pop('nameReference')

		user_payload = {
			'name' : user.name,
			'encryptedPassword' : user.encryptedPassword,
			'partitionAccess' : user.partitionAccess
			}

		# Some users doesn't have shell access 
		if 'shell' in user.raw.keys():
			user_payload['shell'] = user.shell

		d_bigip_mgmt.tm.auth.users.user.create(**user_payload)
		print ("User {} migrated ... ".format(user.name))
