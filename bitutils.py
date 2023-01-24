from itertools import product

def bit_lookup_num(lookup):
  if lookup == '':
    return -1
    
  bits=[]
  current_len=1
  while lookup not in bits:
    bits.extend(["".join(perm[::-1]) for perm in product(["0","1"],repeat=current_len)])
    current_len+=1
  return bits.index(lookup)

def num_lookup_bit(lookup):
  if lookup == -1:
    return ''
    
  bits=[]
  current_len=1
  while len(bits)-1<lookup:
    bits.extend(["".join(perm[::-1]) for perm in product(["0","1"],repeat=current_len)])
    current_len+=1
  return bits[lookup]

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
