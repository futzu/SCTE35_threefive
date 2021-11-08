#### function `threefive.decode`

```python
Help on function decode in module threefive.decode:

decode(stuff=None)
    decode is a SCTE-35 decoder function
    with input type auto-detection.
    SCTE-35 data can be parsed with just
    one function call.                                                                                                                                       
                                                                                                                                                             
    the arg stuff is the input.                                                                                                                              
    if stuff is not set, decode will attempt                                                                                                                 
    to read from sys.stdin.buffer.                                                                                                                           
                                                                                                                                                             
    if stuff is a file, the file data                                                                                                                        
    will be read and the type of the data                                                                                                                    
    will be autodetected and decoded.
    
    SCTE-35 data is printed in JSON format.
    
    For more parsing and output control,
    see the Cue and Stream classes.
    
    Supported inputs:
    
    # Base64
    
    stuff = '/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g='
    threefive.decode(stuff)
    
    # Bytes
    
    payload = b'ü0^Q^@^@^@^@^@^@^@ÿÿÿ^@^@^@O%3<U+0096>'
    threefive.decode(payload)
    
    # Hex String
    
    stuff = '0XFC301100000000000000FFFFFF0000004F253396'
    threefive.decode(stuff)

    # Hex Literal
    
    threefive.decode(0XFC301100000000000000FFFFFF0000004F253396)
    
    # Integer
    
    big_int = 1439737590925997869941740173214217318917816529814
    threefive.decode(big_int)
    
    # Mpegts File
    
    threefive.decode('/path/to/mpegts')
    
    # Mpegts HTTP/HTTPS Streams
    
    threefive.decode('https://futzu.com/xaa.ts')
```

#### class `threefive.Cue`


```python
Help on class Cue in module threefive.cue:

class Cue(threefive.base.SCTE35Base)
 |  Cue(data=None, packet_data=None)
 |  
 |  The threefive.Splice class handles parsing
 |  SCTE 35 message strings.
 |  Example usage:
 |  
 |  >>>> import threefive
 |  >>>> Base64 = "/DAvAAAAAAAA///wBQb+dGKQoAAZAhdDVUVJSAAAjn+fCAgAAAAALKChijUCAKnMZ1g="
 |  >>>> cue = threefive.Cue(Base64)
 |  
 |  # cue.decode() returns True on success,or False if decoding failed
 |  
 |  >>>> cue.decode()
 |  True
 |  
 |  # After Calling cue.decode() the instance variables can be accessed via dot notation.
 |  
 |  >>>> cue.command
 |  {'command_length': 5, 'name': 'Time Signal', 'time_specified_flag': True,
 |  'pts_time': 21695.740089}
 |  
 |  >>>> cue.command.pts_time
 |  21695.740089
 |  
 |  >>>> cue.info_section.table_id
 |  
 |  '0xfc'
 |  
 |  Method resolution order:
 |      Cue
 |      threefive.base.SCTE35Base
 |      builtins.object
 |  
 |  Methods defined here:
 |  
 |  __init__(self, data=None, packet_data=None)
 |      data may be packet bites or encoded string
 |      packet_data is a instance passed from a Stream instance
 |  
 |  decode(self)
 |      Cue.decode() parses for SCTE35 data
 |  
 |  encode(self)
 |      Cue.encode() converts SCTE35 data
 |      to a base64 encoded string.
 |  
 |  encode_as_hex(self)
 |      encode_as_hex returns self.bites as
 |      a hex string
 |  
 |  get(self)
 |      Cue.get returns the SCTE-35 Cue
 |      data as a dict of dicts.
 |  
 |  get_descriptors(self)
 |      Cue.get_descriptors returns a list of
 |      SCTE 35 splice descriptors as dicts.
 |  
 |  get_json(self)
 |      Cue.get_json returns the Cue instance
 |      data in json.
 |  
 |  load(self, stuff)
 |      Cue.load loads SCTE35 data for encoding.
 |      stuff is a dict or json
 |      with any or all of these keys
 |      stuff = {
 |          'info_section': {dict} ,
 |          'command': {dict},
 |          'descriptors': [list of {dicts}],
 |          }
|  
 |  load_command(self, cmd)
 |      load_command loads data for Cue.command
 |      cmd should be a dict.
 |      if 'command_type' is included,
 |      the command instance will be created.
 |  
 |  load_descriptors(self, dlist)
 |      Load_descriptors loads descriptor data.
 |      dlist is a list of dicts
 |      if 'tag' is included in each dict,
 |      a descriptor instance will be created.
 |  
 |  load_info_section(self, isec)
 |      load_info_section loads data for Cue.info_section
 |      isec should be a dict.
 |      if 'splice_command_type' is included,
 |      an empty command instance will be created for Cue.command
 |  
 |  mk_info_section(self, bites)
 |      Cue.mk_info_section parses the
 |      Splice Info Section
 |      of a SCTE35 cue.
 |  
 |  show(self)
 |      Cue.show prints the Cue as JSON
 |  
 |  to_stderr(self)
 |      Cue.to_stderr prints the Cue
 |      as JSON to sys.stderr
 |  
 |  ----------------------------------------------------------------------
 |  Methods inherited from threefive.base.SCTE35Base:
 |  
 |  __repr__(self)
 |  
 |  kv_clean(self)
 |      kv_clean removes items from a dict if the value is None
```

#### class `threefive.Stream`

```python
Help on class Stream in module threefive.stream:

class Stream(builtins.object)
 |  Stream(tsdata, show_null=True)
 |  
 |  Stream class for parsing MPEG-TS data.
 |  
 |  Methods defined here:
 |  
 |  __init__(self, tsdata, show_null=True)
 |      tsdata is an file or http/https url
 |      set show_null=False to exclude Splice Nulls
 |      
 |      Use like...
 |      
 |      from threefive import Stream
 |      strm = Stream("vid.ts",show_null=False)
 |      strm.decode()
 |  
 |  __repr__(self)
 |  
 |  decode(self, func=<function show_cue at 0x00007fb582c77420>)
 |      Stream.decode reads self.tsdata to find SCTE35 packets.
 |      func can be set to a custom function that accepts
 |      a threefive.Cue instance as it's only argument.
 |  
 |  decode_fu(self, func=<function show_cue at 0x00007fb582c77420>)
 |      Stream.decode_fu decodes
 |      1880 packets at a time.
 |  
 |  decode_next(self)
 |      Stream.decode_next returns the next
 |      SCTE35 cue as a threefive.Cue instance.
 |  
 |  decode_program(self, the_program, func=<function show_cue at 0x00007fb582c77420>)
 |      Stream.decode_program limits SCTE35 parsing
 |      to a specific MPEGTS program.
|  
 |  decode_proxy(self, func=<function show_cue_stderr at 0x00007fb582c774c0>)
 |      Stream.decode_proxy writes all ts packets are written to stdout
 |      for piping into another program like mplayer.
 |      SCTE-35 cues are printed to stderr.
 |  
 |  decode_start_time(self)
 |      displays streams that will be
 |      parsed for SCTE-35.
 |  
 |  show(self)
 |      displays streams that will be
 |      parsed for SCTE-35.
 |  
 |  strip_scte35(self, func=<function show_cue_stderr at 0x00007fb582c774c0>)
 |      Stream.strip_scte35 works just likle Stream.decode_proxy,
 |      MPEGTS packets, ( Except the SCTE-35 packets) ,
 |      are written to stdout after being parsed.
 |      SCTE-35 cues are printed to stderr.
 |  
 |  ----------------------------------------------------------------------
```
```

#### class `threefive.Segment`


```python
Help on class Segment in module threefive.segment:

class Segment(threefive.stream.Stream)
 |  Segment(seg_uri, key_uri=None, iv=None)
 |  
 |  The Segment class is a Sub Class of threefive.Stream
 |  made for small, fixed size MPEGTS files,like HLS segments.
 |  
 |  Segment Class Specific Features:
 |  
 |  * Decryption of AES Encrypted MPEGTS.
 |  
 |  * Segment.cues  a list of SCTE35 cues found in the segment.
 |  
 |  
 |  Example:
 |  
 |      from threefive import Segment
 |  
 |      >>>> uri = "https://example.com/1.ts"
 |      >>>> seg = Segment(uri)
 |      >>>> seg.decode()
 |      >>>> [cue.encode() for cue in cues]
 |      ['/DARAAAAAAAAAP/wAAAAAHpPv/8=',
 |      '/DAvAAAAAAAAAP/wFAUAAAKWf+//4WoauH4BTFYgAAEAAAAKAAhDVUVJAAAAAOv1oqc=']
 |  
 |      # For aes encrypted files
 |  
 |      >>>> key = "https://example.com/aes.key"
 |      >>>> IV=0x998C575D24F514AEC84EDC5CABCCDB81
 |      >>>> uri = "https://example.com/aes-1.ts"
 |  
 |      >>>> seg = Segment(uri,key_uri=key, iv=IV)
 |      >>>> seg.decode()
 |      >>>> {cue.packet_data.pcr:cue.encode() for cue in seg.cues}
 |  
 |     { 89718.451333: '/DARAAAAAAAAAP/wAAAAAHpPv/8=',
 |     89730.281789: '/DAvAAAAAAAAAP/wFAUAAAKWf+//4WoauH4BTFYgAAEAAAAKAAhDVUVJAAAAAOv1oqc='}

 |  
 |  Method resolution order:
 |      Segment
 |      threefive.stream.Stream
 |      builtins.object
 |  
 |  Methods defined here:
 |  
 |  __init__(self, seg_uri, key_uri=None, iv=None)
 |      tsdata is an file or http/https url
 |      set show_null=False to exclude Splice Nulls
 |      
 |      Use like...
 |      
 |      from threefive import Stream
 |      strm = Stream("vid.ts",show_null=False)
 |      strm.decode()
 |  
 |  __repr__(self)
 |  
 |  add_cue(self, cue)
 |      add_cue is passed to a Stream instance
 |      to collect SCTE35 cues.
 |  
 |  decode(self)
 |      decode a mpegts segment.
 |  
 |  show_cue(self, cue)
 |      the Segment,cues list.
 |  
 |  ----------------------------------------------------------------------
 |  Methods inherited from threefive.stream.Stream:
 |  
 |  decode_fu(self, func=<function show_cue at 0x00007fb582c77420>)
 |      Stream.decode_fu decodes
 |      1880 packets at a time.
 |  
 |  decode_next(self)
 |      Stream.decode_next returns the next
 |      SCTE35 cue as a threefive.Cue instance.
 |  
 |  decode_program(self, the_program, func=<function show_cue at 0x00007fb582c77420>)
 |      Stream.decode_program limits SCTE35 parsing
 |      to a specific MPEGTS program.
 |  
 |  decode_proxy(self, func=<function show_cue_stderr at 0x00007fb582c774c0>)
 |      Stream.decode_proxy writes all ts packets are written to stdout
 |      for piping into another program like mplayer.
 |      SCTE-35 cues are printed to stderr.
 |  
 |  decode_start_time(self)
 |      displays streams that will be
 |      parsed for SCTE-35.
 |  
 |  show(self)
 |      displays streams that will be
 |      parsed for SCTE-35.
 |  
 |  strip_scte35(self, func=<function show_cue_stderr at 0x00007fb582c774c0>)
 |      Stream.strip_scte35 works just likle Stream.decode_proxy,
 |      MPEGTS packets, ( Except the SCTE-35 packets) ,
 |      are written to stdout after being parsed.
 |      SCTE-35 cues are printed to stderr.
 |  
 |  ----------------------------------------------------------------------
```
