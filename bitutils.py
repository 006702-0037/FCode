def num_lookup_bit(val):
    return bin(val+2)[:2:-1]

def bit_lookup_num(bits):
    binary = '1' + bits[::-1]
    return int(binary, 2) - 2

def text_to_bits(text):
    bits = bin(int.from_bytes(text.encode(), 'big'))[2:]
    return list(bits.zfill(8 * ((len(bits) + 7) // 8)))

def bits_to_text(bits):
    n = int(''.join(bits), 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

def decode_bin(nums):
  return [num_lookup_bit(i) for i in nums]

def encode_bin(bin, max_val):
  start=0
  out=[]
  for i in range(len(bin)):
    if bit_lookup_num("".join(bin[start:i]))>max_val:
      out.append(bit_lookup_num("".join(bin[start:i-1])))
      start=i-1
  out.append(bit_lookup_num("".join(bin[start:len(bin)])))
  return out

if __name__ == "__main__":
    max_val=8
    test_str="got that sploinky"
    returned = encode_bin(text_to_bits(test_str), max_val)
    decoded=bits_to_text(decode_bin(returned))

    raw_bin = "".join(text_to_bits(test_str))

    print(raw_bin)
    print()
    print(returned)
    print()
    print(f"RGB pixel count - {len(returned)}")
    print(f"BW pixel count - {len(raw_bin)}")
    print(decoded)
