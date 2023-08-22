import Image
from text_utils import num_to_text
from decode import dec_color_seq

im = Image.open('out.png')
pixels = list(im.getdata())

while pixels[-1]==(255,255,255):
  pixels.pop()

codex=[1,1,1]
order=[0,1,2]

ret_num = dec_color_seq(pixels, codex, order)
ret_text = num_to_text(ret_num)
print(ret_text)
