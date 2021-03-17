import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import image



def encode(path_image, key, saveas, source, encode=True):
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = Random.new().read(AES.block_size)  # generate IV
    encryptor = AES.new(key, AES.MODE_CBC, IV)
    padding = AES.block_size - len(source) % AES.block_size  # calculate needed padding
    source += bytes([padding]) * padding  # Python 2.x: source += chr(padding) * padding
    data = IV + encryptor.encrypt(source)  # store the IV at the beginning and encrypt
    #print(base64.b64encode(data).decode("latin-1") if encode else data)
    image.encrypt_data_into_image(path_image, base64.b64encode(data).decode("latin-1"),saveas)

def decode(path_image, key, decode=True):
    source = image.decrypt_data_from_image(path_image)
    if decode:
        source = base64.b64decode(source.encode("latin-1"))
    key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
    IV = source[:AES.block_size]  # extract the IV from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, IV)
    data = decryptor.decrypt(source[AES.block_size:])  # decrypt
    padding = data[-1]  # pick the padding value from the end;
    if data[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
        print("Wrong passphrase!")
    return (data[:-padding]).decode()  # remove the padding
