from PIL import Image, ImageFont, ImageDraw
import pyvirtualcam
import numpy as np
import cv2

standard_ratio = 2.2

ascii_characters = ["`",".","-", "'" ,":", "_",",","^", "=", ";", ">","<","+","!","r","c","*","/","z","?","s","L","T","v",")","J","7","(","|","F","i","{","C","}","f","I","3","1","t","l","u","[","n","e","o","Z","5","Y","x","j","y","a","]","2","E","S","w","q","k","P","6","h","9","d","4","V","p","O","G","b","U","A","K","X","H","m","8","R","D","#","$","B","g","0","M","N","W","Q","%","&","@"]
def normalize_grayscale(frame):
    # Normalize grayscale values to the range [0, 255]
    min_val = np.min(frame)
    max_val = np.max(frame)
    normalized_frame = ((frame - min_val) / (max_val - min_val)) * 255
    return normalized_frame.astype(np.uint8)

def image_to_ascii(frame, width=100):
    my_image = Image.fromarray(frame)
    original_width, original_height = my_image.size
    aspect_ratio = width / original_width
    new_height = int(original_height * (aspect_ratio/standard_ratio))

    my_image = my_image.resize((width, new_height))
    grayscale_image = my_image.convert("L")  # Convert to grayscale

    ascii_image = ""
    for y in range(new_height):
        line = ""
        for x in range(width):
            pixel_value = grayscale_image.getpixel((x, y))
            ascii_char = ascii_characters[int((pixel_value / 255) * (len(ascii_characters) - 1))]
            ascii_image += ascii_char
            line += ascii_char
        ascii_image += "\n"

    return ascii_image

def create_ascii_frame(ascii_image, width, height):
    img = Image.new("RGB", (width, height), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    lines = ascii_image.strip().split('\n')
    line_height = font.getsize(" ")[1]
    total_text_height = len(lines) * line_height
    y = (height - total_text_height) // 2  # Calculate top-left corner position for centering

    for line in lines:
        text_width, text_height = font.getsize(line)
        x = (width - text_width) // 2  # Calculate top-left corner position for centering
        draw.text((x, y), line, font=font, fill=(255, 255, 255))
        y += line_height

    return np.array(img)

# with pyvirtualcam.Camera(width=1280, height=720, fps=30) as cam:
#     print(f'Using virtual camera: {cam.device}')
#     frame = np.zeros((cam.height, cam.width, 3), np.uint8)  # RGB
#     while True:
#         frame[:] = cam.frames_sent % 255  # grayscale animation
#         cam.send(frame)
#         cam.sleep_until_next_frame()

        # frame = np.zeros((cam.height, cam.width, 3), np.uint8)  # RGB
        # frame[:, :, :] = cam.frames_sent % 255  # RGB animation

        # # Convert the frame to ASCII
        # ascii_image = image_to_ascii(frame, cam.width//3)

        # # Create an ASCII image
        # ascii_frame = create_ascii_frame(ascii_image, cam.width, cam.height)


        # cam.send( ascii_frame)
        # cam.sleep_until_next_frame()


cap = cv2.VideoCapture(0)  # Open the default camera (usually 0)

with pyvirtualcam.Camera(width=1280, height=720, fps=30) as cam:
    while True:
        ret, frame = cap.read()  # Read a frame from the camera

        # Convert the frame to ASCII
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        normalized_frame = normalize_grayscale(frame)
        ascii_image = image_to_ascii(normalized_frame, cam.width//6)

        # Create an ASCII image
        ascii_frame = create_ascii_frame(ascii_image, cam.width, cam.height)

        cam.send(ascii_frame)
        
        cam.sleep_until_next_frame()

cap.release()  # Release the camera