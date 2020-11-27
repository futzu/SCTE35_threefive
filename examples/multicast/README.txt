threefive is a SCTE-35 parser library, it does not support any network protocols. 
---------------------------------------------------------------------------------

This is an example of how threefive can be used to parse a multicast stream.
this is not a part of threefive, it's just an example. 

mcastc.py is an example multicast client for threefive.

mcastd.py is an example multicast local server.

The current mcast ip settings are optimized to run 
both the client and the server on the host. 

Usage:

start server:

  python3 mcastd.py video.ts
    
start client (in a new terminal):
  
  python3 mcastc.py 
  


-----------------------------------------------
If you need help with multicast, or networking, 
or streaming and the like,
consulting is what we do for a living.
-----------------------------------------------

  
  
