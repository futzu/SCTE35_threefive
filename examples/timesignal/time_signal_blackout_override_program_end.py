from threefive import Cue

"""
14.6. Time_Signal – Program Blackout Override / Program End 
"""

be_64 = "/DBIAAAAAAAA///wBQb+ky44CwAyAhdDVUVJSAAACn+fCAgAAAAALKCh4xgAAAIXQ1VFSUgAAAl/nwgIAAAAACygoYoRAAC0IX6w"

three5 = Cue(be_64)
three5.decode()
three5.show()
