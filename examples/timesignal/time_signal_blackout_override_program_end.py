"""
14.6. Time_Signal – Program Blackout Override / Program End
"""


from threefive import Cue


BE64 = "/DBIAAAAAAAA///wBQb+ky44CwAyAhdDVUVJSAAACn+fCAgAAAAALKCh4xgAAAIXQ1VFSUgAAAl/nwgIAAAAACygoYoRAAC0IX6w"

three5 = Cue(BE64)
three5.decode()
three5.show()
