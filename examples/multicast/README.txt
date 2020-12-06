threefive is a SCTE-35 parser library, 
it does not directly support any network protocols. 
----------------------------------------------------
This is an example of how threefive can be used 
to parse a multicast stream.

mcastc.py is an example multicast client for threefive.

mcastd.py is an example multicast sender

The current mcast ip settings are optimized to run 
both the client and the server on one host. 

Usage:

start client first. 
  python3 mcastc.py

start server in a new terminal.

  python3 mcastd.py video.ts
    
 
The SCTE-35 cue count is printed in green to sys.stderr, to indicate the stream is being parsed. 
Nothing will be printed if the stream is not being parsed.


On UNIX/Linux speed it up by routing multicast on the loopback,
tcpdump will not be able to see the traffic.


	ifconfig lo multicast

	route add -net 224.0.0.0 netmask 240.0.0.0 dev lo 

If you want to use more than one host I suggest

Or add the route to your network device if you want to see traffic with tcpdump

	ifconfig wlp2s0 multicast allmulti

	route add -net 224.0.0.0 netmask 240.0.0.0 dev wlp2s0

OpenBSD uses slightly different syntax:

	route add -inet 224.0.0.0/4 224.0.0.1
	

Then you can monitor traffic with

	tcpdump -i wlp2s0  multicast

I'm really not sure how it works on Windows. 
