# Importing library
import qrcode

# Data to encode
data = "https://github.com/jafarmustafayev1/ecommerce_exam"

# Creating an instance of QRCode class
qr = qrcode.QRCode(version = 1,
                   box_size = 10,
                   border = 5)

# Adding data to the instance 'qr'
qr.add_data(data)

qr.make(fit = True)
img = qr.make_image(fill_color = 'yellow',
                    back_color = 'black')

img.save('MyQRCode2.png')
