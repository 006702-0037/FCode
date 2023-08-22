import encode
import decode

import text_utils as tut
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


example_text = "According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans think is impossible. Yellow, black. Yellow, black. Yellow, black. Yellow, black. Ooh, black and yellow! Let's shake it up a little. Barry! Breakfast is ready! Ooming! Hang on a second. Hello?"
test_num=tut.text_to_num(example_text)

codex=[1,1,1]
order=[0,1,2]

color_barcode=encode.color_seq(test_num, codex, order)
print(color_barcode)
print(f"\n num of colored pixels - {len(color_barcode)}")

decoded_num=decode.dec_color_seq(color_barcode, codex, order)
recovered_text=tut.num_to_text(decoded_num)
print(f"\ninput text: \"{example_text}\"")
print(f"decoded text: \"{recovered_text}\"")

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
