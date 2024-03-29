'''
  takes a number ('num') and converts it to an rgb color
  
  the method by which it does this is taking a color
  interval for each channel (defined in 'codex') and 
  increments each channel by the corresponding amount
  in the codex (determined by the channel's index) 
  until it reaches the maximum number able to be held by
  a single color channel (256).

  Once the maximum number is reached, it sets the current
  channel value to 0 and increments the next channel by 
  its corresponding codex. The order by which the channels
  are incremented is determined by the list 'channel_order'. 

  codex and channel_order are defined as:
    -codex = [increment value for 0th order channels,
              increment value for 1st order channels,
              increment value for 2nd order channels]
    
    -channel_order = [order value for red channel,
                      order value for green channel,
                      order value for blue channel]

  They are both lists of length three typically containing positive integers.

  If a number is too high to be represented as an rgb color
  code given the codex and order in question, this function will
  return -1, signifying it was unable to complete the conversion.

    *note that by setting multiple channels to the same order value they will
     be incremented simultaneuosly by the codex value for their order

    *note that by setting a channels order to be outside of the range from 
     0-2, it will be skipped during incrementation. This may be useful if one
     is attempting to widen their colorspace by leaving a channel constant

    *note that no matter what order or codex, [0,0,0] will always be the
     universal rgb code for the number 0.

    *note that given the maximum possible codex and order, [1,1,1] and
    [0,1,2] respectively, the largest number achievable to be stored in 
    a single code would be 256^3, or 16,777,216
  
''' 

from math import ceil, log

def max_value(bases, channel_order):
  sum=1
  for i in range(len(bases)):
    if i in channel_order:
      sum *= bases[i]
  return sum-1

def color_seq(cval, ccodex, cchannel_order, max=256):

  val = int(cval)
  codex = list(ccodex)
  channel_order = list(cchannel_order)
  
  assert len(codex)==len(channel_order)
  codex_len = len(codex)
  
  colors=[0]*len(codex)
  bases=[ceil(max/num) for num in codex]
  high=max_value(bases, channel_order)
  pix_cnt = ceil(log(val)/log(high+1))-1
  
  channel_order.extend(channel_order*pix_cnt)
  for i in range(len(channel_order)):
    if channel_order[i]>=0:
      channel_order[i]+=len(codex)*(i//len(codex))
    
  codex.extend(codex*pix_cnt)
  colors.extend(colors*pix_cnt)
  bases.extend(bases*pix_cnt)

  for n in range(len(colors)):
    if n in channel_order:
      for i in range(len(colors)):
        if channel_order[i]==n:
          colors[i]=int(val%bases[n])*codex[n]
        
      val //= bases[n]
    if val == 0:
      break
      
  return [colors[i:i + codex_len] for i in range(0, len(colors), codex_len)]


if __name__ == "__main__":  
  test_num = 22517
  
  test_codex = [5,3,5]
  test_order = [0,2,1]

  print(f"encoded number: \"{test_num}\"")
  
  pixels = color_seq(test_num,test_codex,test_order)
  print(f"number of colored pixels: {len(pixels)}")
  print("\nlist of pixels: ")
  [print("\t", pix) for pix in pixels]
