from helperfunctions import DatabaseHandler
from helperfunctions import RouterDhcpConfig

def build_config_list(config_file):
    config = RouterDhcpConfig(config_file)
    config_list=[]
    for pool_name in config.get_dhcppoolname_list():
        mac_address = config.get_macaddr(pool_name)
        ip_address = config.get_ipaddr(pool_name)
        config_list.append([pool_name, mac_address, ip_address])
    return config_list
print build_config_list('config.txt')

def build_config_dict(config_file):
    config = RouterDhcpConfig(config_file)
    pool_name_list = config.get_dhcppoolname_list()
    ip_mac_list = []
    for pool_name in pool_name_list:
        mac_address = config.get_macaddr(pool_name)
        ip_address = config.get_ipaddr(pool_name)
        ip_mac_list.append([mac_address, ip_address])
    config_dict = {}
    for i in range(len(pool_name_list)):
        config_dict[pool_name_list[i]] = ip_mac_list[i]
    return config_dict
print build_config_dict('config.txt')

config_list = build_config_list('config.txt')
db = DatabaseHandler('rtrconfig.db')
for item in config_list:
    db.update(item)






