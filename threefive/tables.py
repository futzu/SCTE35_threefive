def not_zero(i):
    return i !=0

def gte_zero(i):
    return i >=0

def MPU():
    pass

def MID():
    pass
	
'''
Table 20 from page 58 of
https://www.scte.org/SCTEDocs/Standards/ANSI_SCTE%2035%202019r1.pdf

Restrict Group 0 – This segment is restricted for a class of devices 
defined by an out of band message that describes which devices are excluded.

Restrict Group 1 – This segment is restricted for a class of devices 
defined by an out of band message that describes which devices are excluded.  

Restrict Group 2 – This segment is restricted for a class of devices 
defined by an out of band message that describes which devices are excluded. 
'''
table20={
0x00: 'Restrict Group 0',
0x01: 'Restrict Group 1',
0x02: 'Restrict Group 2',
0x03: 'No Restrictions'}

	
table21={
0x00: [	0,None],
0x01: [	gte_zero,'User Defined'],
0x02: [	8,'ISCI'],
0x03: [	12,	'Ad-ID'],
0x04: [	32,	'UMID'],
0x05: [	8, 'ISAN'],
0x06: [	12,'ISAN'],
0x07: [	12,'TID'],
0x08: [	8,'AiringID'],
0x09: [	gte_zero,'ADI'],	
0x0A: [	12,	'EIDR'],
0x0B: [	gte_zero,'ATSC'],
0x0C: [	gte_zero,MPU],
0x0D: [	gte_zero,MID],
0x0E: [	gte_zero,'ADS Info'],
0x0F: [	gte_zero,'URI'],
0x10-0xff: [gte_zero,'Reserved']}


'''
table 22 from page 62 of 
https://www.scte.org/SCTEDocs/Standards/ANSI_SCTE%2035%202019r1.pdf
I am using the segmentation_type_id as a key.

Segmentation_type_id = [segmentation_message,
			segment_num,
			segments_expected,
			sub_segment_num,
			sub_segments_expected]
'''
table22={
0x00  : [ "Not Indicated",0,0, None,None],
0x01  : [ "Content Identification",0,0, None,None],
0x10  : [ "Program Start",1,1, None,None],
0x11  : [ "Program End",1,1, None,None],
0x12 : [ "Program Early Termination",1,1, None,None],
0x13 : [ "Program Breakaway",1,1, None,None],
0x14 : [ "Program Resumption",1,1, None,None],
0x15  : [ "Program Runover Planned",1,1, None,None],
0x16  : [ "Program RunoverUnplanned",1,1, None,None],
0x17 : [ "Program Overlap Start",1,1, None,None],
0x18  : [ "Program Blackout Override",0,0, None,None],
0x19 : [ "Program Start – In Progress",1,1, None,None],
0x20 : [ "Chapter Start",not_zero,not_zero, None,None],
0x21 : [ "Chapter End",not_zero,not_zero, None,None],
0x22 : [ "Break Start",gte_zero,gte_zero, None,None],
0x23 : [ "Break End",gte_zero,gte_zero, None,None],
0x24 : [ "Opening Credit Start",1,1, None,None],
0x25 : [ "Opening Credit End",1,1, None,None],
0x26 : [ "Closing Credit Start",1,1, None,None],
0x27 : [ "Closing Credit End",1,1, None,None],
0x30 : [ "Provider Advertisement Start",gte_zero,gte_zero, None,None],
0x31 : [ "Provider Advertisement End",gte_zero,gte_zero, None,None],
0x32 : [ "Distributor Advertisement Start",gte_zero,gte_zero, None,None],
0x33 : [ "Distributor Advertisement End",gte_zero,gte_zero, None,None],
0x34 : [ "Provider Placement Opportunity Start",gte_zero,gte_zero,gte_zero,gte_zero],
0x35 : [ "Provider Placement Opportunity End",gte_zero,gte_zero, None,None],
0x36 : [ "Distributor Placement Opportunity Start",gte_zero,gte_zero,gte_zero,gte_zero],
0x37 : [ "Distributor Placement Opportunity End",gte_zero,gte_zero, None,None],
0x38 : [ "Provider Overlay Placement Opportunity Start",gte_zero,gte_zero,gte_zero,gte_zero],
0x39 : [ "Provider Overlay Placement Opportunity End",gte_zero,gte_zero, None,None],
0x3A : [ "Distributor Overlay Placement Opportunity Start",gte_zero,gte_zero,gte_zero,gte_zero],
0x3B : [ "Distributor Overlay Placement Opportunity End",gte_zero,gte_zero, None,None],
0x40  : [ "Unscheduled Event Start",0,0, None,None],
0x41  : [ "Unscheduled Event End",0,0, None,None],
0x50  : [ "Network Start",0,0, None,None],
0x51  : [ "Network End",0,0, None,None],
0x3B : [ "Distributor Overlay Placement Opportunity End",gte_zero,gte_zero, None,None],
0x40  : [ "Unscheduled Event Start",0,0, None,None],
0x41  : [ "Unscheduled Event End",0,0, None,None],
0x50  : [ "Network Start",0,0, None,None],
0x51  : [ "Network End",0,0, None,None]}



