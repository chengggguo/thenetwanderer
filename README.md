# the net wanderer
The Net Wanderer seeks to reveal the entanglement of technology, culture and ideology behind China's internet infrastructure. Cheng aims to focus his research during the fellowship on the connection between the critical network gateways in China and the infrastructure running these gateways. He intends to make use of Traceroute, a computer network diagnostic tool, which he will combine with an IP location finder. This will allow him to track specific geographic locations through each IP address it is able to display, although the authenticity of these locations may be difficult to confirm. The Net Wanderer will be exploring questions such as: Where are the geographical locations of Chinese Internet gateways? What are the invisible infrastructures taking place that enable the visible activities of society to continue?


-----
Stages of Development

1. modul test
a. by taking advanage of Roya Ensafi's(2014 version) list of Chinese gateway ip address(https://ensa.fi/active-probing/), I used a offline ip location database to sort the geo-locations.

*while testing the https api request got an ssl error on ubuntu, fixed by following https://blog.csdn.net/zr1076311296/article/details/75136612

b.install and run the active probing program to get the list of gateways' ip address. prepare for the field research.

c.a realtime tracroute program based on python3 and combining the modul a, tracing the path of gateways' geo-location in realtime.

2. unity/unreal


codes are based on python3