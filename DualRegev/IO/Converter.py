__all__ = [
    'bytes_to_binary',
    'binary_to_bytes',
    'binary_to_bytes',
    'bytes_to_binary',
]

"""
這裡的程式碼都是改寫自ChatGPT-4o
"""



# bytes <-> str: 0x...
def bytes_to_hex(byte_data):
    hex_str = byte_data.hex()
    
    return '0x' + hex_str

def hex_to_bytes(data):
    hex_str = data[2:]
    byte_data = bytes.fromhex(hex_str)

    return byte_data

# bytes <-> str: 0b...
def bytes_to_binary(byte_data):
    integer_value = int.from_bytes(byte_data, byteorder='big')
    
    binary_str = bin(integer_value)[2:]
    original_length = len(byte_data) * 8
    
    binary_str = binary_str.zfill(original_length)
    return '0b' + binary_str

def binary_to_bytes(data):
    binary_str = data[2:]

    integer_value = int(binary_str, 2)
    byte_length = (integer_value.bit_length() + 7) // 8

    byte_data = integer_value.to_bytes(byte_length, byteorder='big')
    return byte_data


if __name__ == '__main__':
    data = "0b11001101"
    print(data)
    a = binary_to_bytes(data)
    print(a)
    b = bytes_to_strbinary(a)
    print(b)