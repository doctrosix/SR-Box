#!/usr/bin/env python3
import factorio_rcon
import os

def tp(srcsrvid, srcx, srcy, dstsrvid, dstx, dsty, srcconn, dstconn):
  try:
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
        surface = game.get_surface(1)
        fef=surface.find_entity
        dst=fef('steel-chest', {''' + dstx + ''', ''' + dsty + '''})
        local inv = dst.get_inventory(defines.inventory.chest)
        inv.sort_and_merge()
        slots = 0
        for x=1,#inv do
          if inv[x].valid_for_read then
            slots = slots + 1
          end
        end
        rcon.print(#inv-slots)
    '''

    if dstconn[0]:
      dstclient = dstconn[0]
    else:
      dstclient = factorio_rcon.RCONClient(dsthost, int(dstport), dstpass, timeout=5)
      dstconn[0] = dstclient

    availableslots = dstclient.send_command(cmd)

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
        local inv = src.get_inventory(defines.inventory.chest)
        contents = {}
        if inv.is_empty() then
          rcon.print('empty')
        else
          inv.sort_and_merge()
          types=0

          for i=1,''' + availableslots + ''' do
            if inv[i].valid_for_read then
              name=inv[i].name
              qty = inv.find_item_stack(name).count
              contents = {name=name,count=qty}
              ser = serialize_table(contents)
              rcon.print(ser)
            end
          end
        end

    '''

    rsp=''
    if srcconn[0]:
      srcclient = srcconn[0]
    else:
      srcclient = factorio_rcon.RCONClient(srchost, int(srcport), srcpass, timeout=5)
      srcconn[0] = srcclient
    rsp = srcclient.send_command(cmd) or ''

    contents = '{' + ','.join(rsp.split('\n')) + '}'

    if contents != '[empty]':
      cmd='''/silent-command
          surface = game.get_surface(1)
          fef=surface.find_entity
          dst=fef('steel-chest', {''' + dstx + ''', ''' + dsty + '''})

          contents = ''' + contents + '''

          for k,v in pairs(contents) do
            if dst.can_insert(v) then
              dst.insert(v)
              rcon.print('{' .. k .. ',' .. "'ok'}")
            else
              rcon.print('{' .. k .. ',' .. "'nofit'}")
            end
          end
      '''

      if dstconn[0]:
        dstclient = dstconn[0]
      else:
        dstclient = factorio_rcon.RCONClient(dsthost, int(dstport), dstpass, timeout=5)
        dstconn[0] = dstclient
      result = dstclient.send_command(cmd) or ''
      transferstatus = '{' + ','.join(result.split('\n')) + '}'

      cmd='''/silent-command
        fef=surface.find_entity
        src=fef('steel-chest', {''' + srcx + ''', ''' + srcy + '''})
        contents = ''' + contents + '''
        transferstatus = ''' + transferstatus + '''
        for k,v in pairs(transferstatus) do
          if v[2] == 'ok' then
            src.get_inventory(defines.inventory.chest).remove(contents[k])
          end
        end
      '''
      res = srcclient.send_command(cmd)
  except Exception as e:
    print('EXCEPTION DURING TELEPORT')
    print(e)
    srcconn[0] = None
    dstconn[0] = None


if __name__ == '__main__':
  srcsrvid = os.sys.argv[1]
  srcx = os.sys.argv[2]
  srcy = os.sys.argv[3]
  dstsrvid = os.sys.argv[4]
  dstx = os.sys.argv[5]
  dsty = os.sys.argv[6]
  tp(srcsrvid, srcx, srcy, dstsrvid, dstx, dsty, [None], [None])
