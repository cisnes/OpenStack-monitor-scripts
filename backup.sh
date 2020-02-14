#!/bin/bash
cd /backups
sudo su
sudo cockroach dump bf --insecure > backup.sql
exit
scp backup.sql ubuntu@192.168.132.58:
ssh ubuntu@192.168.132.58 sudo cp -n backup.sql /backup
ssh ubuntu@192.168.132.58 rm backup.sql
sudo rm backup.sql