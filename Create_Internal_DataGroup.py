# This function will extract and create Only Internal data groups 


import sys, os
from pprint import pprint

def Create_Internal_DataGroup(s_f5_mgmt,d_f5_mgmt,dg_name):


    if d_f5_mgmt.tm.ltm.data_group.internals.internal.exists(name=dg_name):
        #input ("Skipping data group creation .... ")
        pass
    else:
        # Load internal data group from Source BigIP
        tmp_dg = s_f5_mgmt.tm.ltm.data_group.internals.internal.load(name=dg_name)

        # Prepare to create the data group in the destination bigip
        tmp_dg_data = { 
            'name': tmp_dg.name,
            'records': tmp_dg.records,
            'type' : tmp_dg.type
            }

        d_f5_mgmt.tm.ltm.data_group.internals.internal.create(**tmp_dg_data)
