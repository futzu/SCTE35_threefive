"""
Example from the specification

14.2. Splice_Insert

"""

import threefive

Hex = "0xFC302F000000000000FFFFF014054800008F7FEFFE7369C02EFE0052CCF500000000000A0008435545490000013562DBA30A"
Base64 = "/DAvAAAAAAAA///wFAVIAACPf+/+c2nALv4AUsz1AAAAAAAKAAhDVUVJAAABNWLbowo="
"""
Using Hex
"""
print(f'parsing {Hex}') 
htf = threefive.Splice(Hex)
htf.show()

"""
Using Base64 auto
(output should be the same as above)
"""
print(f'parsing {Base64}')
btf = threefive.Splice(Base64)
btf.show()
