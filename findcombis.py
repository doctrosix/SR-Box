#!/usr/bin/env python3 
import factorio_rcon
import os

srvid = os.sys.argv[1]
srchost = None
srcport = None
srcpass = None
with open('server.list') as f:
  for line in f:
    if line.strip()[1] != '#':
      pieces = line.strip().split()
      if len(pieces) == 4:
        if pieces[0] == srvid:
          srchost = pieces[1]
          srcport = pieces[2]
          srcpass = pieces[3]

if not srchost or not srcport or not srcpass:
  exit(-1)

cmd='''/silent-command 
  surf = game.surfaces['nauvis']
  fef = surf.find_entities_filtered
  for k,v in pairs(fef({name='constant-combinator'})) do 
    b= v.get_control_behavior() 

    signals=0
    ival=0
    for x=1,b.signals_count do 
      s = b.get_signal(x) 
      if s.signal then 
        signals = signals + 1
        if s.signal.name == 'signal-I' then
          ival = s.count
        end
      end
    end

    if signals==2 and ival ~= 0 then
      for x=1,b.signals_count do 
        s = b.get_signal(x) 
        if s.signal then
          if s.signal.name == 'signal-R' or s.signal.name == 'signal-S' then

            pos = v.position.x .. ' ' .. v.position.y

            npos = {v.position.x, v.position.y-1}
            epos = {v.position.x+1, v.position.y}
            spos = {v.position.x, v.position.y+1}
            wpos = {v.position.x-1, v.position.y}

            nchest = fef({name='steel-chest', position=npos, radius=.1})
            echest = fef({name='steel-chest', position=epos, radius=.1})
            schest = fef({name='steel-chest', position=spos, radius=.1})
            wchest = fef({name='steel-chest', position=wpos, radius=.1})

            cpos = nil
            if #nchest > 0 then
              cpos = npos
            elseif #echest > 0 then
              cpos = epos
            elseif #schest > 0 then
              cpos = spos
            elseif #wchest > 0 then
              cpos = wpos
            end
           
            if cpos then 
              if s.signal.name == 'signal-R' then
                rcon.print('R'.. ' ' .. pos .. ' ' .. ival .. ' ' .. 
                  s.count .. ' ' .. cpos[1] .. ' ' .. cpos[2])
              end

              if s.signal.name == 'signal-S' then
                rcon.print('S'.. ' ' .. pos .. ' ' .. ival .. ' ' .. 
                  s.count .. ' ' .. cpos[1] .. ' ' .. cpos[2])
              end
            end
          end
        end
      end
    end
  end
'''

srcclient = factorio_rcon.RCONClient(srchost, int(srcport), srcpass)
contents = srcclient.send_command(cmd)
#print(contents)
print(str(srvid) + ' ')

with open(srvid + '.combis', 'w') as f:
  f.write(contents or '')
