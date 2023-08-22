from math import ceil
from encode import color_seq, max_value
  
def dec_color_seq(vals, codex, channel_order, max_val=256):

  assert len(codex)==len(channel_order)
  bases=[ceil(max_val/num) for num in codex]
  high=int(max_value(bases, channel_order))+1
  
  sum = 0
  for n in range(len(vals)):
    total=0
    mult=1
    color = vals[n]

    for i in range(len(channel_order)):
      if i in channel_order:
        pos=channel_order.index(i)
        total+=int(color[pos]/codex[i])*mult
        mult*=bases[i]
    sum+=total*(high**n)
    
  return int(sum)
    
  
if __name__ == "__main__":  
  test_num = 123456789
  
  test_codex = [1,1,1]
  test_order = [-1,0,-1]

  print(f"encoded number: \"{test_num}\"")
  
  pixels = color_seq(test_num,test_codex,test_order)
  out = dec_color_seq(pixels,test_codex,test_order)
  print(f"decoded number: \"{out}\"")
