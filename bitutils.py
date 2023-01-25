
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

def text_from_bits(bits):
    n = int(''.join(bits), 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

def str_encode_bit(text, max_val):
  text_bin = text_to_bits(text)
  
  start=0
  out=[]
  for i in range(len(text_bin)):
    if bit_lookup_num("".join(text_bin[start:i]))>max_val:
      out.append(bit_lookup_num("".join(text_bin[start:i-1])))
      start=i-1
  out.append(bit_lookup_num("".join(text_bin[start:len(text_bin)])))
  return out

def bit_decode_str(nums):
  bits=[num_lookup_bit(i) for i in nums]
  return text_from_bits(bits)

if __name__ == "__main__":
  max_val=256000
  test_str="my mans got that sploinky"
  returned = str_encode_bit(test_str, max_val)
  decoded=bit_decode_str(returned)

  print("".join(text_to_bits(test_str)))
  print()
  print(returned)
  print()
  print(f"pixel count - {len(returned)}")
  print(decoded)
