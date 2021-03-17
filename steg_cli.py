import argparse
import util
from getpass import getpass
import os.path
from os import path
import time

switches = argparse.ArgumentParser(prog='Steg')
switches.add_argument('--image', '-i', help="Specify the path to an image file (with extension)")

### Encode Group Arguments ###
encode_group = switches.add_argument_group('Encode', 'Encode message into an image file')
encode_group.add_argument('--encode', '-e', action="store_true", help="Enable Encoding. Require to run with -i")

### Decode Group Arguments ###
decode_group = switches.add_argument_group('Decode', 'Decode message from an image file')
decode_group.add_argument('--decode', '-d', action="store_true", help="Enable Decoding. Require to run with -i")
args = switches.parse_args()

def check_image_file():
    if args.image:
        if path.exists(args.image):
            return True
        else:
            print("Unable to locate image file!")
    else:
        print("Require an image file")


def main():
    ### Check if an Image file has been specified ###

    if args.encode:
        if check_image_file():
            plain_text_message = input("Please enter a message to encode: ")
            key = getpass(prompt='Enter a passphrase to encrypt: ')
            saveas = input("Save an image as (with extension): ")
            print("Processing...")
            time.sleep(2)
            util.encode(args.image ,bytes(key, 'utf-8'), saveas, bytes(plain_text_message, 'utf-8'))
            print("Process Completed! " + str(saveas) + " has been created.")
    elif args.decode:
        if check_image_file():
            decrypt_key = getpass(prompt='Enter a passphrase to decrypt: ')
            print(util.decode(args.image ,bytes(decrypt_key, 'utf-8')))
    else:
        user_input = input("Please choose whether to Encode (e) or Decode (d): ")
        while user_input != "e" and user_input != "d":
            print("Invalid Input. Please Try Again!")
            user_input = input("Please choose whether to Encode (e) or Decode (d): ")
        if user_input == "e":
            plain_text_message = input("Please enter a message to encode: ")
            key = getpass(prompt='Enter a passphrase to encrypt: ')
            path_image = input("Select an Image file (with extension): ")
            if path.exists(path_image):
                saveas = input("Save an image as (with extension): ")
                print("Processing...")
                time.sleep(2)
                util.encode(path_image, bytes(key, 'utf-8'), saveas, bytes(plain_text_message, 'utf-8'))
                print("Process Completed! " + str(saveas) + " has been created.")
            else:
                print("Unable to locate image file!")
        else:
            decrypt_key = getpass(prompt='Enter a passphrase to decrypt: ')
            path_image = input("Select an Image file (with extension): ")
            if (path.exists(path_image)):
                print(util.decode(path_image ,bytes(decrypt_key, 'utf-8')))
            else:
                print("Unable to locate image file!")

main()