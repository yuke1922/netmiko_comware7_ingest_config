import os
import pandas as pd
from netmiko import ConnectHandler
from getpass import getpass
from pprint import pprint
import json

def clear():
    os.system('clear')

clear()
os.system('rm -rf *.xlsx')
os.system('rm -rf output')
clear()
password = getpass()
clear()

print("Gathering Device")

device = {
        "device_type":"hp_comware",
        "host":"172.19.20.30.",
        "username":"admin",
        "password":password,
        }
clear()
net_connect = ConnectHandler(**device)
print("Processing Layer 2 VLANs...")
cmw_l2_vlan = (net_connect.send_command('display vlan brief', use_textfsm=True))
clear()
print("Processing Layer 3 VLANs...")
cmw_l3_vlan = (net_connect.send_command('dis ip interface', use_textfsm=True))
clear()
print("Processing LLDP Neighbors...")
cmw_lldp = (net_connect.send_command('dis lldp neighbor-information verbose', use_textfsm=True))
clear()
print("Processing Routing Table...")
cmw_iproute = (net_connect.send_command('dis ip routing-table', use_textfsm=True))
clear()
print("Processing Device Inventory...")
cmw_inv = (net_connect.send_command('dis dev manu', use_textfsm=True))

cmw_gig_ports = (net_connect.send_command('display current', use_ttp=True, ttp_template='ttp/gig_intf.ttp'))

cmw_xge_ports = (net_connect.send_command('display current', use_ttp=True, ttp_template='ttp/xge_intf.ttp'))

cmw_lag_ports = (net_connect.send_command('display current', use_ttp=True, ttp_template='ttp/lag_intf.ttp'))

os.system('mkdir output')

clear()
print("Organizing and Exporting")
cmw_gig_ports_df = pd.DataFrame.from_dict(cmw_gig_ports[0][0])

cmw_gig_ports_df.to_csv('./output/gig_ports.csv', index = False)

cmw_xge_ports_df = pd.DataFrame.from_dict(cmw_xge_ports[0][0])

cmw_xge_ports_df.to_csv('./output/xge_ports.csv', index = False)

cmw_lag_ports_df = pd.DataFrame.from_dict(cmw_lag_ports[0][0])

cmw_lag_ports_df.to_csv('./output/lag_ports.csv', index = False)

cmw_l3vlan_df = pd.DataFrame.from_dict(cmw_l3_vlan)

cmw_l3vlan_df.to_csv('./output/l3_vlan.csv', index = False)

cmw_l2vlan_df = pd.DataFrame.from_dict(cmw_l2_vlan)

cmw_l2vlan_df.to_csv('./output/l2_vlan.csv', index = False)

cmw_lldp_df = pd.DataFrame.from_dict(cmw_lldp)

cmw_lldp_df.to_csv('./output/lldp.csv', index = False)

cmw_iproute_df = pd.DataFrame.from_dict(cmw_iproute)

cmw_iproute_df.to_csv('./output/iproute.csv', index = False)

cmw_inv_df = pd.DataFrame.from_dict(cmw_inv)

cmw_inv_df.to_csv('./output/inventory.csv', index = False)







clear()
