#!/bin/bash
#initialize DB
#cat dbinit.sql | sqlite3 rtrconfig.db
sqlite3 rtrconfig.db "DROP TABLE IF EXISTS kom_a;"
sqlite3 rtrconfig.db "DROP TABLE IF EXISTS kom_b;"
sqlite3 rtrconfig.db "CREATE TABLE kom_a(
        pool_name TEXT,
        ip_address TEXT,
        mac_address TEXT,
        istaken TEXT
);"
sqlite3 rtrconfig.db "CREATE TABLE kom_b(
        pool_name TEXT,
        ip_address TEXT,
        mac_address TEXT,
        istaken TEXT
);"



for i in {5..230}; do
  sqlite3 rtrconfig.db "INSERT INTO kom_a (ip_address) VALUES (\"192.168.4.$i\")"
  sqlite3 rtrconfig.db "INSERT INTO kom_b (ip_address) VALUES (\"192.168.5.$i\")"
done

