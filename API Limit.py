import pyrax
import requests
import json

API_Key = raw_input("Enter API Key: ")
username = raw_input("Enter username:  ")
DDI = raw_input("Enter DDI: ")

pyrax.set_setting("identity_type", "rackspace")
auth = pyrax.set_setting("identity_type", "rackspace")
#pyrax.set_default_region("DFW")
pyrax.set_credentials(username, API_Key)
authid = pyrax.identity
auth_token = authid.token

cs_dfw = pyrax.connect_to_cloudservers(region='DFW')
cs_iad = pyrax.connect_to_cloudservers(region='IAD')
cs_ord = pyrax.connect_to_cloudservers(region='ORD')
cf = pyrax.cloudfiles
cbs_dfw = pyrax.cloud_blockstorage
cdb = pyrax.cloud_databases
clb = pyrax.cloud_loadbalancers
clb_ord = pyrax.connect_to_cloud_loadbalancers(region='ORD')
clb_iad = pyrax.connect_to_cloud_loadbalancers(region='IAD')
clb_list_ord = clb_ord.list()
clb_list_iad = clb_iad.list()
dns = pyrax.cloud_dns
cnw = pyrax.cloud_networks


cslimits_iad = cs_iad.limits.get()
  # Convert the generator to a list
cslimits_iad_list = [rate for rate in cslimits_iad.absolute]
  # Pull out max_ram api limit and total used ram from list
max_ram_IAD = [x.value for x in cslimits_iad_list if x.name == "maxTotalRAMSize"][0]
total_ram_IAD = [x.value for x in cslimits_iad_list if x.name == "totalRAMUsed"][0]
#Get the percent ram used and round it up for clean output
percent_ram_IAD = (float(total_ram_IAD) / float(max_ram_IAD)) * 100
percent_ram_used_IAD = round(float(("%.2f" % percent_ram_IAD)))

print ("Cloud Servers - IAD ")
print ("    Total RAM limit: %s Mb" % max_ram_IAD)
print ("    Total IAD Server RAM used: %s Mb" % total_ram_IAD)
print ("    Total percent of RAM used: %s percentage " % percent_ram_used_IAD)

cslimits_ord = cs_ord.limits.get()
  # Convert the generator to a list
cslimits_ord_list = [rate for rate in cslimits_ord.absolute]
  # Pull out max_ram api limit and total used ram from list
max_ram_ord = [x.value for x in cslimits_ord_list if x.name == "maxTotalRAMSize"][0]
total_ram_ord = [x.value for x in cslimits_ord_list if x.name == "totalRAMUsed"][0]
#Get the percent ram used and round it up for clean output
percent_ram_ord = (float(total_ram_ord) / float(max_ram_ord)) * 100
percent_ram_used_ord = round(float(("%.2f" % percent_ram_ord)))

print ("Cloud Servers - ORD ")
print ("    Total RAM limit: %s Mb" % max_ram_ord)
print ("    Total ORD Server RAM used: %s Mb" % total_ram_ord)
print ("    Total percent of RAM used: %s percentage " % percent_ram_used_ord)


#IAD Cloud Block Storage Limits
headers_dfw = {'User-Agent': 'python-cinderclient','accept': 'application/json','X-Auth-Token': ("%s" % auth_token)}
r_iad = requests.get("https://iad.blockstorage.api.rackspacecloud.com/v1/%s/os-quota-sets/%s?usage=True" % (DDI, DDI), data=0, headers=headers_dfw)
data_iad = json.loads(r_iad.text)
iad_gb_SATA = data_iad['quota_set']['gigabytes_SATA']['in_use']
iad_gb_SSD = data_iad['quota_set']['gigabytes_SSD']['in_use']
iad_snapshots = data_iad['quota_set']['snapshots']['in_use']
iad_snapshots_SATA = data_iad['quota_set']['snapshots_SATA']['in_use']
iad_snapshots_SSD = data_iad['quota_set']['snapshots_SSD']['in_use']
iad_volumes = data_iad['quota_set']['volumes']['in_use']
iad_volumes_SATA = data_iad['quota_set']['volumes_SATA']['in_use']
iad_volumes_SATA_limit = data_iad['quota_set']['volumes_SATA']['limit']
iad_volumes_SSD = data_iad['quota_set']['volumes_SSD']['in_use']
iad_volumes_SSD_limit = data_iad['quota_set']['volumes_SSD']['limit']

print ("Cloud Block Storage Usage IAD: ")
print ("    SSD Volumes in use: %s" % iad_volumes_SSD)
print ("    SSD GB in use: %s" % iad_gb_SSD)
print ("    SATA Volumes in use: %s" % iad_volumes_SATA)
print ("    SATA GB in use: %s" % iad_gb_SATA)
print ("    Total Volumes in use: %s" % iad_volumes)
#print ("    Snapshots in use: %s" % iad_snapshots)
#print ("    Snapshots_SATA in use: %s" % iad_snapshots_SATA)
#print ("    Snapshots_SSD in use: %s" % iad_snapshots_SSD)
#print ("    SSD Volumes Limit: %s" % iad_volumes_SSD_limit)
#print ("    SATA Volumes Limit: %s" % iad_volumes_SATA_limit)

#ORD Cloud Block Storage Limits
headers_ord = {'User-Agent': 'python-cinderclient','accept': 'application/json','X-Auth-Token': ("%s" % auth_token)}
r_ord = requests.get("https://ord.blockstorage.api.rackspacecloud.com/v1/%s/os-quota-sets/%s?usage=True" % (DDI, DDI),data=0, headers=headers_ord)
data_ord = json.loads(r_ord.text)
ord_volumes_SSD = data_ord['quota_set']['volumes_SATA']['in_use']
ord_volumes_SSD_limit = data_ord['quota_set']['volumes_SATA']['limit']
ord_gb_SATA = data_ord['quota_set']['gigabytes_SATA']['in_use']
ord_gb_SATA_limit = data_ord['quota_set']['gigabytes_SATA']['limit']
ord_gb_SSD = data_ord['quota_set']['gigabytes_SSD']['in_use']
ord_snapshots = data_ord['quota_set']['snapshots']['in_use']
ord_snapshots_SATA = data_ord['quota_set']['snapshots_SATA']['in_use']
ord_snapshots_SSD = data_ord['quota_set']['snapshots_SSD']['in_use']
ord_volumes = data_ord['quota_set']['volumes']['in_use']
ord_volumes_SATA = data_ord['quota_set']['volumes_SATA']['in_use']
ord_volumes_SSD = data_ord['quota_set']['volumes_SSD']['in_use']

print ("Cloud Block Storage Usage ORD: ")
print ("    SSD Volumes in use: %s" % ord_volumes_SSD)
print ("    SSD GB in use: %s" % ord_gb_SSD)
print ("    SATA Volumes in use: %s" % ord_volumes_SATA)
print ("    SATA GB in use: %s" % ord_gb_SATA)
print ("    Total Volumes in use: %s" % ord_volumes)
#print ("    Snapshots in use: %s" % ord_snapshots)
#print ("    Snapshots_SATA in use: %s" % ord_snapshots_SATA)
#print ("    Snapshots_SSD in use: %s" % ord_snapshots_SSD)
#print ("    SSD Volume Limit: %s" % ord_volumes_SSD_limit)
#print ("    SATA Volume Limit: %s" % ord_gb_SATA_limit)


#IAD Cloud Loadbalancer Absolute limits
headers_lb_iad = {'accept': 'application/json','X-Auth-Token': ("%s" % auth_token)}
r_lb_iad = requests.get("https://iad.loadbalancers.api.rackspacecloud.com/v1.0/%s/loadbalancers/absolutelimits/?limit=0&offset=0" % (DDI),data=0, headers=headers_lb_iad)
r_lb_iad_count = requests.get("https://iad.loadbalancers.api.rackspacecloud.com/v1.0/%s/loadbalancers" % (DDI),data=0, headers=headers_lb_iad)
r_lb_iad_count_b = requests.get("https://iad.loadbalancers.api.rackspacecloud.com/v1.0/%s/loadbalancers?offset=100" % (DDI),data=0, headers=headers_lb_iad)
data_lb_iad = json.loads(r_lb_iad.text)
data_lb_iad_count = json.loads(r_lb_iad_count.text)
data_lb_iad_count_b = json.loads(r_lb_iad_count_b.text)
iad_lb_name = data_lb_iad_count['loadBalancers']
iad_lb_name_b = data_lb_iad_count_b['loadBalancers']
iad_count = len(iad_lb_name)
iad_count_b = len(iad_lb_name_b)
iad_total_count = iad_count + iad_count_b
iad_lb_IPV6_LIMIT = data_lb_iad['absolute'][0]['value']
iad_lb_LOADBALANCER_LIMIT = data_lb_iad['absolute'][1]['value']
iad_lb_BATCH_DELETE_LIMIT = data_lb_iad['absolute'][2]['value']
iad_lb_ACCESS_LIST_LIMIT = data_lb_iad['absolute'][3]['value']
iad_lb_NODE_LIMIT = data_lb_iad['absolute'][4]['value']
iad_lb_NODE_META_LIMIT = data_lb_iad['absolute'][5]['value']
iad_lb_LOADBALANCER_META_LIMIT = data_lb_iad['absolute'][6]['value']
iad_lb_CERTIFICATE_MAPPING_LIMIT = data_lb_iad['absolute'][7]['value']
#iad_lb_count = len(clb_list_iad)

print ("Cloud Loadbalancer Usage IAD: ")
print ("    LB Limit: %s" % iad_lb_LOADBALANCER_LIMIT)
print ("    LB Count: %s" % iad_total_count)
print ("    Node Limit: %s" % iad_lb_NODE_LIMIT)
#print ("    Node Meta Limit: %s" % iad_lb_NODE_META_LIMIT)
#print ("    LB Meta Limit: %s" % iad_lb_LOADBALANCER_META_LIMIT)
#print ("    Certificate Mapping Limit: %s" % iad_lb_CERTIFICATE_MAPPING_LIMIT)
#print ("    IPV6 Limit: %s" % iad_lb_IPV6_LIMIT)
#print ("    Batch Delete Limit: %s" % iad_lb_BATCH_DELETE_LIMIT)
#print ("    Access List Limit: %s" % iad_lb_ACCESS_LIST_LIMIT)

#ORD Cloud Loadbalancer Absolute limits
headers_lb_ord = {'accept': 'application/json','X-Auth-Token': ("%s" % auth_token)}
r_lb_ord = requests.get("https://ord.loadbalancers.api.rackspacecloud.com/v1.0/%s/loadbalancers/absolutelimits/?limit=0&offset=0" % (DDI),data=0, headers=headers_lb_ord)
r_lb_ord_count = requests.get("https://ord.loadbalancers.api.rackspacecloud.com/v1.0/%s/loadbalancers" % (DDI),data=0, headers=headers_lb_ord)
r_lb_ord_count_b = requests.get("https://ord.loadbalancers.api.rackspacecloud.com/v1.0/%s/loadbalancers?offset=100" % (DDI),data=0, headers=headers_lb_ord)
data_lb_ord = json.loads(r_lb_ord.text)
data_lb_ord_count = json.loads(r_lb_ord_count.text)
data_lb_ord_count_b = json.loads(r_lb_ord_count_b.text)
ord_lb_name = data_lb_ord_count['loadBalancers']
ord_lb_name_b = data_lb_ord_count_b['loadBalancers']
ord_count = len(ord_lb_name)
ord_count_b = len(ord_lb_name_b)
ord_total_count = ord_count + ord_count_b
ord_lb_IPV6_LIMIT = data_lb_ord['absolute'][0]['value']
ord_lb_LOADBALANCER_LIMIT = data_lb_ord['absolute'][1]['value']
ord_lb_BATCH_DELETE_LIMIT = data_lb_ord['absolute'][2]['value']
ord_lb_ACCESS_LIST_LIMIT = data_lb_ord['absolute'][3]['value']
ord_lb_NODE_LIMIT = data_lb_ord['absolute'][4]['value']
ord_lb_NODE_META_LIMIT = data_lb_ord['absolute'][5]['value']
ord_lb_LOADBALANCER_META_LIMIT = data_lb_ord['absolute'][6]['value']
ord_lb_CERTIFICATE_MAPPING_LIMIT = data_lb_ord['absolute'][7]['value']
#ord_lb_count = len(clb_list_ord)

print ("Cloud Loadbalancer Usage ORD: ")
print ("    LB Limit: %s" % ord_lb_LOADBALANCER_LIMIT)
print ("    LB Count: %s" % ord_total_count)
print ("    Node Limit: %s" % ord_lb_NODE_LIMIT)
#print ("    Node Meta Limit: %s" % ord_lb_NODE_META_LIMIT)
#print ("    Loadbalancer Meta Limit: %s" % ord_lb_LOADBALANCER_META_LIMIT)
#print ("    Certificate Mapping Limit: %s" % ord_lb_CERTIFICATE_MAPPING_LIMIT)
#print ("    IPV6 Limit: %s" % ord_lb_IPV6_LIMIT)
#print ("    LB Count: %s" % ord_lb_count)
#print ("    Batch Delete Limit: %s" % ord_lb_BATCH_DELETE_LIMIT)
#print ("    Access List Limit: %s" % ord_lb_ACCESS_LIST_LIMIT)




















