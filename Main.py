# This is a main file 
# It calls individual functions to create different Bigip components

# Sequence would be :

# 1. Create Monitors
# 2. Create Pools
# 3. Create Profiles
# 4. Create Virtuals

# Imports 
from f5.bigip import ManagementRoot
import sys,os
from Create_Monitors import Create_Monitors
from Migrate_Pools import Migrate_Pools
from migrate_virtuals import migrate_virtuals
from Extract_DataGroup import Extract_DataGroup
from Compare_Configs import Compare_Configs
from Migrate_Users import Migrate_Users

# Source and Destination BigIP credentials
# Extract from the enviornment Variables

# Sample 
# s_BigIP_IP = "10.10.10.10"
# s_Username = "admin"
# s_Password = "admin"

# Source
s_BigIP_IP = os.environ.get('s_BigIP_IP')
s_Username = os.environ.get('s_Username')
s_Password = os.environ.get('s_Password')

# Destination
d_BigIP_IP = os.environ.get('d_BigIP_IP')
d_Username = os.environ.get('d_Username')
d_Password = os.environ.get('d_Password')

# Verify if required directory structure exists prior to start.
# If it doesn't then create one 

if not os.path.isdir("data"):
	print ("\nError: \"data\" folder is required for the successful execution of this script! ")
	input("Press any to create one ... ")
	os.makedirs("data")

if not os.path.isdir("ansible"):
	print ("\nError: \"ansible\" folder is required for the successful execution of this script! ")
	input("Press any to create one ... ")
	os.makedirs("ansible")

if not os.path.isdir("ansible/inv"):
	print ("\nError: \"ansible/inv\" folder is required for the successful execution of this script! ")
	input("Press any to create one ... ")
	os.makedirs("ansible/inv")

if not os.path.isdir("ansible/group_vars"):
	print ("\nError: \"ansible/group_vars\" folder is required for the successful execution of this script! ")
	input("Press any to create one ... ")
	os.makedirs("ansible/group_vars")

# Create source and dest BigIP Mgmt pointers
try:
	s_F5_MGMT = ManagementRoot(s_BigIP_IP,s_Username,s_Password)
	d_F5_MGMT = ManagementRoot(d_BigIP_IP, d_Username, d_Password)
except:
	print("Error: -- \n Please make sure environment variables for BigIP IP, Username and Password are set correctly!")
	print(" Sample shell script to set env variable is included - export_env.sh \n")
	sys.exit()



# Migrate Monitors from Source BigIP to Dest BigIP
# These moniors are used by Pools including ones contains FQDN as their pool members
Create_Monitors(s_F5_MGMT,d_F5_MGMT)
input("Monitors created ")

# Migrate Pools 
Migrate_Pools(s_F5_MGMT,d_F5_MGMT)
input("Pools created ")


# Migrate Virtual Servers along with their Persistence Profiles, iRules, Data Groups 
migrate_virtuals(s_F5_MGMT,d_F5_MGMT)
input("Virtual created ")


# Migrate users
## Migrate_Users(s_F5_MGMT,d_F5_MGMT)
## input("Users Created")

# Compare Pools
## Compare_Configs(s_F5_MGMT,d_F5_MGMT)
## input("Configs ready to compare ")

