from ciscoconfparse import CiscoConfParse
import sqlite3
import os, datetime



class DatabaseHandler():
    def __init__(self, db):
        self.conn = sqlite3.connect(db)

    def create_baseline_table(self):
        c = self.conn.cursor()
        c.execute('''DROP TABLE IF EXISTS ip_to_mac;''')
        c.execute('''CREATE TABLE ip_to_mac(
            kom_type TEXT,
            pool_name TEXT,
            ip_address TEXT,
            mac_address TEXT,
            istaken TEXT);''')
        self.conn.commit()
        for j in range(0, 2):
            if j == 0:
                kom_type = "KOM-A"
                octet = "0"
            else:
                kom_type = "KOM-B"
                octet = "5"
            for i in range(2, 240):
                ip_address = "192.168." + str(octet) + "." + str(i)
                c.execute('''
                INSERT INTO ip_to_mac (kom_type, ip_address, istaken) VALUES (?, ?, ?)
                ''', (kom_type, ip_address, "N"))
        self.conn.commit()

    def sync_table_with_list(self, list):
        self.list = list
        c = self.conn.cursor()
        c.execute(''' UPDATE ip_to_mac
                    SET pool_name = ?, mac_address = ?, istaken = ?
                    WHERE ip_address = ?
        ''', (self.list[0], self.list[1], "Y", self.list[2]))
        self.conn.commit()

    def get_free_ip(self, kom_type):
        c = self.conn.cursor()
        c.execute(''' SELECT ip_address FROM ip_to_mac
                    WHERE kom_type = ? AND istaken = "N"
                    LIMIT 1''', (kom_type,))
        free_ip = c.fetchone()
        return free_ip

class RouterDhcpConfig:
    def __init__(self, config_file):
        self.config_file = config_file
        self.parse = CiscoConfParse(self.config_file)

    def get_dhcppool_config(self, pool_name):
        find_result = self.parse.find_children(pool_name)
        return find_result

    def get_dhcppoolname_list(self):
        dhcppoolname_list = []
        find_result = self.parse.find_parents_w_child('^ip dhcp pool', 'host')
        for parent in find_result:
            dhcppoolname_list.append(parent.split()[3])
        return dhcppoolname_list

    def get_ipaddr(self, pool_name):
        find_result = self.parse.find_children(pool_name)
        return find_result[1].split()[1]

    def get_ipaddrmask(self, pool_name):
        find_result = self.parse.find_children(pool_name)
        return find_result[1].split()[2]

    def get_macaddr(self, pool_name):
        find_result = self.parse.find_children(pool_name)
        return find_result[2].split()[1]

    def get_defaultrouter(self, pool_name):
        find_result = self.parse.find_children(pool_name)
        return find_result[3].split()[1]

    def get_dns(self, pool_name):
        find_result = self.parse.find_children(pool_name)
        return [find_result[4].split()[1], find_result[4].split()[2]]