Welcome to SR-Box

Send-Recieve-Box controller

This acts as a factorio game server controller that teleports chest contents from one server to another
WORK IN PROGRESS

You need a minimum of 3 computers (or VMs) to make this work.
one SR-Box controller, and two (or more) game servers.
We're still working out the limits of how much material, and servers a single controller can handle.

Goals: create Cross-server teleport chests without any player mods necessary.
Inspiration: Clusterio, Gridlock
Thanks to: The Python RCON library guy.

Credits:
    Buddy Moore         Coding
    Truman Kilen        Sysadmin
    Mario Hernandez     Sysadmin

1. `git clone https://github.com/doctrosix/SR-Box.git`
2. Copy `server.list.example` to `server.list` and update with your server RCON parameters. Assign each server in your teleport network a unique integer ID
3. In one shell, run `while true; do timeout 10 ./findcombis.py <SERVERID1>; sleep 5; done`
3. In another shell, run `while true; do timeout 10 ./findcombis.py <SERVERID2>; sleep 5; done`
4. In another shell, run `./executeteleports.py`
5. In game, now you can set up a steel chest with an adjacent constant combinator with the following signals: `{S OR R}` for Send or Receive AND `I`. The value of `S` or `R` represents the send or receive channel. The value of `I` is the teleport network server ID you are sending to or receiving from. For example, Server 16 can send to server 27 by making a steel chest on server 16 with a combinator adjacent to it with value `S=44` and `I=27`. On Server 27, we make a steel chest with combinator adjacent to it with `R=44` and `I=16`. Matches are done on a first come first serve basis using `find_entities_filtered`.
6. ???
7. Profit.

Next steps:
    -Optimize code for less reconnects
    -Burn testing to find rough mass-teleport limits
    -cross-server transaction confirmation
    -Add security, and SSH tunnels. all RCON traffic is currently plain text.
