def encrypt(data):
    flux = (len(data) << 8) | data[0]
    output = []
    
    for i, byte in enumerate(data):
        echo = byte ^ (flux & 0xff)
        output.append(echo)
        
        if i % (len(data) % 10 + 5) == 0:
            flux ^= (echo << (i % 5))
        
        _ = (flux >> 3) & 0x7f
        
        flux = (flux * 3 + echo) & 0xffffffff
    
    return bytes(output)
