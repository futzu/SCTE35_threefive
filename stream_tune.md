
### Tuning PAT and PMT packet parsing in threefive.Stream

*  __cProfile'd the Stream class parsing 3.7GB of MPEGTS video for SCTE35.__
 ```sh
 
        106,143,354 function calls (106142526 primitive calls) in 36.231 seconds


    75710    0.025    0.000    0.025    0.000 stream.py:166(_parse_length)
    37840    0.007    0.000    0.007    0.000 stream.py:173(_parse_program_number)
    
 20859289    5.287    0.000    8.727    0.000 stream.py:180(_parser)
 
     8399    0.448    0.000    1.427    0.000 stream.py:247(_program_association_table)
     
    37840    0.325    0.000    0.638    0.000 stream.py:257(_program_map_table)
    37840    0.105    0.000    0.107    0.000 stream.py:296(_parse_program_streams)

```
*  __Added Stream._last_pat__ (type bytes, holds last pat packet payload) 
*  __Added Stream._last_pmt__ (type dict, maps pmt_pid and  packet payload)

* __Added comparison checks__ in Stream._parser(pkt) to __skip parsing for PAT or PMT packets with the same payload__.


* cProfile'd the Stream class parsing 3.7GB of MPEGTS video for SCTE35.__( after the changes)__
       
     *  __Boom goes the dynamite__.
```sh
       105,227,586 function calls (105226758 primitive calls) in 32.990 seconds

       50    0.000    0.000    0.000    0.000 stream.py:168(_parse_length)
       10    0.000    0.000    0.000    0.000 stream.py:175(_parse_program_number)
       
 20859289    5.141    0.000    6.502    0.000 stream.py:182(_parser
 
                 # 1 call. 1 unique PAT in the video stream.
                 
        1    0.000    0.000    0.001    0.001 stream.py:258(_program_association_table)
      
                 # 10 calls. 10 programs in the video stream. 10 PMTs
       
       10    0.000    0.000    0.002    0.000 stream.py:268(_program_map_table)
       10    0.000    0.000    0.002    0.000 stream.py:307(_parse_program_streams)


```


| Method                           |          Calls  Before|                 Calls  After|
|----------------------------------|------------------------|------------------------|
|Stream._parse_length              |     __75710__ |        __50__ |
|Stream._parse_program_number      |     __37840__ |        __10__ |
|Stream._program_association_table |      __8399__ |         __1__ |
|Stream._program_map_table         |     __37840__ |        __10__ |
|Stream._parse_program_streams|     __37840__ |        __10__ |
