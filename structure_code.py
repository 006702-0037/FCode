import numpy as np
import cv2

def create_aruco_marker(size, marker_id):
    dictionary = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
    tag = np.zeros((size, size, 1), dtype="uint8")
    marker = cv2.aruco.drawMarker(dictionary, marker_id, size, tag, 1)

    return marker

def organize_color_seq(color_seq):
    square = int(len(color_seq) ** 0.5) + 1
    for _ in range(square ** 2 - len(color_seq)):
        color_seq.append([255, 255, 255])

    pixels = np.array(color_seq, dtype=np.uint8)
    pixels = pixels.reshape(-1, square, 3)
    return pixels

def GenerateFcode(color_sequence):
    pixels=organize_color_seq(color_sequence)

    # Define image dimensions
    width,height,colors = pixels.shape
    border_multiplier=1.15
    # Create the image with ArUco markers
    aruco_size = max([6*4,width, height]) // 4
    markers = [1, 2, 3]  # IDs for the three corners
    aruco_images = []

    for marker_id in markers:
        aruco_image = create_aruco_marker(aruco_size, marker_id)
        aruco_images.append(aruco_image)

    # Create a larger canvas for the resized image and markers with white borders
    canvas = np.ones((height + 2 * (aruco_size), width + 2 * (aruco_size), 3),dtype=np.uint8) * 255

    for i in range(aruco_size, width+aruco_size):
        canvas[:, i:i + 1] = [0,0,255]
    for i in range(aruco_size+1, width+aruco_size-1, 1 * 2):
        canvas[:, i:i + 1] = 0

    for j in range(aruco_size, height+aruco_size):
        canvas[j:j + 1, :] = [0,255,0]
        canvas[j, 0:aruco_size] = [255,0,0]
    for j in range(aruco_size+1, height+aruco_size-1, 1 * 2):
        canvas[j:j + 1, :] = 0

    canvas[aruco_size:-aruco_size, aruco_size:-aruco_size] = pixels

    # Place ArUco markers touching corners with the resized image
    canvas[:aruco_size, :aruco_size] = aruco_images[0]
    canvas[:aruco_size, -aruco_size:] = aruco_images[1]
    canvas[-aruco_size:, :aruco_size] = aruco_images[2]

    canvas = cv2.resize(canvas, (500,500), interpolation = cv2.INTER_AREA)
    height, width, channels = canvas.shape

    border_size=int(height*(border_multiplier**0.5))-height

    new_height = height+2*border_size
    new_width = width+2*border_size

    bordered_image = np.ones((new_height, new_width, channels), dtype=np.uint8) * 255
    bordered_image[border_size:-border_size, border_size:-border_size] = canvas

    # Display or save the resulting image
    cv2.imshow("Image with ArUco Markers", bordered_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    import encode

    import text_utils as tut
    import numpy as np

    #example_text = "According to all known laws of aviation, there is no way a bee should be able to fly. Its wings are too small to get its fat little body off the ground. The bee, of course, flies anyway because bees don't care what humans think is impossible. Yellow, black. Yellow, black. Yellow, black. Yellow, black. Ooh, black and yellow! Let's shake it up a little. Barry! Breakfast is ready! Ooming! Hang on a second. Hello? - Barry? - Adam? - Oan you believe this is happening? - I can't. I'll pick you up. Looking sharp. Use the stairs. Your father paid good money for those. Sorry. I'm excited. Here's the graduate. We're very proud of you, son. A perfect report card, all B's. Very proud. Ma! I got a thing going here. - You got lint on your fuzz. - Ow! That's me! - Wave to us! We'll be in row 118,000. - Bye! Barry, I told you, stop flying in the house! - Hey, Adam. - Hey, Barry."
    #example_text="do them long johns get it on?????"
    example_text="Knock Knock!... Who's there?... Lettuce!... Thats impossible, lettuce cant speak."
    test_num = tut.text_to_num(example_text)

    codex = [255, 255, 255]
    order = [0, 1, 2]

    color_barcode = encode.color_seq(test_num, codex, order)
    GenerateFcode(color_barcode)