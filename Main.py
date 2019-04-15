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


# Create source and dest BigIP Mgmt pointers
s_F5_MGMT = ManagementRoot(s_BigIP_IP,s_Username,s_Password)
d_F5_MGMT = ManagementRoot(d_BigIP_IP, d_Username, d_Password)



Create_Monitors(s_F5_MGMT,d_F5_MGMT)
Migrate_Pools(s_F5_MGMT,d_F5_MGMT)



# TODO :
# Create_Profiles(s_F5_MGMT,d_F5_MGMT)
# Create_Virtual(F5_MGMT,Virtual_Config_Param)


