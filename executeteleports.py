#!/usr/bin/env python3

import os
import glob
import subprocess
import time
import threading
import datetime

import teleportchest

threads = {}
srcconns = {}
dstconns = {}

while True:
  for f in glob.glob('*.combis'):
    srcid = f.replace('.combis','')
    with open(f) as srctps:
      for srcl in srctps:
        s = srcl.split()
        if s[0] == 'S':
          srcx = s[5]
          srcy = s[6]
          dstsrvid = s[3]
          dstchan = s[4]
          if os.path.exists(dstsrvid + '.combis'):
            with open(dstsrvid + '.combis') as dsttps:
              for dstl in dsttps:
                d = dstl.split()
                if d[0] == 'R' and d[4] == dstchan:
                  dstx = d[5]
                  dsty = d[6]
                  key=':'.join([str(x) for x in [srcid, srcy, srcy, dstsrvid, dstx, dsty]])
                    
                  if key in threads:
                    if not threads[key][1].isAlive(): 
                      threads.pop(key)
                    else:
                      if (datetime.datetime.utcnow() - threads[key][0]).total_seconds() > 10:
                        print('STUCK: ' + key)
                        srcconns[key] = [None]
                        dstconns[key] = [None]
                        threads.pop(key)
                  else:
                    if key not in srcconns:
                      srcconns[key] = [None]
                    if key not in dstconns:
                      dstconns[key] = [None]

                    t = threading.Thread(target=teleportchest.tp,
                      args=(srcid, srcx, srcy, dstsrvid, dstx, dsty, srcconns[key], dstconns[key]))
                    threads[key] = (datetime.datetime.utcnow(), t)
                    t.start()
  time.sleep(.01)
