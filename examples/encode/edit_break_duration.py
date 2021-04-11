import threefive

b64 = "/DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4AUsz1AAAAAAAKAAhDVUVJAAABNWLbowo="

cue = threefive.Cue(b64)
cue.decode()

# break_duration is currently 60.293567

# use dot notation to access values and change them
cue.command.break_duration = 90.0

# Run cue.encode to generate new base64 string

newb64 = cue.encode()

# returns
# b'/DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4Ae5igAAAAAAAKAAhDVUVJAAABNVB2fJs='


cue.show()
