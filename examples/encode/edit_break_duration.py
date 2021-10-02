import threefive

base_six_four = "/DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4AUsz1AAAAAAAKAAhDVUVJAAABNWLbowo="

cue = threefive.Cue(base_six_four)
cue.decode()
cue.show()
# use dot notation to access values and change them
cue.command.break_duration = 9000.0

# Run cue.encode to generate new base64 string
print(cue.encode())

# returns
# b'/DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4Ae5igAAAAAAAKAAhDVUVJAAABNVB2fJs='


cue.show()
