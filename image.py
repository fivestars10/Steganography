from PIL import Image, ImageTk
from tkinter import filedialog
import cv2
import numpy as np
import math

def encrypt_data_into_image(path_image, data, saveas):
    image_display_size = 300, 300
    # load the image
    img = cv2.imread(path_image)
    # break the image into its character level. Represent the characters in ASCII.
    data = [format(ord(i), '08b') for i in data]
    _, width, _ = img.shape
    # algorithm to encode the image
    PixReq = len(data) * 3

    RowReq = PixReq/width
    RowReq = math.ceil(RowReq)

    count = 0
    charCount = 0
    for i in range(RowReq + 1):
        # Step 4
        while(count < width and charCount < len(data)):
            char = data[charCount]
            charCount += 1
            # Step 5
            for index_k, k in enumerate(char):
                if((k == '1' and img[i][count][index_k % 3] % 2 == 0) or (k == '0' and img[i][count][index_k % 3] % 2 == 1)):
                    img[i][count][index_k % 3] -= 1
                if(index_k % 3 == 2):
                    count += 1
                if(index_k == 7):
                    if(charCount*3 < PixReq and img[i][count][2] % 2 == 1):
                        img[i][count][2] -= 1
                    if(charCount*3 >= PixReq and img[i][count][2] % 2 == 0):
                        img[i][count][2] -= 1
                    count += 1
        count = 0
    # Write the encrypted image into a new file
    cv2.imwrite(saveas, img)


def decrypt_data_from_image(path_image):
    image_display_size = 500, 350
    # Algorithm to decrypt the data from the image
    img = cv2.imread(path_image)
    data = []
    stop = False
    for index_i, i in enumerate(img):
        i.tolist()
        for index_j, j in enumerate(i):
            if((index_j) % 3 == 2):
                # first pixel
                data.append(bin(j[0])[-1])
                # second pixel
                data.append(bin(j[1])[-1])
                # third pixel
                if(bin(j[2])[-1] == '1'):
                    stop = True
                    break
            else:
                # first pixel
                data.append(bin(j[0])[-1])
                # second pixel
                data.append(bin(j[1])[-1])
                # third pixel
                data.append(bin(j[2])[-1])
        if(stop):
            break

    message = []
    # join all the bits to form letters (ASCII Representation)
    for i in range(int((len(data)+1)/8)):
        message.append(data[i*8:(i*8+8)])
    # join all the letters to form the message.
    message = [chr(int(''.join(i), 2)) for i in message]
    message = ''.join(message)
    return message