from PIL import Image,ImageFont, ImageDraw
import tkinter as tk
from tkinter import filedialog






standard_ratio = 2.5

ascii_characters = ["`",".","-", "'" ,":", "_",",","^", "=", ";", ">","<","+","!","r","c","*","/","z","?","s","L","T","v",")","J","7","(","|","F","i","{","C","}","f","I","3","1","t","l","u","[","n","e","o","Z","5","Y","x","j","y","a","]","2","E","S","w","q","k","P","6","h","9","d","4","V","p","O","G","b","U","A","K","X","H","m","8","R","D","#","$","B","g","0","M","N","W","Q","%","&","@"]

def image_to_ascii(image_path, width=100):
    my_image = Image.open(image_path)
    original_width, original_height = my_image.size
    aspect_ratio =width/original_width 
    new_height = int(original_height * (aspect_ratio/standard_ratio))
    print (str(aspect_ratio) + " " + str(original_height) + " " + str(original_width) + " " + str(new_height))

    my_image = my_image.resize((width, new_height))
    grayscale_image = my_image.convert("L")  # Convert to grayscale

    ascii_image = ""
    for y in range(new_height):
        
        line = "";
        for x in range(width):
            pixel_value = grayscale_image.getpixel((x, y))
            ascii_char = ascii_characters[pixel_value * (len(ascii_characters) - 1) // 255]
            ascii_image += ascii_char
            line += ascii_char
        print(line)
        ascii_image += "\n"
        

    img =Image.new("1", (original_width*3,original_height*3),1)
    draw = ImageDraw.Draw(img)

    # use a bitmap font
    font = ImageFont.truetype("ConsolaMono-Book.ttf", size=10)

    draw.text((1, 1), ascii_image, font=font)

    img.show()

    return ascii_image


# with pyvirtualcam.Camera(width=1280, height=720, fps=30) as cam:
#     while True:
#         frame = np.zeros((cam.height, cam.width, 4), np.uint8) # RGBA
#         frame[:,:,:3] = cam.frames_sent % 255 # grayscale animation
#         frame[:,:,3] = 255
#         cam.send(frame)
#         cam.sleep_until_next_frame()

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename() 

if file_path:
    ascii_image = image_to_ascii(file_path)
    

    print(ascii_image)
else:
    print("No image selected.")


