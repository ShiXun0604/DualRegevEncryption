__all__ = [
    'bytes_to_binary',
    'binary_to_bytes',
    'bin_to_hex',
    'hex_to_bin',
]


# b'' <-> {0,1}*
def bytes_to_binary(data):
    return ''.join(f'{byte:08b}' for byte in data)


def binary_to_bytes(binary_str):
    byte_list = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
    return bytes(int(byte, 2) for byte in byte_list)


# 0b <-> 0x
def bin_to_hex(bin_str: str) -> str:
    if not bin_str.startswith('0b'):
        raise ValueError("Invaliv data input")
    return hex(int(bin_str, 2))

def hex_to_bin(hex_str: str) -> str:
    if not hex_str.startswith('0x'):
        raise ValueError("Invaliv data input")
    return bin(int(hex_str, 16))