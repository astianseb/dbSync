#!/bin/bash
#initialize DB
#cat dbinit.sql | sqlite3 rtrconfig.db
sqlite3 rtrconfig.db "DROP TABLE IF EXISTS ip_to_mac;"
sqlite3 rtrconfig.db "CREATE TABLE ip_to_mac(
        kom_type TEXT,
        pool_name TEXT,
        ip_address TEXT,
        mac_address TEXT,
        istaken TEXT
);"

for j in {1..2}; do
  if [ $j -eq 1 ]; then
    kom_type="KOM-A"
    octet="0"
 else
    kom_type="KOM-B"
    octet="5"
 fi
 for i in {5..230}; do
      sqlite3 rtrconfig.db "INSERT INTO ip_to_mac (kom_type, ip_address, istaken) VALUES (\"$kom_type\",\"192.168.$octet.$i\",\"N\")"
    done
done
