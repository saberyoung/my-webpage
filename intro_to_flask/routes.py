from flask import Flask, abort, make_response, render_template_string
from flask import render_template, request, session, url_for, redirect, flash, g
import sqlite3
import config
from flask_bootstrap import Bootstrap
from logging.handlers import TimedRotatingFileHandler
import logging
import numpy as np
import glob,re,os
import time
import string
import re
import random
import pylab as plt
import sqlconn,util
from datetime import datetime, timedelta
from intro_to_flask import app
from intro_to_flask.forms import ContactForm, SignupForm, SigninForm
from flask_mail import Message,Mail
from intro_to_flask.models import db, User2, User
from flask import jsonify
from sqlalchemy import func
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter
from flask import Blueprint
from flask_paginate import Pagination
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.models import Range1d
from bokeh.models import HoverTool, BoxSelectTool, BoxZoomTool, ResizeTool, ResetTool
from bokeh.embed import file_html, components
import subprocess

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

mail = Mail()

## log file
server_log = TimedRotatingFileHandler('server.log','D')
server_log.setLevel(logging.DEBUG)
server_log.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s'
))
error_log = TimedRotatingFileHandler('error.log', 'D')
error_log.setLevel(logging.DEBUG)
error_log.setFormatter(logging.Formatter(
    '%(asctime)s: %(message)s [in %(pathname)s:%(lineno)d]'
))


##############################
@app.route('/')
def index():
    return render_template('base.html')

@app.route('/aboutme',methods = ['POST','GET'])
def aboutme():
    if request.method == 'GET':
        return render_template('2half.html')
    if request.method == 'POST':
        return render_template('2half.html')

@app.route('/aboutme/cv')
def cv():
    return render_template('cv.html')

@app.route('/home')
def home():
  return render_template('home.html')

@app.route('/myaccount',methods = ['GET','POST'])
def myaccount():
    command = ['select username from users where id='+str(session['user_id'])]
    data = sqlconn.query(command,sqlconn.conn)
    username=data[0]['username']
    if request.method == 'GET':
        command = ['select * from users_information where username="'+str(username)+'"']
        data = sqlconn.query(command,sqlconn.conn)
        if not data:
            dictionary = {
                'username':str(username)}
            sqlconn.insert_values(sqlconn.conn,'users_information',dictionary)
        return render_template('myaccount.html',inlist=data)
    elif request.method == 'POST':
        command = ['delete from users_information where username ="'+str(username)+'"']
        sqlconn.query(command,sqlconn.conn)
        result = request.form
        dictionary = {
            'username':str(username),
            'gender':str(result['gender']),
            'month':str(result['month_start']),
            'year':str(result['year_start']),
            'day':str(result['day_start']),
            'location':str(result['location'])+'@'+str(result['country']),
            'email':str(result['email']),
            'zipcode':str(result['zipcode']),
            'work':str(result['work']),
            'phone':str(result['telephone'])}
        sqlconn.insert_values(sqlconn.conn,'users_information',dictionary)
        command = ['select * from users_information where username="'+str(username)+'"']
        data = sqlconn.query(command,sqlconn.conn)
        return render_template('myaccount.html',inlist=data)

@app.route('/info',methods = ['GET'])
def info():
    command = ['select username from users where id='+str(session['user_id'])]
    data = sqlconn.query(command,sqlconn.conn)
    username=data[0]['username']
    return render_template("info.html",name=username)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm() 
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('contact.html', form=form)
        else:
            msg = Message(form.subject.data, sender='saberyoung@gmail.com', recipients=['saberyoung@gmail.com'])
            msg.body = """
            From: %s <%s>
            %s
            """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)
            return render_template('contact.html', success=True)
 
    elif request.method == 'GET':
        return render_template('contact.html', form=form)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

## dlt40 pages
def showall():
    triggerlist=[]
    gcnfiles=glob.glob('/Users/sheng.yang/ownCloud/dlt40/gcn/gcn_*.txt')
    for gcn in gcnfiles:
        trigger=re.search(r'G\w\w\w\w\w\w*',str(os.path.basename(gcn))).group(0)
        triggerlist.append(trigger)
    return triggerlist

triggerlist = showall()
@app.route('/dlt40/')
def dltshow_base():
    return render_template('dlt40_base.html',tlist=triggerlist)
    
@app.route('/dlt40/<trigger>')
def dltshow(trigger):
    import sqlconn
    command = ['select * from gcn_'+str(trigger)]
    data = sqlconn.query(command,sqlconn.conn)
    result={}
    for i in range(len(data)):
        result[i]=[]
        result[i].append(data[i]['name'])
        result[i].append(data[i]['distance'])
        result[i].append(data[i]['bmag'])
        result[i].append(data[i]['kmag'])
        result[i].append(data[i]['obs_window'])
        result[i].append(data[i]['ra0'])
        result[i].append(data[i]['dec0'])
    return render_template('dlt40.html',result=result)

## grawita pages
def showall_1():
    piclist,triggerlist={},[]
    for tt in glob.glob('/Users/sheng.yang/ownCloud/grawita/gw_sy/plot_*'):
        triggerlist.append(re.search(r'plot_\w\w\w\w\w\w*',str(tt)).group(0)[-6:])
    for tt in triggerlist:
        mkdir('intro_to_flask/static/img/grawita/')
        mkdir('intro_to_flask/static/img/grawita/'+tt)
        piclist[tt]=[]
        picfiles=glob.glob('/Users/sheng.yang/ownCloud/grawita/gw_sy/plot_'+tt+'/test_img/*png')
        for pic in picfiles:
            piclist[tt].append(os.path.basename(pic))
            copy(pic,os.path.basename(pic),'intro_to_flask/static/img/grawita/'+tt+'/')
    return piclist

piclist=showall_1()

@app.route('/grawita/')
def gwshow_base():
    return render_template('grawita_base.html',piclist = piclist)

@app.route('/grawita/readme')
def gwshow_readme():
    return render_template('grawita_readme.html',piclist = piclist)

@app.route('/grawita/<trig>')
def gwshow_base1(trig):
    numtotal=len(piclist[trig[1:]])
    return render_template('grawita_base1.html',trigger = trig,num=numtotal,piclist=piclist)

@app.route('/grawita/<trig>/<int:num>',methods = ['POST', 'GET'])
def gwshow_trigger(trig,num):
    if request.method == 'GET':
        numtotal=len(piclist[trig[1:]])
        pic=piclist[trig[1:]][num]
        return render_template('grawita_trigger.html',trigger=trig,num=num,pic=pic,numtotal=numtotal)
    
    elif request.method == 'POST':
        if 'user_id' in session:
            command = ['select username from users where id='+str(session['user_id'])]
            data = sqlconn.query(command,sqlconn.conn)
            username=data[0]['username']
            dbname=db_create(str(trig),username)
        result = request.form
        no,nsn,nnsn='',0,0
        try:
            if result['sn']:
                if result['sn']=='on':nsn+=1
        except:pass        
        try:
            if result['nsn']:
                if result['nsn']=='on':nnsn+=1
        except:pass        
        try:
            if result['Other opinion']:
                no=result['Other opinion']
        except:pass
        dictionary = {
            'triggername':str(trig),
            'number':str(num),
            'SN':str(nsn),
            'NSN':str(nnsn),
            'other':str(no)}
        sqlconn.insert_values(sqlconn.conn,dbname,dictionary)
        numtotal=len(piclist[trig[1:]])
        pic=piclist[trig[1:]][num]
        return render_template('grawita_trigger.html',trigger=trig,num=num+1,pic=pic,numtotal=numtotal)

@app.route('/grawita/result/',methods = ['POST'])
def result():
    if 'user_id' in session:
        command = ['select username from users where id='+str(session['user_id'])]
        data = sqlconn.query(command,sqlconn.conn)
        username=data[0]['username']
    else:username='Nobody'
    return render_template("grawita_result.html",user = username,tlist=piclist.keys())

@app.route('/grawita/result/<user>_<trigger>')
def result1(user,trigger):
    dbname="GW_"+str(trigger)+"_"+str(user)
    command = ['select * from '+dbname]
    data = sqlconn.query(command,sqlconn.conn)
    return render_template("grawita_result1.html",result = data)

## others
@app.route('/wedding')
def wedding():
    return render_template('wedding.html')

@app.route('/wedding/chinese')
def wedding1():
    return render_template('wedding_chn.html')

@app.route('/wedding/english')
def wedding2():
    return render_template('wedding_eng.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/mail')
def mails():
    return render_template('mail.html')

@app.route('/photos')
def photos():
    return render_template('photos.html')

@app.route('/start')
def startpage():
    return render_template('startpage.html')

@app.route('/startup')
def startup():
    return render_template('startup.html')
