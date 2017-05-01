import os,sqlconn

def mkdir(dir):
    if os.path.exists(dir):pass
    else:os.system('mkdir '+dir)

def copy(cfileb,cfilea,dir):
    if os.path.exists(dir+cfilea):pass
    else:os.system('cp '+cfileb+' '+dir+cfilea)

def db_create(trigger,username):
    if username:
        dbname="GW_"+str(trigger)+"_"+str(username)
    else:
        import random
        dbname="GW_"+str(trigger)+"_"+str(random.randint(0,999))
    command = ["CREATE TABLE `"+str(dbname)+"` (`id` int(11) unsigned NOT NULL AUTO_INCREMENT,`triggername` text,`number` int(11) DEFAULT NULL,`SN` int(11) DEFAULT NULL,`NSN` int(11) DEFAULT NULL,`other` text, PRIMARY KEY (`id`)) ENGINE=InnoDB AUTO_INCREMENT=124 DEFAULT CHARSET=latin1"]
    try:
        sqlconn.query(command,sqlconn.conn)
        return dbname
    except:
        print "Table gcn_"+str(ligoid)+" already exists, insert directly!"
        return False
