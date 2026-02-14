#!/usr/bin/env python3

def encrypt(plaintext):
    encrypted = bytearray()
    state = plaintext[0]
    
    for byte in plaintext:
        enc_byte = byte ^ state
        encrypted.append(enc_byte)
        state = ((state << 3) + (enc_byte << 1) + byte) % 256
    
    return bytes(encrypted)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python encrypt.py <plaintext>")
        print("Example: python encrypt.py 'your_message_here'")
        sys.exit(1)
    
    plaintext = sys.argv[1].encode()
    encrypted = encrypt(plaintext)
    
    with open("flag.txt", "w") as f:
        f.write(encrypted.hex())
    
    print(f"Encryption successful!")
    print(f"Encrypted length: {len(encrypted)} bytes")
    print(f"Output saved to: flag.txt (hex format)")
