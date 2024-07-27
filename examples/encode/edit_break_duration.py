"""
Example of Editing a Cue.Command and re-encoding
"""

import threefive

BE64 = "/DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4AUsz1AAAAAAAKAAhDVUVJAAABNWLbowo="

cue = threefive.Cue(BE64)
cue.decode()
cue.show()
# use dot notation to access values and change them
cue.command.break_duration_ticks = cue.as_ticks(9000.0)

# Run cue.encode to generate new base64 string
print(cue.encode())

# returns
#  '/DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4Ae5igAAAAAAAKAAhDVUVJAAABNVB2fJs='


cue.show()
