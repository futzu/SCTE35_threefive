from threefive import Splice

'''
14.6. Time_Signal – Program Blackout Override / Program End 
'''

Base64='/DBIAAAAAAAA///wBQb+ky44CwAyAhdDVUVJSAAACn+fCAgAAAAALKCh4xgAAAIXQ1VFSUgAAAl/nwgIAAAAACygoYoRAAC0IX6w'

three5=Splice(Base64)
print('Info Section')
three5.show_info_section()
print('Splice Command')
three5.show_command()
print('Splice Descriptors')
three5.show_descriptors()
