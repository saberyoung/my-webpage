from intro_to_flask import app
#from flask.ext.sqlalchemy import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash 
from flask_user import login_required, UserManager, UserMixin, SQLAlchemyAdapter
from sqlalchemy.dialects.mysql import DOUBLE

db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    # User authentication information
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')
    reset_password_token = db.Column(db.String(100), nullable=False, server_default='')

    # User email information
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())

    # User information
    active = db.Column('is_active', db.Integer, nullable=False, server_default='0')
    first_name = db.Column(db.String(100), nullable=False, server_default='')
    last_name = db.Column(db.String(100), nullable=False, server_default='')



class User2(db.Model):
  __tablename__ = 'users2'
  uid = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(120), unique=True)
  pwdhash = db.Column(db.String(54))
   
  def __init__(self, firstname, lastname, email, password):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password)
     
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)
   
  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)
    
 
class galaxies(db.Model):
  from sqlalchemy.dialects.mysql import DOUBLE
  __tablename__ = 'galaxies'
  nid = db.Column(db.BigInteger, primary_key = True)
  RAJ2000 = db.Column(DOUBLE)
  DEJ2000 = db.Column(DOUBLE)
  Kcmag = db.Column(DOUBLE)
  e_Kcmag = db.Column(DOUBLE)
  cz = db.Column(DOUBLE)
  e_cz = db.Column(DOUBLE)
  dist = db.Column(DOUBLE)
  distmod = db.Column(DOUBLE)
  ipix = db.Column(DOUBLE)
  post = db.Column(DOUBLE)
  runnumber = db.Column(db.BigInteger)
  rank = db.Column(DOUBLE)
  ID = db.Column(db.Text)


class obslog(db.Model):
  from sqlalchemy.dialects.mysql import DOUBLE
  __tablename__ = 'obslog'
  id = db.Column(db.BigInteger, primary_key = True)
  user = db.Column(db.Text)
  targetid = db.Column(db.BigInteger)
  triggerjd = db.Column(DOUBLE)
  windowstart = db.Column(DOUBLE)
  windowend = db.Column(DOUBLE)
  filters = db.Column(db.VARCHAR(30))
  exptime = db.Column(db.VARCHAR(30))
  numexp = db.Column(db.VARCHAR(30))
  proposal = db.Column(db.VARCHAR(30))
  site = db.Column(db.VARCHAR(10))
  instrument = db.Column(db.VARCHAR(30))
  sky = db.Column(db.FLOAT)
  seeing = db.Column(db.FLOAT)
  airmass = db.Column(db.FLOAT)
  slit = db.Column(db.FLOAT)
  acqmode = db.Column(db.VARCHAR(20))
  priority = db.Column(db.Text)
  reqnumber = db.Column(db.Integer)
  tracknumber = db.Column(db.Integer)
  tarfile = db.Column(db.VARCHAR(60))
  status = db.Column(db.VARCHAR(20))


class gwgc(db.Model):
  from sqlalchemy.dialects.mysql import DOUBLE
  __tablename__ = 'gwgc'
  id = db.Column(db.BigInteger, primary_key = True)
  name = db.Column(db.Text)
  ra0 = db.Column(DOUBLE)
  dec0 = db.Column(DOUBLE)
  tt = db.Column(db.FLOAT)
  appbmag = db.Column(db.FLOAT)
  a = db.Column(db.FLOAT)
  ea = db.Column(db.FLOAT)
  b = db.Column(db.FLOAT)
  eb = db.Column(db.FLOAT)
  ba = db.Column(db.FLOAT)
  eba = db.Column(db.FLOAT)
  pa = db.Column(db.FLOAT)
  absbmag = db.Column(db.FLOAT)
  dist = db.Column(db.FLOAT)
  edist = db.Column(db.FLOAT)
  eappbmag = db.Column(db.FLOAT)
  eabsbmag = db.Column(db.FLOAT)

class referenceimages(db.Model):
  from sqlalchemy.dialects.mysql import DOUBLE
  __tablename__ = 'referenceimages'
  id = db.Column(db.BigInteger, primary_key = True)
  targetid = db.Column(db.Integer)
  filter = db.Column(db.VARCHAR(20))
  filename = db.Column(db.VARCHAR(50))


class candidates(db.Model):
  from sqlalchemy.dialects.mysql import DOUBLE
  __tablename__ = 'candidates'
  id = db.Column(db.BigInteger, primary_key = True)
  targetid = db.Column(db.BigInteger)
  filename = db.Column(db.VARCHAR(50))
  filepath = db.Column(db.VARCHAR(100))
  ra0 = db.Column(DOUBLE)
  dec0 = db.Column(DOUBLE)
  xpos = db.Column(db.FLOAT)
  ypos = db.Column(db.FLOAT)
  magauto = db.Column(db.FLOAT)
  magautoerr = db.Column(db.FLOAT)
  classstar = db.Column(db.FLOAT)
  fluxrad = db.Column(db.FLOAT)
  fluxauto = db.Column(db.FLOAT)
  fluxautoerr = db.Column(db.FLOAT)
  ellipticity = db.Column(db.FLOAT)
  fwhm = db.Column(db.FLOAT)
  bkg = db.Column(db.FLOAT)
  fluxmax = db.Column(db.FLOAT)
  classificationid = db.Column(db.Integer)
  jd = db.Column(db.FLOAT)
  magabs = db.Column(db.FLOAT)
  score = db.Column(db.FLOAT)
  fakecandidateid = db.Column(db.Integer)
  magtype = db.Column(db.Integer)
  limmag = db.Column(db.FLOAT)

class sources(db.Model):
  from sqlalchemy.dialects.mysql import DOUBLE
  __tablename__ = 'sources'
  id = db.Column(db.BigInteger, primary_key = True)
  targetid = db.Column(db.BigInteger)
  filename = db.Column(db.VARCHAR(50))
  filepath = db.Column(db.VARCHAR(100))
  ra0 = db.Column(DOUBLE)
  dec0 = db.Column(DOUBLE)
  xpos = db.Column(db.FLOAT)
  ypos = db.Column(db.FLOAT)
  magauto = db.Column(db.FLOAT)
  magautoerr = db.Column(db.FLOAT)
  classstar = db.Column(db.FLOAT)
  fluxrad = db.Column(db.FLOAT)
  fluxauto = db.Column(db.FLOAT)
  fluxautoerr = db.Column(db.FLOAT)
  ellipticity = db.Column(db.FLOAT)
  fwhm = db.Column(db.FLOAT)
  bkg = db.Column(db.FLOAT)
  fluxmax = db.Column(db.FLOAT)
  classificationid = db.Column(db.Integer)
  jd = db.Column(db.FLOAT)
  magabs = db.Column(db.FLOAT)
  score = db.Column(db.FLOAT)
  fakecandidateid = db.Column(db.Integer)
  magtype = db.Column(db.Integer)
  limmag = db.Column(db.FLOAT)

class TNS(db.Model):
  from sqlalchemy.dialects.mysql import DOUBLE
  __tablename__ = 'TNS'
  id = db.Column(db.BigInteger, primary_key = True)
  ra0 = db.Column(DOUBLE)
  dec0 = db.Column(DOUBLE)
  objectname = db.Column(db.Text)


class idcandidates(db.Model):
  from sqlalchemy.dialects.mysql import DOUBLE
  __tablename__ = 'idcandidates'
  id = db.Column(db.BigInteger, primary_key = True)
  ra0 = db.Column(DOUBLE)
  dec0 = db.Column(DOUBLE)
  classificationid = db.Column(db.Integer)
  tnsid = db.Column(db.Integer)
  tnsname = db.Column(db.Text)
  dltname = db.Column(db.Text)
  
class dataraw(db.Model):
  from sqlalchemy.dialects.mysql import DOUBLE
  __tablename__ = 'dataraw'
  id = db.Column(db.BigInteger, primary_key = True)
  targetid = db.Column(db.BigInteger)
  filename = db.Column(db.VARCHAR(50))
  filepath = db.Column(db.VARCHAR(100))
  ra0 = db.Column(DOUBLE)
  dec0 = db.Column(DOUBLE)
  object = db.Column(db.VARCHAR(50))
  jd = db.Column(DOUBLE)
  exptime = db.Column(db.FLOAT)
  filter = db.Column(db.VARCHAR(20))
  telescope = db.Column(db.VARCHAR(20))
  instrument = db.Column(db.VARCHAR(20))
  airmass = db.Column(db.FLOAT)
  filetype = db.Column(db.Integer)
  quality = db.Column(db.Integer)
  wcs = db.Column(db.Integer)
  psf = db.Column(db.VARCHAR(50))
  diff = db.Column(db.VARCHAR(50))
  detections = db.Column(db.VARCHAR(50))
  cosmic = db.Column(db.Integer)
  obsid = db.Column(db.Integer)
  ut = db.Column(db.Time)
  dateobs = db.Column(db.DATE)
  dayobs = db.Column(db.DATE)
  ZP = db.Column(db.FLOAT)
  dZP = db.Column(db.FLOAT)
  fwhm = db.Column(db.FLOAT)
  limmag = db.Column(db.FLOAT)

class targets(db.Model):
  from sqlalchemy.dialects.mysql import DOUBLE
  __tablename__ = 'targets'
  id = db.Column(db.BigInteger, primary_key = True)
  ra0 = db.Column(DOUBLE)
  dec0 = db.Column(DOUBLE)
  active = db.Column(db.Integer)
  distance = db.Column(db.FLOAT)
  Bmagabs = db.Column(db.FLOAT)
  Kmagabs = db.Column(db.FLOAT)
  morphtype = db.Column(db.FLOAT)
  majaxis = db.Column(db.FLOAT)
  lastjd = db.Column(DOUBLE)


class targetnames(db.Model):
  from sqlalchemy.dialects.mysql import DOUBLE
  __tablename__ = 'targetnames'
  id = db.Column(db.BigInteger, primary_key = True)
  name = db.Column(db.VARCHAR(50))
  targetid = db.Column(db.BigInteger)
  active = db.Column(db.Integer)

class classification(db.Model):
  from sqlalchemy.dialects.mysql import DOUBLE
  __tablename__ = 'classification'
  id = db.Column(db.BigInteger, primary_key = True)
  classification = db.Column(db.Text)
