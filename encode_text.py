import bitutils as btut
import utils as ut
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

example_text="hi"
test_bin=btut.text_to_bits(example_text)

codex=[125,1,1]
order=[0,0,-1]
max_channel_val=256
channel_amnt=3

bases = ut.get_bases(codex,max_channel_val)
max_value = ut.max_value(bases, order)

color_barcode=[]
encoded=btut.encode_bin(test_bin, max_value)
for code in encoded:
  color_barcode.append(ut.color_seq(code, codex, order, max=max_channel_val,amnt=channel_amnt))
  
print(color_barcode)
print(f"\n num of colored pixels - {len(color_barcode)}")

square = int(len(color_barcode)**0.5)+1
for _ in range(square**2-len(color_barcode)):
  color_barcode.append([255,255,255])
  
pixels = np.array(color_barcode, dtype=np.uint8)
pixels = pixels.reshape(-1, square, 3)

im = Image.fromarray(pixels)
im.save("out.png")

plt.tight_layout()
plt.imshow(pixels)
plt.show()
