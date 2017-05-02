import sqlconn
import glob
import numpy as np
import re
import os
import string
import sys

option = '2'

if option=='1':   
#    command = ['select t.ra0,t.dec0,t.distance,t.Bmagabs,t.Kmagabs,t.ebv,t.morphtype from targets as t']
    command = ['select * from gcn']
    data = sqlconn.query(command,sqlconn.conn)
    for i in range(len(data)):
        print data[i]['name']
if option=='2':
    ascfile=glob.glob('/Users/sheng.yang/ownCloud/dlt40/gcn/gcn_*.txt')
    for ascifile in ascfile:
        name,ra,dec,dist,bmag,kmag,obs=[],[],[],[],[],[],[]
        ligoid=re.search(r'G\w\w\w\w\w\w*',str(os.path.basename(ascifile))).group(0)

        # create table
        command = ["CREATE TABLE `gcn_"+str(ligoid)+"` (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,`name` text,`ra0` int(11) DEFAULT NULL,`dec0` int(11) DEFAULT NULL,`distance` int(11) DEFAULT NULL,`kmag` int(11) DEFAULT NULL,`bmag` int(11) DEFAULT NULL,`obs_window` text,PRIMARY KEY (`id`)) ENGINE=InnoDB AUTO_INCREMENT=124 DEFAULT CHARSET=latin1"]
        try:
            sqlconn.query(command,sqlconn.conn)
        except:
            print "Table gcn_"+str(ligoid)+" already exists"
            continue
        
        test=open(ascifile).readlines()
        for n,ii in enumerate(test):
            try:
                if ii.split()[0]=='Below':nn = n+2
            except:pass
        if nn:
            for mm in range(nn,len(test)):
                
                if len(test[mm].split())==7:
                    name.append(test[mm].split()[0])
                    ra.append(test[mm].split()[1])
                    dec.append(test[mm].split()[2])
                    dist.append(test[mm].split()[3])
                    bmag.append(test[mm].split()[4])
                    kmag.append(test[mm].split()[5])
                    obs.append(test[mm].split()[6])
                    
                elif len(test[mm].split())==6:
                    name.append(test[mm].split()[0])
                    ra.append(test[mm].split()[1])
                    dec.append(test[mm].split()[2])
                    dist.append(test[mm].split()[3])
                    bmag.append(test[mm].split()[4])
                    kmag.append(test[mm].split()[5])
                else:print ligoid,' check input gcn!'
                
            for jj,kk in enumerate(ra):
                try:
                    dictionary = {
                        'ra0':ra[jj],
                        'dec0':dec[jj],
                        'name':name[jj],      
                        'distance':dist[jj],
                        'kmag':kmag[jj],
                        'bmag':bmag[jj],
                        'obs_window':obs[jj]}
                except:
                    dictionary = {
                        'ra0':ra[jj],
                        'dec0':dec[jj],
                        'name':name[jj],      
                        'distance':dist[jj],
                        'kmag':kmag[jj],
                        'bmag':bmag[jj]}
                sqlconn.insert_values(sqlconn.conn,'gcn_'+str(ligoid),dictionary)
