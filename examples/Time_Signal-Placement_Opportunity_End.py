"""
Example from the specification

14.3. Time_Signal–Placement_Opportunity_End

"""

import threefive

Base64 = "/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g="

stuff = threefive.Splice(Base64)

stuff.show()
