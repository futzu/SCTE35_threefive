
'''

Use adaptation_fields for the splice countdown.
Be nice when you splice.

'''

def adaptation_fields(bitbin):               
    adaptation_field_length=bitbin.asint(8)
    if  adaptation_field_length > 0:
        discontinuity_indicator=bitbin.asflag(1)
        random_access_indicator=bitbin.asflag(1)
        elementary_stream_priority_indicator=bitbin.asflag(1) 
        PCR_flag=bitbin.asflag(1)
        OPCR_flag=bitbin.asflag(1)                                                                   
        splicing_point_flag=bitbin.asflag(1) 
        transport_private_data_flag=bitbin.asflag(1)
        adaptation_field_extension_flag=bitbin.asflag(1)
        
        if PCR_flag:
            program_clock_reference_base =bitbin.asint(33)    
            reserved=bitbin.forward(6)
            program_clock_reference_extension = bitbin.asint(9)  
            #print(f'PCR {program_clock_reference_base}')
       
        if OPCR_flag:
            original_program_clock_reference_base = bitbin.as90k(33)
            reserved=bitbin.forward(6)
            original_program_clock_reference_extension = bitbin.asint(9)
            
        if splicing_point_flag:  
                    splice_countdown = bitbin.as90k(8)
                    #print(f'Splice Countdown: {splice_countdown}')
                    
        if transport_private_data_flag:
            tpdl = transport_private_data_length = bitbin.as90k(8)     
            while tpdl:
                private_data_byte=bitbin.asint(8)
                tpdl -=1    
        
        if adaptation_field_extension_flag:
            adaptation_field_extension_length=bitbin.asint(8)
            ltw_flag = bitbin.asflag(1)
            piecewise_rate_flag = bitbin.asflag(1)
            seamless_splice_flag = bitbin.asflag(1)
            reserved = bitbin.forward(5)
            
            if ltw_flag:
                ltw_valid_flag = bitbin.asflag(1)
                ltw_offset = bitbin.asint(15)
            
            if piecewise_rate_flag:
                reserved=bitbin.forward(2)
                piecewise_rate = bitbin.asint(22)
                
            if seamless_splice_flag:     
                splice_type = bitbin.asint(4)
                DTS_next_AU  = bitbin.asint(3) #31-29
                marker_bit = bitbin.asflag(1)
                DTS_next_AU = bitbin.asint(15) # 29 - 15
                marker_bit = bitbin.asflag(1)
                DTS_next_AU  = bitbin.asint(15)  # 14-0
                marker_bit = bitbin.asflag(1)
                                
            #  for (i = 0; i < N; i++) 
            #      reserved = bitbin.asint(8)       
             
                 
                
                    
