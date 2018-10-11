#! python3
# -*- coding: utf-8 -*-
import codecs
import struct
import uao_u2b
import uao_b2u

class Codec(codecs.Codec):
    def encode(self,input,errors='replace'):
        uaostr = b''
        ptr = 0
        
        input_len = len(input)
        
        while input_len > ptr:
            try :
                uni = input[ptr:ptr+1]
                mapkey = encoding_map[bytes(uni, 'utf-8')]
                hex = struct.pack('>i', mapkey)[2:]
                uaostr += hex
                ptr += 1
            except:
                uni = input[ptr:ptr+1]
                uaostr += uni.encode('big5hkscs', 'replace')
                ptr += 1
            
        return uaostr, len(uaostr)

    def decode(self,input,errors='replace'):
        unistr = ''
        ptr = 0
        
        input_len = len(input)
        
        while input_len > ptr:
            try :
                hex = input[ptr:ptr+2]
                mapkey = struct.unpack('!H', hex)[0]
                uni = chr(decoding_map[mapkey])
                unistr += uni
                ptr += 2
            except:
                hex = input[ptr:ptr+1]    
                val = struct.unpack('!B', hex)[0]
                uni = chr(val)
                unistr += uni
                ptr += 1
            
        return unistr, len(unistr)

class IncrementalEncoder(codecs.IncrementalEncoder):
    pass

class IncrementalDecoder(codecs.IncrementalDecoder):
    pass

class StreamWriter(Codec,codecs.StreamWriter):
    pass

class StreamReader(Codec,codecs.StreamReader):
    pass

    
def getregentry(codec_name):
    return codecs.CodecInfo(
        name='big5ext',
        encode=Codec().encode,
        decode=Codec().decode,
        incrementalencoder=IncrementalEncoder,
        incrementaldecoder=IncrementalDecoder,
        streamreader=StreamReader,
        streamwriter=StreamWriter,
    )

codecs.register(getregentry)
