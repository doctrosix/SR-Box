Welcome to teleporting chests

1. `git clone https://github.com/doctrosix/SR-Box`
2. Copy `server.list.example` to `server.list` and update with your server RCON parameters. Assign each server in your teleport network a unique integer ID
3. In one shell, run `while true; do ./findcombis.py; sleep 5; done`
4. In another shell, run `while true; do ./executeteleports.py; sleep .1; done`
5. In game, now you can set up a steel chest with an adjacent constant combinator with the following signals: `{S OR R}` for Send or Receive AND `I`. The value of `S` or `R` represents the send or receive channel. The value of `I` is the teleport network server ID you are sending to or receiving from. For example, Server 16 can send to server 27 by making a steel chest on server 16 with a combinator adjacent to it with value `S=44` and `I=27`. On Server 27, we make a steel chest with combinator adjacent to it with `R=44` and `I=16`. Matches are done on a first come first serve basis using `find_entities_filtered`.
6. ???
7. Profit.