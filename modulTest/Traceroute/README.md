Command: ./batch-find-router

Description: Using ip_providers configured in qiang/config.py, batch-find-router will first get a list of ip to shoot at.
For each ip, it invokes ./find-router destionation-ip to try to find GFW attached router on the path. The result
is in var/gfw-attached-routers.csv.

Command: ./find-router destination-ip

Example: ./find-router 173.252.110.27

Description: find-router command will send packet to the destination-ip you specified, but the ttl will 
change from a very low value and increase one each time. When the packet reached the router with GFW
attached, we will start to recieve "TCP RST" or "Wrong DNS Answer" due to GFW reactions. By doing this, we
can tell if there is any GFW attached router between you and the destionation ip, and what's it ip address.

Command: ./watchdog dst1 dst2 dst3 ...

Example: ./watchdog 202.106.0.20 173.252.110.27 2> /tmp/watchdog.log

Description: watchdog will run find-router against the destinations you specified. It will report if it is initially
blocked and when it is being unblocked/blocked in file var/watchdog.csv.

Blog post:

* http://fqrouter.tumblr.com/post/46561836548/gfw-qiang
* http://fqrouter.tumblr.com/post/46745599157/qiang-dns-wrong-answer-probe-py
* http://fqrouter.tumblr.com/post/46758595474/qiang-tcp-rst-probe-py

[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/fqrouter/qiang/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

