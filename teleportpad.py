#!/usr/bin/env python3
import factorio_rcon
import os

def tp(srcsrvid, srcconn):
  srchost = None
  srcport = None
  srcpass = None
  with open('server.list') as f:
    for line in f:
      if line.strip()[1] != '#':
        pieces = line.strip().split()
        if len(pieces) == 4:
          if pieces[0] == srcsrvid:
            srchost = pieces[1]
            srcport = pieces[2]
            srcpass = pieces[3]

  if not srchost or not srcport or not srcpass:
    exit(-1)

  cmd='''/silent-command 
    for k,v in pairs(game.surfaces[1].find_entities_filtered({name='character', area={{-66,-18},{-56,-8}}})) do 
      v.player.connect_to_server({address='kilen.me:6011'})
    end
  '''

  if srcconn[0]:
    srcclient = srcconn[0]
  else:
    srcclient = factorio_rcon.RCONClient(srchost, int(srcport), srcpass, timeout=5)
    srcconn[0] = srcclient

  ret = srcclient.send_command(cmd)
  #print(ret)

if __name__ == '__main__':
  srcsrvid = os.sys.argv[1]
  tp(srcsrvid, [None])
