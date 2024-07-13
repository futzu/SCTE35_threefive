
# Ffmpeg rewriting SCTE-35 packets.
## As of 2.4.55, threefive can parse the packet either way.

<div> I love you msnbc, (please don't get mad at me for using your SCTE-35) </div>

<br>
<br>
<div> Let me preface this by saying this is not a criticism of ffmpeg.<br>
 In my experience, ffmpeg tends to do things the correct way, <br>
 and I have no problem adapting to them.<br>
 
My goal is to keep threefive as flexible and compatible as possible.<br>
</div>

#### This is what I usually get for SCTE-35 packets. 

* four byte header
* \x00
* SCTE-35 Cue
* padding to 188 bytes

  
![image](https://github.com/user-attachments/assets/11bb0424-725a-4701-9cc1-2d8727fede05)



`ffmpeg -i msnbc-latest.ts  -map 0 -c copy msnbc-latest-ffmpeg.ts`

#### Now ffmpeg changes that packet to look like this.

* four byte header + AFC
* padding to 188 bytes
* PES header
* SCTE-35 Cue


![image](https://github.com/user-attachments/assets/3e1b096d-bcee-4c94-980c-6e67bf5a2d7c)




## As of 2.4.55, threefive can parse the packet either way.

