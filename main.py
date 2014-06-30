#!/usr/bin/env python2

from os import path
import numpy as np
import time
import subprocess

import cortex

######### CONFIG START
dbg_mode = False
defsz = (960, 540) #(1920, 1080)
delay_before_start = 30
port = 22648
fps = 30
bitrate = '2000k'
fnamepre = 'brainmovie'

fnamepattern='%s%%07d.png' % (fnamepre)

eg_datafile = path.join('data', 'S1_retinotopy.hdf')
######### CONFIG END

print 'opening eg file (%s)...'%(eg_datafile)
egds = cortex.openFile(eg_datafile)
print '...done'

#print 'quickshow random'
#im = cortex.quickshow((np.random.randn(31, 100, 100), "S1", "fullhead"))

print 'webshow, setting up server...'
js_handle = cortex.webgl.show(egds, port=port, open_browser=False)
print '...done'

print 'getting client... open a web browser to localhost:%d'%(port)
js_client = js_handle.get_client() #this will block until a browser has opened
# Start with left hemisphere view
#js_client._set_view(azimuth=[90],altitude=[90.5],mix=[0])
js_client.setState('labels', False)
#js_client.setState('alpha', 0)
#TODO: can't access the dataAlpha parameter through this python interface
# to turn off data overlay...
print '...done'

# Initialize list
# Append key frames for rotation and flattening
# first rotate through certain angles,
# then flatten from fidicial through inflated to flat
animation = []
if not dbg_mode:
	for az,idx in zip([90,180,270],[0,1.0,2.0]):
		animation.append({'state':'azimuth','idx':idx,'value':[az]})
	for az,idx in zip([0,0.5,1.0],[2.0,3.0,4.0]):
		animation.append({'state':'mix','idx':idx,'value':[az]})
else:
	for az,idx in zip([90,180,200],[0,0.1,0.2]):
		animation.append({'state':'azimuth','idx':idx,'value':[az]})
	for az,idx in zip([0,0.5,1.0],[0.2,0.3,0.4]):
		animation.append({'state':'mix','idx':idx,'value':[az]})

tosleep=delay_before_start if not dbg_mode else 1
print 'sleeping %d seconds'%(tosleep)
print 'if you want to adjust properties in the web interface, do it now!'
while tosleep > 0:
	time.sleep(1)
	tosleep-=1
	print '%d seconds remaining...'%(tosleep)

sz=defsz
print 'making animation with size %s...' %(str(sz))

# Animate! (use default settings)
js_client.makeMovie(animation, filename=fnamepattern, size=sz, fps=fps)
print '...done'

encoding_command = ['ffmpeg',
	#'-s %dx%d'%(sz[0],sz[1]),
	'-r',
	'%d'%(fps),
	'-i',
	'%s'%(fnamepattern),
	'-r',
	'%d'%(fps),
	'-b:v',
	'%s'%(bitrate),
	'%s.avi'%(fnamepre)]

print 'converting to movie with ffmpeg...'
retcode = subprocess.call(encoding_command)
print '...done'

print 'finished.'
