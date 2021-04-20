import threefive


"""

Multiple Segmentation Upid Descriptors Example

Three AiringID and One MPU

"""

airid_mpu = "/DCSAAAAAAAAAP/wBQb/RgeVUgB8AhdDVUVJbs6+VX+/CAgAAAAABy0IxzELGQIXQ1VFSW7MmIh/vwgIAAABGDayFhE3AQECHENVRUluzw0If/8AABvLoAgIAAAAAActVhIwDBkCKkNVRUluzw02f78MG1JUTE4xSAEAAAAAMTM3NjkyMDI1NDQ5NUgxAAEAAGnbuXg="

cuep = threefive.Cue(airid_mpu)
cuep.decode()
cuep.show()
