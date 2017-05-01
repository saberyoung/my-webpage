import sqlconn,util
#import htmCircle
import numpy as np
import ephem
import string
import os


def northupeastleft(data, hdr):
  if hdr['cd1_1'] > 0:
    data = np.fliplr(data)
  if hdr['cd2_2'] > 0:
    data = np.flipud(data)
  return data

################################################################################
def visibility(_ra0,_dec0,_plot=True,xx='300',yy='200'):
  import StringIO
  import matplotlib
  import string,ephem,datetime
  import numpy as np
  from matplotlib.font_manager import FontProperties
  import matplotlib.dates as mdates
  from matplotlib.ticker import MultipleLocator
  import urllib
  from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
  from matplotlib.figure import Figure
  from matplotlib.dates import DateFormatter
  import pylab as plt

  #########################################################################
  site_ll = {
      'tst' : {'latitude' : '+34.433161', 'longitude' : '-119.8631' , 'color': 'k'},
      'sqa' : {'latitude' : '+34.6924533','longitude' : '-120.0422217' , 'color': 'c'},
      'ogg' : {'latitude' : '+20.706900', 'longitude' : '-156.25800', 'color': '#3366dd'},
      'bpl' : {'latitude' : '+34.433161', 'longitude' : '-119.8631',  'DOMA' : '01.08', 'color': 'g'},
      'elp' : {'latitude' : '+30.679833', 'longitude' : '-104.015173','DOMA' : '03.10','color': '#700000'},
      'lsc' : {'latitude' : '-30.167367', 'longitude' : '-70.8049',   'DOMA' : '05.02', 'DOMB' : '10.03', 'DOMC' : '11.04', 'color': 'm'},
      'cpt' : {'latitude' : '-32.3826',   'longitude' : '+20.8124',   'DOMA' : '06.05', 'DOMB' : '07.06', 'DOMC' : '08.10', 'color': '#004f00'},
      'coj' : {'latitude' : '-31.2733',   'longitude' : '+149.438',   'DOMA' : '14.12', 'DOMB' : '02.13', 'SPARE' : '09.00','color': '#fac900' }}

 ###########################################################################
  col='brgmc'
  sun = ephem.Sun()
  star = ephem.FixedBody()
  star._ra = str(float(_ra0)/15.)
  star._dec = str(float(_dec0))
  td = datetime.timedelta(minutes=10)
  obs = ephem.Observer()       #will contain ephemeris for start time
  utnow = obs.date.datetime()  #current utdate/time
  if _plot:
    import pylab as plt
    fig=Figure()
    fig.patch.set_alpha(0.0)
#    fig.transFigure = True
    ax = fig.add_axes([.1,.15,.8,.8])
    ax.plot([utnow,utnow],[0.1,90],'r--',label='')

  ii=0
  dates1=[]
  lab={'lsc':'LSC (Chile)','elp':'ELP (Texas)','cpt':'CPT (South Africa)','coj':'COJ (Australia)','ogg':'OGG (Hawaii)'}
  for site in ['coj','ogg','cpt','elp','lsc']:
        obs = ephem.Observer()       #will contain ephemeris for start time
        moon = ephem.Moon()
        utdate = obs.date  #current utdate/time
        obs.date = utdate
        obs.lat = site_ll[site]['latitude']
        obs.long = site_ll[site]['longitude']
        sun.compute(obs)

        obs.horizon='-12'
        nextrise = obs.next_rising(sun,use_center=True)
        nextset = obs.next_setting(sun,use_center=True)

        nextriseutc= nextrise.datetime()
        nextsetutc= nextset.datetime()
        if nextsetutc > nextriseutc:
            nextsetutc=nextsetutc+datetime.timedelta(days=-1)
        date = nextsetutc
        dates,dates2=[],[]
        altitude,distance=[],[]
        lha=[]
        HA=[]
        while date < nextriseutc:
            date += td
            dates.append(date)
            dates2.append(date.hour)
            obs.date = date
            moon.compute(obs)
            star.compute(obs)
            gg,tt,ll=string.split(str(ephem.separation((star.az, star.alt), (moon.az, moon.alt))),':')
            hh,mm,ss=string.split(str(star.alt),':')
            lha.append(abs((obs.sidereal_time()-star._ra)*24.0/(2.0*ephem.pi)))
##############################
            if '-' in hh:
                sign=-1
                de=0
            else:
                sign=1.
                de = (np.abs(float(hh))+(float(mm)/60.0 + float(ss)/3600.0))*sign
            altitude.append(de)
##############################
            if '-' in gg:
                sign=-1
                de1=0
            else:
                sign=1.
                de1 = (abs(float(gg))+(float(tt)/60.0 + float(ll)/3600.0))*sign
            distance.append(de1)
        dist= '%3.1f' % (np.mean(np.array(distance)))
        stringa=lab[site]    #+' (Moon dist: '+str(dist)+"$^{o}$)"
        dates1=np.array(list(dates1)+list(dates))
        altitudegood=[altitude[x] if (lha[x] <= 4.8) else None for x in range(0,len(lha))]
        altitudebad=[altitude[x] if (lha[x] > 4.8) else None for x in range(0,len(lha))]
        if _plot:
            #dd=[(i-utnow).seconds/3600. for i in dates]
            ax.plot(dates, altitudegood, '-', label=stringa, color=site_ll[site]['color'],linewidth=3)
            ax.plot(dates, altitudebad, ':', label='', color=site_ll[site]['color'])

        ii=ii+1
  if _plot:
    import pylab as plt
    # Plot airmass limit line (airmass=2)

    titlefont = FontProperties()
    titlefont.set_size(18)
    titlefont.set_family('sans-serif')
    titlefont.set_style('normal')

    ax.set_xlabel('UT',fontproperties=titlefont)
    ax.set_ylabel('Altitude',fontproperties=titlefont)
    ax.set_ylim(0.,90)
    leg=ax.legend(numpoints=1,handlelength = .4,markerscale=1.5,loc=(.02,0.05),ncol=1,fancybox=True,prop={'size':5})
    leg.get_frame().set_alpha(0)
    for label in leg.get_texts():
        label.set_fontsize(16)

    ax.xaxis.set_major_formatter( matplotlib.dates.DateFormatter('%dT%H'))
    ax.format_xdata = matplotlib.dates.DateFormatter('%d:%h')
    canvas=FigureCanvas(fig)
    pngplot = StringIO.StringIO()

    canvas.print_png(pngplot)
    pngplot = pngplot.getvalue().encode("base64")
  return urllib.quote(pngplot.rstrip('\n'))


#############################################################

def sendtrigger2(_name,_ra,_dec,expvec,nexpvec,filtervec,_utstart,_utend,username,passwd,proposal,camera='sbig',
                 _airmass=2.0,_site='', _type='NORMAL'):
    import httplib
    import urllib
    import json
    import string,re
    from datetime import datetime
    def JDnow(datenow='',verbose=False):
        import datetime
        import time
        _JD0=2455927.5
        if not datenow:
            datenow = datetime.datetime(time.gmtime().tm_year, time.gmtime().tm_mon, time.gmtime().tm_mday,
                                        time.gmtime().tm_hour, time.gmtime().tm_min, time.gmtime().tm_sec)
        _JDtoday=_JD0 + (datenow-datetime.datetime(2012, 01, 01,00,00,00)).seconds/(3600. * 24)+\
                   (datenow - datetime.datetime(2012, 01, 01,00,00,00)).days
        if verbose: print 'JD= '+str(_JDtoday)
        return _JDtoday

    if _type in ['immediate_too']:
        _type = 'TARGET_OF_OPPORTUNITY'
    elif _type in ['NORMAL']:
           _type='NORMAL'
    else:
        _type='NORMAL'

    fildic={'1m0': {'U': 'U','B': 'B','V': 'V', 'R': 'R','I': 'I',
                   'u': 'up','g': 'gp', 'r': 'rp', 'i': 'ip', 'z': 'zs',
                   'up': 'up', 'gp': 'gp', 'rp': 'rp', 'ip': 'ip', 'zs': 'zs'}}
    fildic['2m0'] = fildic['1m0']

    _inst={'sinistro': '1M0-SCICAM-SINISTRO','sbig': '1M0-SCICAM-SBIG',
           'spectral': '2M0-SCICAM-SPECTRAL','oneof': 'oneof'}
    binx={'sbig': 2,'sinistro': 1,'spectral': 2}

    if camera in ['sbig', 'sinistro', 'oneof']:
        telclass = '1m0'
    else:
        telclass = '2m0'

    if _site in ['elp', 'cpt', 'ogg', 'lsc', 'coj']:
       _location={ "telescope_class": telclass, 'site' : _site}
    else:     _location={ "telescope_class": telclass}

    if camera in ['sbig', 'sinistro', 'spectral']:
       molecules=[]
       for i in range(0,len(filtervec)):
          molecules.append({"ag_mode": "OPTIONAL", "ag_name": "", "bin_x": int(binx[camera]), "bin_y": int(binx[camera]),
                            "defocus": 0.0, "exposure_count": int(nexpvec[i]), "exposure_time": float(expvec[i]),
                            "filter": fildic[telclass][filtervec[i]], "instrument_name": _inst[camera], "priority": 1,
                            "type": "EXPOSE"})

       user_request =  {"group_id": _name,
                     "operator": "single",
                     "type": "compound_request",
                     "requests": [ { "operator": "single",
                                     "type": "compound_request",
                                     "requests": [ {
                                         "constraints": {"max_airmass": float(_airmass) },
                                         "location": _location,
                                         "molecules": molecules,
                                         "observation_note": "C#",
                                         "observation_type": _type,
                                         "type": "request",
                                         "windows": [ {"end": _utend, "start": _utstart }  ],
                                         "target": {"coordinate_system": "ICRS",
                                                    "epoch": 2000.0,
                                                    "equinox": "J2000",
                                                    "parallax": 0.0,
                                                    "proper_motion_dec": 0.0,
                                                    "proper_motion_ra": 0.0,
                                                    "ra": float(_ra),
                                                    "dec": float(_dec),
                                                    "name": _name,
                                                    "type": "SIDEREAL"}} ]}]}
    elif camera in ['oneof']:
       molecules1=[]
       for i in range(0,len(filtervec)):
          molecules1.append({"ag_mode": "OPTIONAL", "ag_name": "", "bin_x": 2, "bin_y": 2,
                            "defocus": 0.0, "exposure_count": int(nexpvec[i]), "exposure_time": float(expvec[i]),
                            "filter": fildic[telclass][filtervec[i]], "instrument_name": "SCICAM", "priority": 1,
                            "type": "EXPOSE"})

       molecules2=[]
       for i in range(0,len(filtervec)):
          molecules2.append({"ag_mode": "OPTIONAL", "ag_name": "", "bin_x": 1, "bin_y": 1,
                            "defocus": 0.0, "exposure_count": int(nexpvec[i]), "exposure_time": float(expvec[i]),
                            "filter": fildic[telclass][filtervec[i]], "instrument_name": "1M0-SCICAM-SINISTRO", "priority": 1,
                            "type": "EXPOSE"})

       user_request =  {"group_id":_name,
                     "operator": "ONEOF",
                     "type": "compound_request",
                     "requests": [ { "operator": "single",
                                     "type": "compound_request",
                                     "requests": [ {
                                         "constraints": {"max_airmass": float(_airmass) },
                                         "location": _location,
                                         "molecules": molecules1,
                                         "observation_note": "C#",
                                         "type": "request",
                                         "windows": [ {"end": _utend, "start": _utstart }  ],
                                         "target": {"coordinate_system": "ICRS",
                                                    "epoch": 2000.0,
                                                    "equinox": "J2000",
                                                    "parallax": 0.0,
                                                    "proper_motion_dec": 0.0,
                                                    "proper_motion_ra": 0.0,
                                                    "ra": float(_ra),
                                                    "dec": float(_dec),
                                                    "name": _name,
                                                    "type": "SIDEREAL"}} ]},\
                                   { "operator": "single",
                                     "type": "compound_request",
                                     "requests": [ {
                                         "constraints": {"max_airmass": float(_airmass) },
                                         "location": _location,
                                         "molecules": molecules2,
                                         "observation_note": "C#",
                                         "type": "request",
                                         "windows": [ {"end": _utend, "start": _utstart }  ],
                                         "target": {"coordinate_system": "ICRS",
                                                    "epoch": 2000.0,
                                                    "equinox": "J2000",
                                                    "parallax": 0.0,
                                                    "proper_motion_dec": 0.0,
                                                    "proper_motion_ra": 0.0,
                                                    "ra": float(_ra),
                                                    "dec": float(_dec),
                                                    "name": _name,
                                                    "type": "SIDEREAL"}} ]}]
       }

############################################################################################################

    json_user_request = json.dumps(user_request)
    params = urllib.urlencode({'username': username ,'password': passwd, 'proposal': proposal, 'request_data' : json_user_request})
#    conn = httplib.HTTPSConnection("test.lcogt.net")
    conn = httplib.HTTPSConnection("lcogt.net")
    conn.request("POST", "/observe/service/request/submit", params)
    response = conn.getresponse().read()
    print response
    python_dict = json.loads(response)
    if 'id' in python_dict:
       tracking_number = str(python_dict['id'])
       status='ok'
    elif 'error' in python_dict:
       tracking_number = str('0')
       status  = re.sub(' ','_',str(python_dict['error']))

    _start = datetime.strptime(string.split(str(_utstart),'.')[0],"20%y-%m-%d %H:%M:%S")
    _end = datetime.strptime(string.split(str(_utend),'.')[0],"20%y-%m-%d %H:%M:%S")
    input_datesub = JDnow(verbose=False)
    input_str_smjd = JDnow(_start,verbose=False)
    input_str_emjd = JDnow(_end,verbose=False)
    _seeing = 9999
    _sky = 9999
    _instrument = telclass
    priority = 1

    try:
       lineout = str(input_datesub) + ' ' + str(input_str_smjd) + ' '+str(input_str_emjd) + '   ' + str(_site)+\
                 ' ' + ','.join(filtervec)+' ' + ','.join(nexpvec) + ' ' + ','.join(expvec) + '   ' + \
                 str(_airmass) + '   '+str(proposal) + ' ' + str(username) + ' '+str(_seeing) + ' ' + str(_sky) + \
                 ' '+str(_instrument) + ' '+str(priority) + ' '+str(tracking_number) + '  0 '+str(status)
    except:
       lineout = str(input_datesub) + ' ' + str(input_str_smjd) + ' ' + str(input_str_emjd) + '   ' + str(_site) + \
                 ' ' + ','.join(filtervec) + ' ' + ','.join(nexpvec) + ' ' + ','.join(expvec) + '   ' + \
                 str(_airmass) + '   '+str(proposal) + ' ' + str(username) + ' ' + str(_seeing) + ' ' + str(_sky) + \
                 ' ' + str(_instrument) + ' ' + str(priority) + ' 0  0 '+status
    return lineout
################################################################################

def downloadsdss(_ra,_dec,_band):
    from astroquery.sdss import SDSS
    from astropy import coordinates as coords
    import astropy.units as u
    import os
    import numpy as np
    print _ra,_dec
    pos = coords.SkyCoord(ra=float(_ra)*u.deg,dec=float(_dec)*u.deg)
    print 'pos=  ',pos
    xid = SDSS.query_region(pos, spectro=False, radius=200*u.arcsec)
    print xid
    if xid:
      filevec=[]
      for run in set(xid['field']):
        xid2=xid[xid['field']==run]
        xid2.remove_rows(np.arange(1,len(xid2)))
        im = SDSS.get_images(matches=xid2, band='r')
        im[0][0].writeto(_band+'_SDSS_'+str(run)+'.fits')
        filevec.append(_band+'_SDSS_'+str(run)+'.fits')
      return filevec
    else:
      return ''

def updatedatabase(_targetid, querytype='active', _classification=1):
    from intro_to_flask import models
    from intro_to_flask.models import db
    if querytype == 'active':
        db.session.query(models.targets).filter_by(id=_targetid).update({models.targets.active:_classification})
        db.session.commit()
        return _classification
    elif querytype == 'classification':
      db.session.query(models.candidates).filter_by(id=_targetid).update({models.candidates.classificationid: _classification})
      db.session.commit()
      print _targetid, _classification
      _act = db.session.query(models.classification.classification).filter(models.classification.id==_classification)
      return str(_act[0].classification)
    elif querytype == 'classificationall':
      print  _classification,_targetid,querytype,'here'
      db.session.query(models.idcandidates).filter_by(id=_targetid).update({models.idcandidates.classificationid: _classification})
      db.session.commit()
      db.session.query(models.candidates).filter_by(targetid=_targetid).update({models.candidates.classificationid: _classification})
      db.session.commit()
      print _targetid, _classification
      _act = db.session.query(models.classification.classification).filter(models.classification.id==_classification)
      return str(_act[0].classification)
    elif querytype == 'addname':
    	_act0 = db.session.query(models.idcandidates).filter(models.idcandidates.id==_targetid)
    	if str(_act0[0].dltname):
    		return 'object has already a DLT name'
    	else:
    		newname = dlt40.nextname()
    		db.session.query(models.idcandidates).filter_by(id=_targetid).update({models.idcandidates.dltname: newname})
    		db.session.commit()
    		print _targetid, newname
    		_act = db.session.query(models.idcandidates).filter(models.idcandidates.id==_targetid)
    		return str(_act[0].dltname)


#################################################################################

def plot_phot(targid, width=450, height=250, magtype='fluxmag'):
 import random
 # Get the data string:
 lcdata, mint, maxt, minmag, maxmag = ('[ {label: "1m0-10 rp",  points: {show: true, fill: true, fillColor: "red", type: "o", radius: 2, errorbars: "y", yerr: {show:true, upperCap: "-", lowerCap: "-", radius: 2} },  color: "red",  data: [ [-516.076604258, -4.8055, 0.016], [-516.080265693, -4.807, 0.015] ] } ]', -516.0806318368763, -516.0762381147593, -4.807, -4.8055)

 if lcdata == '':
     line = '''<span style="font-family: 'Open Sans', sans-serif; font-weight:400; font-size:14; color:black;">No photometry to display</span>'''
     return line
 # Make the flot plot:
 r = random.randrange(0, 10001)
 line = '''<div id="lcplot%s%s%s" style="width:%spx;height:%spx"></div>''' %(targid, magtype, str(r), str(width), str(height))
 line=line+ '''<script id="source_phot" language="javascript" type="text/javascript">'''
 line=line+ '''function negformat(val, axis) {
            return val.toFixed(axis.tickDecimals);
          };'''

 line=line+ '''$(function () {
          var lcplot = $("#lcplot%s%s%s");
          var xlabel = '<div style="position:absolute;left:%spx;bottom:5px;color:#666;font-family: \\'Open Sans\\', sans-serif; font-weight:400; font-size:12">Days Ago</div>';
          var options = {
                 series: {
                    lines: { show: false },
                    shadowSize: 0
                 },
                 legend: { show: false },
                 xaxis: {
                    font: {size: 12, weight: "400", family: "'Open Sans', sans-serif"},
                    color: '#666',
                    tickColor: '#DCDCDC',
                    tickFormatter:negformat,
                    autoscaleMargin: 0.02,
                    reversed: true ,
	            labelHeight: 35,
                    min: %s,
                    max: %s
                 },
                 yaxis: {
                    font: {size: 12, weight: "400", family: "'Open Sans', sans-serif"},
                    color: '#666',
                    tickColor: '#DCDCDC',
		    tickFormatter:negformat,
                    transform: function (v) { return -v; },
                    inverseTransform: function (v) { return -v; },
                    reversed: true ,
                    min: %s,
                    max: %s,
                    position: "left"
                 },
                 selection: { mode: "xy" },
                 grid: { hoverable: true, borderWidth: 1 }
                };
          ''' % (targid, magtype, r, width/2-20,str(mint), str(maxt), str(minmag), str(maxmag))

 line=line+ '''function plotSelected() {
          var data = %s;
          var plot = $.plot(lcplot, data,
                     $.extend(true, {}, options, {})
                     )
  	  lcplot.append(xlabel);
	  return plot;
          }
          var plot = plotSelected();
      ''' %lcdata

 line=line+ ''' // tooltips
          function showChartTooltip(x, y, contents) {
              $('<div id="charttooltip%s%s%s">' + contents + '</div>').css( {
                  position: 'absolute',
                  display: 'None',
                  top: y + 5,
                  left: x + 5,
                  border: '1px solid #fdd',
                  padding: '2px',
                  'background-color': '#fee',
                  opacity: 0.8
              }).appendTo("body").fadeIn(200);
          }
          var previousPoint = null;
          $("#lcplot%s%s%s").bind("plothover", function (event, pos, item) {
              $("#x").text(pos.x.toFixed(2));
              $("#y").text(pos.y.toFixed(2));
              if (item) {
                  if (previousPoint != item.datapoint) {
                      previousPoint = item.datapoint;
                      $("#charttooltip%s%s%s").remove();
                      var x = item.datapoint[0].toFixed(2),
                          y = item.datapoint[1].toFixed(2);
                      showChartTooltip(item.pageX, item.pageY, "<span style=\\"font-family: 'Open Sans', sans-serif; font-weight:400; font-size:12; color:black;\\"> mag: " + y + " (" + -x + " days ago) <br> " + item.series.label + "</span>");
                  }
              }
              else {
                  $("#charttooltip%s%s%s").remove();
                  previousPoint = null;
              }
          });''' %(targid, magtype, r, targid, magtype, r, targid, magtype, r, targid, magtype, r)

 line=line+ '''
       // zooming
       lcplot.bind("plotselected", function (event, ranges) {
           var data = %s;
           plot = $.plot(lcplot, data,
                  $.extend(true, {}, options, {
                        xaxis: { min: ranges.xaxis.from, max: ranges.xaxis.to },
			yaxis: { min: ranges.yaxis.from, max: ranges.yaxis.to }
      			})
           )
           lcplot.append(xlabel);
           // zooming reset button:
           $("<div style='right:10px; top:7px; font-family:\\"Open Sans\\",sans-serif; font-weight:400; font-size:12; color:black; position:absolute; cursor:pointer'>[reset]</div>")
           .appendTo(lcplot)
           .click(function () {
              plot.getOptions().xaxes[0].min = %s;
              plot.getOptions().xaxes[0].max = %s;
              plot.getOptions().yaxes[0].min = %s;
              plot.getOptions().yaxes[0].max = %s;
              plot.setupGrid();
              plot.draw();
           });
       });
 ''' % (lcdata,mint, maxt, minmag, maxmag)

 line=line+ '''
       // zooming reset button
       $("<div style='right:10px; top:7px; font-family:\\"Open Sans\\",sans-serif; font-weight:400; font-size:12; color:black; position:absolute; cursor:pointer'>[reset]</div>")
           .appendTo(lcplot)
           .click(function () {
              plot.getOptions().xaxes[0].min = %s;
              plot.getOptions().xaxes[0].max = %s;
              plot.getOptions().yaxes[0].min = %s;
              plot.getOptions().yaxes[0].max = %s;
              plot.setupGrid();
              plot.draw();
           });
       ''' %(mint, maxt, minmag, maxmag)
 line=line+ '''}); '''
 line=line+ '''</script> '''
 return line

###########################################################################


def fastpng(candidateid,width=300, grow=1,sigma=4, image='diff'):
    import dlt40
    import os
    import re
    from PIL import ImageDraw
    import urllib
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    import StringIO
    import cStringIO
    from astropy.io import fits as pyfits
    from scipy.misc import toimage

    done = False
    command = ['select * from candidates where id = '+str(candidateid)]
    lista = dlt40.query(command,dlt40.conn)
    if len(lista):
        filename=lista[0]['filename']
        if image=='ref':
            filename = re.sub("diff","ref",filename)
        elif image=='tar':
            filename = re.sub("diff.","",filename)

        path = lista[0]['filepath']
        xPix = int(lista[0]['xpos'])
        yPix = int(lista[0]['ypos'])
        if os.path.isfile(path+filename):
          done = True

    if done:
        hdulist = pyfits.open(path+filename)
        data = hdulist[0].data
        hdr  = hdulist[0].header
        cd1 = hdr['cd1_1']
        cd2 = hdr['cd2_2']

        x1 = max(xPix-width,0)
        x2 = min(xPix+width,1024)
        if x1 == 0:
            x2 = width*2
        if x2 == 1024:
            x1= 1024 - width*2

        y1 = max(yPix-width,0)
        y2 = min(yPix+width,1024)

        if y1 == 0:
            y2 = width*2
        if y2 == 1024:
            y1= 1024 - width*2

        if cd1 < 0:
            tx = xPix - x1
        else:
            tx = 2*width - (xPix - x1)

        ty = yPix - y1
        if cd2 < 0:
            ty = yPix - y1
        else:
            ty = 2*width - (yPix - y1)

        print tx,ty

        YY = data[y1:y2,x1:x2] 
        YY = northupeastleft(YY, hdr)
        _z1,_z2 = dlt40.zscale(YY)

        im = toimage(YY, cmin=_z1, cmax=_z2*sigma)
        draw = ImageDraw.Draw(im)

        cor = (tx+8,ty,tx+28,ty)
        draw.line(cor,width = 3, fill='white')
        cor = (tx,ty+8,tx,ty+28)
        draw.line(cor,width = 3, fill='white')

        pngplot = StringIO.StringIO()
        im.save(pngplot, 'PNG')
        pngplot.seek(0)
        line = pngplot.getvalue().encode("base64")
        pngplot.close()
        return urllib.quote(line.rstrip('\n'))
    else:
        return 

#############################################################################################

def fastpngframe(candidateid,name,width=1000, grow=1,sigma=4, line=True):
    import dlt40
    import os
    import re
    from PIL import ImageDraw
    import urllib
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    import StringIO
    import cStringIO
    from astropy.io import fits as pyfits
    from scipy.misc import toimage

    done = False
    if name:
      if '.ref' in name:
        name0 = re.sub('.ref','',name)
      else:
        name0 = name

      command = ['select * from dataraw where filename = "'+str(name0)+'"']
      lista = dlt40.query(command,dlt40.conn)
      if len(lista):
        filename = name
        path = lista[0]['filepath']
        if os.path.isfile(path+filename):   done = True
    elif candidateid:
      command = ['select * from dataraw where id = '+str(candidateid)]
      lista = dlt40.query(command,dlt40.conn)
      if len(lista):
        filename=lista[0]['filename']
        path = lista[0]['filepath']
        if os.path.isfile(path+filename):   done = True

    if width >= 512:
       width = 512

    if done:
        hdulist = pyfits.open(path+filename)
        data = hdulist[0].data
        hdr  = hdulist[0].header

        xPix = int(512)
        yPix = int(512)

        x1 = max(xPix-width,0)
        x2 = min(xPix+width,1024)

        if x1 == 0:
            x2 = width*2
        if x2 == 1024:
            x1= 1024 - width*2

        y1 = max(yPix-width,0)
        y2 = min(yPix+width,1024)

        if y1 == 0:
            y2 = width*2
        if y2 == 1024:
            y1= 1024 - width*2

        data = northupeastleft(data, hdr)

        _z1,_z2 = dlt40.zscale(data[y1:y2,x1:x2])
        im = toimage(data[y1:y2,x1:x2], cmin=_z1, cmax=_z2*sigma)
        draw = ImageDraw.Draw(im)

        xoff = -0.5
        yoff = 1.0
        ny = 1024
        x = int(round((xPix + xoff - max([0, x1]))))
        y = int(round((min([y2, ny]) - yPix + yoff)))

        if line:
          #        draw=ImageDraw.Draw(im)
          draw.line((x,y+7,x,y+25), fill='white')
          draw.line((x-7,y,x-25,y), fill='white')

        pngplot = StringIO.StringIO()
        im.save(pngplot, 'PNG')
        pngplot.seek(0)
        line = pngplot.getvalue().encode("base64")
        pngplot.close()
        return urllib.quote(line.rstrip('\n'))
    else:
        return

#############################################################################################
from math import ceil

class Pagination(object):

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in xrange(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
               num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num


def getid(_ra0,_dec0,arcsec = 2,table='idsources'):
  cx,cy,cz,htm = dlt40.dlt40sql.coordinateident(_ra0,_dec0,lev=16)
  line = htmCircle.htmCircleRegion(16, _ra0, _dec0, arcsec)
  line2=' AND (cx * '+str(cx)+' +  cy * '+str(cy)+' + cz * '+str(cz)+' >= cos('+str(np.radians(arcsec/3600.))+') )'
  command=['select id from '+table+' '+line+' '+line2+' ']
  aa = dlt40.query(command, dlt40.conn)
  if len(aa)>=1:
    _id = aa[0]['id']
  else:
    _id=''
  return _id

#######################################################

def ecliptic(_ra,_dec):
    """
    returning ecliptic and galactic coordinates in degree
    input in hours
    """
    obj = ephem.Equatorial(_ra,_dec)
    ecl = ephem.Ecliptic(obj)
    gal = ephem.Galactic(obj)

    xx = float(string.split(str(ecl.lon),':')[1])/60+\
         float(string.split(str(ecl.lon),':')[2])/3600+\
         float(string.split(str(ecl.lon),':')[0])
    if float(string.split(str(ecl.lat),':')[0])>=0:
        yy = float(string.split(str(ecl.lat),':')[1])/60+\
             float(string.split(str(ecl.lat),':')[2])/3600+\
             float(string.split(str(ecl.lat),':')[0])
    else:
        yy =  float(string.split(str(ecl.lat),':')[0])-\
              float(string.split(str(ecl.lat),':')[1])/60-\
              float(string.split(str(ecl.lat),':')[2])/3600

    xx0 = float(string.split(str(gal.lon),':')[1])/60.+\
          float(string.split(str(gal.lon),':')[2])/3600.+\
          float(string.split(str(gal.lon),':')[0])
    if float(string.split(str(gal.lat),':')[0])>=0:
        yy0 = float(string.split(str(gal.lat),':')[1])/60+\
              float(string.split(str(gal.lat),':')[2])/3600+\
              float(string.split(str(gal.lat),':')[0]) 
    else:
        yy0 = float(string.split(str(gal.lat),':')[0])-\
              float(string.split(str(gal.lat),':')[1])/60-\
              float(string.split(str(gal.lat),':')[2])/3600
    return xx,yy, xx0,yy0

##############################################################

def findlimits(targetid,days):
  line = '/dark/hal/bin/findlimit.py '+ targetid + ' ' + days
  os.system(line)
