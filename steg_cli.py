import argparse
import util
from getpass import getpass
import PIL.Image
import io
import os
from os import path
import time


switches = argparse.ArgumentParser(prog='Steg')
switches.add_argument('--image', '-i', required=True, help="Specify cover image (with extension)")
switches.add_argument('--secret', '-s', help="Specify secret image (with extension)")
switches.add_argument('--output', '-o', help="Specify the path to an image file (with extension)")

### Encode Group Arguments ###
encode_group = switches.add_argument_group('Encode', 'Encode message into an image file')
encode_group.add_argument('--encode', '-e', action="store_true", help="Enable Encoding.")

### Decode Group Arguments ###
decode_group = switches.add_argument_group('Decode', 'Decode message from an image file')
decode_group.add_argument('--decode', '-d', action="store_true", help="Enable Decoding.")
args = switches.parse_args()

def check_image_file(image, secret):
    # Opening and converting images to RGB
    cover_img = PIL.Image.open(image)
    cover_img = cover_img.convert('RGB')
    secret_img = PIL.Image.open(secret)
    secret_img = secret_img.convert('RGB')

    # Calculating sizes
    cover_size = cover_img.width * cover_img.height
    secret_size = secret_img.width * secret_img.height

    if cover_size >= secret_size * 8:
        return True
    else:
        print("Cover image is not large enough to hold secret data.")

def image_exist():
    if args.image:
        if path.exists(args.image):
            return True
        else:
            print("Unable to locate image file!")
    else:
        print("Require an image file")

def image_to_bytes(path):
    count = os.stat(path).st_size / 2
    with open(path, 'rb') as f:
        return f.read()

def bytes_to_image(bytes_data, saveas):
    image = PIL.Image.open(io.BytesIO(bytes_data))
    image.save(saveas)

def main():
    if args.encode:
        if image_exist():
            if check_image_file(args.image, args.secret):
                plain_text_message = image_to_bytes(args.secret)
                key = getpass(prompt='Enter a passphrase to encrypt: ')
                saveas = args.output
                print("Processing...")
                time.sleep(2)
                util.encode(args.image, bytes(key, 'utf-8'), saveas, plain_text_message)
                print("Process Completed! " + str(saveas) + " has been created.")
    elif args.decode:
        if image_exist():
            decrypt_key = getpass(prompt='Enter a passphrase to decrypt: ')
            bytes_data = util.decode(args.image, bytes(decrypt_key, 'utf-8'))
            print("Processing...")
            time.sleep(2)
            bytes_to_image(bytes_data, args.output)
            print("Process Completed! " + str(args.output) + " has been created.")
main()