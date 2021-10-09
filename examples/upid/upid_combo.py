"""
Combination Segmentation Upid Example

"""


import threefive


COMBO = "/DA9AAAAAAAAAACABQb+0fha8wAnAiVDVUVJSAAAv3/PAAD4+mMNEQ4FTEEzMDkICAAAAAAuU4SBNAAAPIaCPw=="

cuep = threefive.Cue(COMBO)
cuep.decode()
cuep.show()
