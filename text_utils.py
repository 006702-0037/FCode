def text_to_num(text, format='utf-8', endian='big'):
  return int.from_bytes(text.encode(format), endian)

def num_to_text(num, format='utf-8', endian='big'):
  return num.to_bytes((num.bit_length() + 7) // 8, endian).decode(format)

if __name__ == "__main__":
  example = "common bingus w"

  out_num = text_to_num(example)
  ret_text = num_to_text(out_num)

  assert ret_text==example, "conversion failed!"
  
  print(f"input text: \"{example}\"")
  print(f"equivalent number: {out_num}")
  
