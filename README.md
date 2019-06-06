### f5-networks-bigip-migrate-configuration

	There are severals (may be) easier ways to migrate bigip configuration from one unit to another, but i chose to use python, f5-sdk and ansible to accomplish this task.

### Executive Summary 
	If you want to migrate BigIP configurations from one unit to a another(new) unit then this repo will help you out.
	It is design in a way to transfer different bigip components ( monitors, pools, virtuals, data groups, users etc.) using independent python functions

### Environment
	1. f5-sdk : 3.0.14
	2. python : 3.6.5
	3. BigIP version (both source and destination ) : 12.1.2 HF1

### How to use it 
	Review and Execute Main.py file to start the migration

### Sequence 
	1. Migrate Monitors
	2. Migrate Pools
	3. Migrate Virtuals
	4. Migrate Users
	5. Compare Configuration 

### Requirements

	Folders needs to be created manually after Git download
	1. data
	2. ansible
	3. ansible/inv
	4. ansible/group_vars

	For Virtual Servers, migrate the following manually
	1. SSL Certificates
	2. SSL Profiles ( Client & Server SSL)
	3. Custom http profiles

	For Persistence profile
	1. It only check for "cookie" profiles

	For Ansible
	1. Create_DataGroups.py file needs to be udpated with ansible related variables

### Migrate Monitors

	Function : Create_Monitors(...)
		This will read all the monitors from the source BigIP and create ones which aren't part of "default" monitors.
		If need to skip any monitors then add in "default_monitors" list.

### Migrate Pools

	Function : Migrate_Pools(...)
		This will read all pools from source BigIP. Create one if it empty and move to the next one.
		If pool has members, then check if its FQDN enabled (['autopopulate'] == 'enabled')
		Fill up the pool payload with members information and call either Create_FQDNPool(...) function OR Create_Pool(...)
		- Function : Create_FQDNPool(...)
			Create FQDN node first and then add node to the pool
		- Function : Create_Pool(...)
			Create regular pool

### Migrate Virtuals

	Function : migrate_virtual(...)
		This will read all virtual servers from source bigip
		Fill up virtual payload with basic attributes
		Check for Persistence Profile, if exists then call fucntion Create_PersistenceProfile(...)

		- Function : Create_PersistenceProfile(...)
			Check for Cookie profiles, if doesn't exists then load from source BigIP and create on destination BigIP
			Check for rules, if attached then call function Create_iRules(...)

		- Function : Create_iRules(...)
			Check if iRules exists on the destination bigip, if not then read it from source and create on the destination bigip
			Also save the irules in the "data" folders to be scanned for any embedded data groups
			Call function Search_Datagroups(...) to scan iRules and look for data groups

			- Function : Search_Datagroups(...)
				Search Data Groups and return the name of Data Groups if found ( both internal and external data groups)
				Check if the data group is internal then call Create_Internal_DataGroup(...) to extract and create one
				If data group is external then call function Extract_DataGroup(...) to extract all data groups

			- Function : Extract_DataGroup (...)
				Check if DG exists on the source BigIP
				download the contents and save locally in the 'data' folder
				Call Create Data Groups to create all data groups extracted in the above function

			- Function : Create_DataGroups(...)
				I ran into a problem creating data group using f5-sdk. But found bigip ansible module to create datagroups
				So this function basically create an ansible script and pause while requesting to run an ansible script from a second terminal window
				This script also hard coded ansible variables
		Now iRules can be safely attached with the Virtual server, so add irules into virtual payload
		Next is to go through all the profiles attached to the virtual and add in the virtual payload
		Now Virtual payload has been updated with all the required elements and its time to create a virtual server on the destination bigip

		- Function : Create_Virtual(...)
			This will be called with destination bigip and virtual payload to create one 
			It will check if one exists prior to create one.

### Migrate Users

	Function : Migrate_Users(...)
		This function will read bigip local users, their encrypted passwords, their shell privilege as well as their roles and then create them on the destination bigip

### Compare Configuration 

	Function : Compare_Configs(...)
		This is a simple function
		This will download the following configuration from both Source and Destination bigips to compare in the "data" folder
		1. Pools info
		2. Virtuals info
		3. Users info


### useful links

	Check useful.links.md file

### Special Thanks
	Special Thanks to F5 Devcentral Community 
	Also it wasn't possible without f5-sdk and bigip ansible modules. So special thanks to f5-sdk and ansible teams.

### disclaimer 

	use at your own risk