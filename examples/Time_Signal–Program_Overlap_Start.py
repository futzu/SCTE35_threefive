"""
Example from the specification

14.5. Time_Signal–Program_Overlap_Start

"""


import threefive

Hex = "0xFC302F000000000000FFFFF00506FEAEBFFF640019021743554549480000087F9F0808000000002CA56CF5170000951DB0A8"


stuff = threefive.Splice(Hex)
stuff.show()
