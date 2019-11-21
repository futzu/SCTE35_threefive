#!/usr/bin/env python3

import sys
import threefive 

'''
example command line tool.
''' 

try: mesg=sys.argv[1]
except: 
    print( '''
    Needs a hex or base64 string to decode.
    Try this:
        python cli.py  '/DAvAAAAAAAA///wBQb+rvF8TAAZAhdDVUVJSAAAB3+fCAgAAAAALKVslxEAAMSHai4='
        
    '''
    )
    sys.exit() 

tf=threefive.Splice
tf(mesg).show()
