import sys, threefive
'''
Fast parse mpegts for SCTE35 messages

ex.
    python3 fast_parse.py < video.ts
'''

tsdata=sys.stdin.buffer


while tsdata:
    packet=tsdata.read(188)
    if not packet: break
    if (packet[5] ==0xfc) and (packet[18] != 0):
        try:
            tf=threefive.Splice(packet[5:])
            tf.show()
        except: pass
