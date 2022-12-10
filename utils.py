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
from math import ceil

def max_value(bases, channel_order):
  sum=1
  for i in range(len(bases)):
    if i in channel_order:
      sum *= bases[i]
  return sum-1

def color_seq(val, codex, channel_order, max=256, amnt=3):
  colors=[0 for k in range(amnt)]
  bases=[ceil(max/num) for num in codex]
  
  high=max_value(bases, channel_order)
  if val>high:
    return val-high

  for n in range(len(colors)):
    if n in channel_order:
      for i in range(len(colors)):
        if channel_order[i]==n:
          colors[i]=int(val%bases[n])*codex[n]
        
      val //= bases[n]
    if val == 0:
      break

  return colors

print(color_seq(3, [255,20,30], [0,1,0]))
