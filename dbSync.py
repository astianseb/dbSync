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

config_list = build_config_list('config.txt')
db = DatabaseHandler('rtrconfig.db')
#db.create_baseline_table()
#for item in config_list:
#    db.sync_table_with_list(item)
print db.get_free_ip("KOM-A")[0]
print db.get_free_ip("KOM-B")[0]






