import qrcode
from PIL import Image, ImageFont, ImageDraw
from os.path import join, dirname
from sys import argv

# loading base images
background_img = join(dirname(__file__), "images/background.jpg")
central_logo  = join(dirname(__file__), "images/logo.jpg")

# QR code resolution
qr_res = (190,190)

# QR position on background image
qr_pos = (105,75)

# TEXT FOR COMPANY NAME ( or other )
text_1_size = 22
text_1_pos = (110, 350)

# TEXT FOR CONTENT
text_2_size = 40
text_2_pos = (110, 280)

# fixing text size and font style
text_1_font = ImageFont.truetype(join(dirname(__file__), "fonts/GOTHICB.ttf"), text_1_size)
text_2_font = ImageFont.truetype(join(dirname(__file__), "fonts/GOTHICB.ttf"), text_2_size)

def getQR(strs, name):
  qr = qrcode.QRCode(
    version = 1,
    error_correction = qrcode.constants.ERROR_CORRECT_L,
    box_size = 10,
    border = 2,
  )

  qr.add_data(strs)
  qr.make(fit = True)

  # creating qr image  in black and white
  img = qr.make_image(
    fill_color = "black", 
    back_color = "white")

  icon = Image.open(central_logo)
  img_w, img_h = img.size

  factor = 6
  size_w = int(img_w / factor)
  size_h = int(img_h / factor)
  icon_w, icon_h = icon.size

  if icon_w > size_w:
    icon_w = size_w

  if icon_h > size_h:
    icon_h = size_h

  icon = icon.resize((icon_w, icon_h), Image.ANTIALIAS)
  w = int((img_w - icon_w) / 2)
  h = int((img_h - icon_h) / 2)

  # add icon to center of the qr image
  img.paste(icon, (w, h), None)
  img = img.convert('RGB')
  img.save(name)
  return img

def createQRTag(name, body, text_top, text_bottom):
  getQR(body.upper(), name.upper())
  print("opening ", background_img)
  oriImg = Image.open(background_img)
  oriImg2 = Image.open(name)
  oriImg2 = oriImg2.resize(qr_res)
  oriImg.paste(oriImg2, qr_pos)
  draw = ImageDraw.Draw(oriImg)

  # TEXT1 position  ( COMPANY ) 
  draw.text(text_1_pos, text_top, (0,0,0), font=text_1_font)

  # TEXT2 position 
  draw.text(text_2_pos, text_bottom, (0,0,0), font=text_2_font)

  #oriImg = oriImg.convert('RGB')
  oriImg.save(name)

if __name__ == '__main__':
    arg_1 = argv[1]
    arg_2 = argv[2]
    filename = arg_2.upper()+"_"+arg_1.upper()+".jpg"
    
    # add info and create qr tag
    createQRTag(
        join(dirname(__file__), "output", filename), 
        arg_2.upper(), 
        arg_1.upper(), 
        arg_2.upper()
    )
