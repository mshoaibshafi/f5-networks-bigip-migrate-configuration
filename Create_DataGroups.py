# This function will create all data groups extracted in the previous function

# Important Note : 
# Please update the ansible related variables below before using this file

import sys, os

def Create_DataGroups(d_f5_mgmt,dg_list,virt_name):

	#print ("You are in Create_DataGroups !!!")

	# If same virtual server appeneded with https or http then trim it to avoid duplication
	virt_name = virt_name.replace('-https','')
	virt_name = virt_name.replace('-http','')

	# Create an ansible yaml file and then provide the ansible-playbook command at the end to run from a different window
	# skip if ansible file already exists 

	if (os.path.isfile("ansible/group_vars/"+virt_name)):
		print ("\nAnsible file already exist skipping data group creation  ..... ")
		print ("\n Assuming data group created either during -http or -https VIP creation " )
		#input("returning ... ")
		return
	else:
		# Ansible related variables
		new_ansible_file = open("ansible/group_vars/"+virt_name,"w")
		new_ansible_file.write("\nbigip_username: \"ansible\"")
		new_ansible_file.write("\nbigip_password: \"password\"")
		new_ansible_file.write("\nbigip_port: \"443\"")
		new_ansible_file.write("\nvalidate_certs: \"no\"")
		new_ansible_file.write("\nbigip_server : \"labbigip2800\" ")
		new_ansible_file.write("\n")
		new_ansible_file.write("\n# === Data Group Config Variables === ")
		new_ansible_file.write("\nDataGroup_with_items:")

		for dg_name in dg_list:
			new_ansible_file.write("\n- external_file_name: {}".format(dg_name))
			new_ansible_file.write("\n  name: \"{}\"".format(dg_name))
			new_ansible_file.write("\n  records_src: \"../data/{}\"".format(dg_name))
	
	
		new_ansible_file.close()
	
		with open("ansible/inv/hosts","w") as new_host_file:
			new_host_file.write("\n[{}]".format(virt_name))
			new_host_file.write("\nlabbigip2800 ansible_host=localhost")

		print ("\nRun the following ansible command to create Data Groups !!!! ")
		print (" cd ansible ; sudo ansible-playbook -i inv/hosts -e \"hosts={}\" create-datagroups.yaml ".format(virt_name))

		input("Run the ansible from second window !!! ")

#		


#		bigip_username: "admin" 
#		bigip_password: "r@1d3r" 
#		bigip_port: 443 
#		validate_certs: "no" 
#		bigip_server : "labbigip2800" 
#		bigip_partition : "Common" 


#	# === Data Group Config Variables === 
#	DataGroup_with_items:
#	- external_file_name: samplesite.evenue.net_ph 
#	  name: "samplesite.evenue.net_ph" 
#	  records_src: "../data/samplesite.evenue.net_ph" 
#	- external_file_name: samplesite.evenue.net_qit 
#	  name: "samplesite.evenue.net_qit" 
#	  records_src: "../data/samplesite.evenue.net_qit" 
#	- external_file_name: northernquest.evenue.net_sd 
#	  name: "samplesite.evenue.net_sd" 
#	  records_src: "../data/samplesite.evenue.net_sd" 
#	- external_file_name: samplesite.evenue.net_linkids 
#	  name: "samplesite.evenue.net_linkids" 
#	  records_src: "../data/samplesite.evenue.net_linkids" #



