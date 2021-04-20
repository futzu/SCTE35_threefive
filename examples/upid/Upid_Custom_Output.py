import threefive

"""
tons of segmentation upid examples
"""

adid = (
    "/DA4AAAAAAAA///wBQb+AAAAAAAiAiBDVUVJAAAAA3//AAApPWwDDEFCQ0QwMTIzNDU2SBAAAGgCL9A="
)
umid = "/DBHAAAAAAAA///wBQb+AAAAAAAxAi9DVUVJAAAAA3+/BCAGCis0AQEBBQEBDSATAAAA0skDbI8ZU0OrcBTS1xi/2hEAAPUV9+0="
isan = (
    "/DA4AAAAAAAA///wBQb+AAAAAAAiAiBDVUVJAAAABn//AAApPWwGDAAAAAA6jQAAAAAAABAAAPaArb4="
)
tid2 = "/DAzAAAAAAAA///wBQb+AAAAAAAdAhtDVUVJAAAAA3+/BwxNVjAwMDQxNDY0MDARAAB2a6fC"
airid = "/DBhAAAAAAAA///wBQb+qM1E7QBLAhdDVUVJSAAArX+fCAgAAAAALLLXnTUCAAIXQ1VFSUgAACZ/nwgIAAAAACyy150RAAACF0NVRUlIAAAnf58ICAAAAAAsstezEAAAihiGnw=="
adi = "/DBEAAAAAAAA///wBQb+AFJlwAAuAixDVUVJYgAFin+/CR1TSUdOQUw6My1zUTROZ0ZUME9qUHNHNFdxVVFvdzUAAEukzlg="
eidr = (
    "/DA4AAAAAAAA///wBQb+AAAAAAAiAiBDVUVJAAAAA3//AAApPWwKDBR4+FrhALBoW4+xyBAAAGij1lQ="
)
atsc = (
    "/DA4AAAAAAAA///wBQb+AAAAAAAiAiBDVUVJAAAAA3//AAApPWwLDADx7/9odW1hbjAxMhAAALdaWG4="
)
airid_mpu = "/DCSAAAAAAAAAP/wBQb/RgeVUgB8AhdDVUVJbs6+VX+/CAgAAAAABy0IxzELGQIXQ1VFSW7MmIh/vwgIAAABGDayFhE3AQECHENVRUluzw0If/8AABvLoAgIAAAAAActVhIwDBkCKkNVRUluzw02f78MG1JUTE4xSAEAAAAAMTM3NjkyMDI1NDQ5NUgxAAEAAGnbuXg="
mid = "/DA9AAAAAAAAAACABQb+0fha8wAnAiVDVUVJSAAAv3/PAAD4+mMNEQ4FTEEzMDkICAAAAAAuU4SBNAAAPIaCPw=="
ads2 = "/DBUAAAAAAAA///wBQb+AAAAAAA+AjxDVUVJAAAAC3+/Di1BRFMtVVBJRDphYTg1YmJiNi01YzQzLTRiNmEtYmViYi1lZTNiMTNlYjc5OTkRAACV15uV"
uri = "/DBZAAAAAAAA///wBQb+AAAAAABDAkFDVUVJAAAACn//AAApMuAPLXVybjp1dWlkOmFhODViYmI2LTVjNDMtNGI2YS1iZWJiLWVlM2IxM2ViNzk5ORAAAFz7UQA="

dmesg = [adid, umid, isan, tid2, airid, adi, eidr, atsc, airid_mpu, mid, ads2, uri]

ids = []


def stuff(t, upid):
    if t not in ids:
        ids.append(t)
        print(f"\033[92m{hex(t)}\033[0m : {upid}")


for m in dmesg:
    tf = threefive.Cue(m)
    tf.decode()
    tf.encode()
    [stuff(d.segmentation_upid_type, d.segmentation_upid) for d in tf.descriptors]
