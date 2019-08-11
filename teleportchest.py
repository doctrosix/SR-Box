#!/usr/bin/env python3 
import factorio_rcon
import os

def tp(srcsrvid, srcx, srcy, dstsrvid, dstx, dsty, srcconn, dstconn):
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

  dsthost = None
  dstport = None
  dstpass = None
  with open('server.list') as f:
    for line in f:
      if line.strip()[1] != '#':
        pieces = line.strip().split()
        if len(pieces) == 4:
          if pieces[0] == dstsrvid:
            dsthost = pieces[1]
            dstport = pieces[2]
            dstpass = pieces[3]

  if not dsthost or not dstport or not dstpass:
    exit(-1)

  cmd='''/silent-command 

      function serialize_table(t)
        s='{' 
        for x,y in pairs(t) do 
          s = s .. "['" .. x .. "']" .. '=' .. "'" .. y .. "'" .. ',' 
        end 
        if #s>1 then 
          s=s:sub(1,-2) 
        end 
        s=s..'}' 

        return(s)
      end

      surface = game.get_surface(1)
      fef=surface.find_entity
      src=fef('steel-chest', {''' + srcx + ''', ''' + srcy + '''})
      inv = src.get_inventory(defines.inventory.chest)
      contents = {}
      if inv.is_empty() then 
        rcon.print('empty')
      else
        inv.sort_and_merge()
        types=0
        for k,_ in pairs(inv.get_contents()) do types = types + 1 end
        name=inv[math.random(types)].name
        qty = inv.find_item_stack(name).count
        contents = {name=name,count=qty}
        ser = serialize_table(contents)
        rcon.print(ser)
      end

  '''

  if srcconn[0]:
    srcclient = srcconn[0]
  else:
    srcclient = factorio_rcon.RCONClient(srchost, int(srcport), srcpass, timeout=5)
    srcconn[0] = srcclient
  contents = srcclient.send_command(cmd)
  summary = contents

  if contents != 'empty':
    cmd='''/silent-command 
        surface = game.get_surface(1)
        fef=surface.find_entity
        dst=fef('steel-chest', {''' + dstx + ''', ''' + dsty + '''})

        contents = ''' + contents + '''

        if dst.can_insert(contents) then
          dst.insert(contents)
          rcon.print('ok')
        else
          rcon.print('nofit')
        end
    '''

    if dstconn[0]:
      dstclient = dstconn[0]
    else:
      dstclient = factorio_rcon.RCONClient(dsthost, int(dstport), dstpass, timeout=5) 
      dstconn[0] = dstclient
    result = dstclient.send_command(cmd)
    summary = summary + ' ' + result 

    if result == 'ok':
      cmd='''/silent-command 
        contents = ''' + contents + '''
        fef=surface.find_entity
        src=fef('steel-chest', {''' + srcx + ''', ''' + srcy + '''})
        src.get_inventory(defines.inventory.chest).remove(contents)
        rcon.print('deleted')
      '''
      res = srcclient.send_command(cmd)
      summary = summary + ' ' + res
      print(summary)

if __name__ == '__main__':
  srcsrvid = os.sys.argv[1]
  srcx = os.sys.argv[2]
  srcy = os.sys.argv[3]
  dstsrvid = os.sys.argv[4]
  dstx = os.sys.argv[5]
  dsty = os.sys.argv[6]
  tp(srcsrvid, srcx, srcy, dstsrvid, dstx, dsty)
