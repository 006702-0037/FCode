def num_lookup_bit(num):
    x = 2
    bits = ''
    while num >= 0:
        bits += '0' if num%x < x/2 else '1'
        num -= x
        x *= 2
    return bits

def bit_lookup_num(bits):
    x = 2
    num = 0
    for b in bits:
        num += x//2 if b == '0' else x
        x *= 2
    return num-1

def text_to_bits(text):
    bits = bin(int.from_bytes(text.encode(), 'big'))[2:]
    return list(bits.zfill(8 * ((len(bits) + 7) // 8)))

def bits_to_text(bits):
    n = int(''.join(bits), 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

def encode_bin(bin, max_val):
  start=0
  out=[]
  for i in range(len(bin)):
    if bit_lookup_num("".join(bin[start:i]))>max_val:
      out.append(bit_lookup_num("".join(bin[start:i-1])))
      start=i-1
  out.append(bit_lookup_num("".join(bin[start:len(bin)])))
  return out

def decode_bin(nums):
  return [num_lookup_bit(i) for i in nums]

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
