#!/usr/bin/env python3

import glob
import subprocess
import time
import threading

import teleportchest

threads = {}

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
          with open(dstsrvid + '.combis') as dsttps:
            for dstl in dsttps:
              d = dstl.split()
              if d[0] == 'R' and d[4] == dstchan:
                dstx = d[5]
                dsty = d[6]
                key=':'.join([str(x) for x in [srcid, srcy, srcy, dstsrvid, dstx, dsty]])
                if key in threads:
                  if not threads[key].isAlive(): 
                    threads.pop(key)
                else:
                  t = threading.Thread(target=teleportchest.tp,
                    args=(srcid, srcx, srcy, dstsrvid, dstx, dsty))
                  threads[key] = t
                  t.start()
  time.sleep(.01)
