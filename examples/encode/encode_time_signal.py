"""
Example of Encoding a Time Signal Command from Scratch
"""
import threefive

cmd = threefive.TimeSignal()
# {'command_length': 0, 'command_type': 6, 'bites': None, 'name': 'Time Signal', 'time_specified_flag': None, 'pts_time': None}

# set the values needed
cmd.time_specified_flag = True
cmd.pts_time = 23000.677777

# Create an empty Cue
cue = threefive.Cue()

# set cue.command to the TimeSignal Command cmd
cue.command = cmd

print(cue.encode())
#  '/DAWAAAAAAAAAP/wBQb+e2KfxwAAN6nTrw=='

#  run cue.show() to check values.
cue.show()
