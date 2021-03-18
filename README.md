# Steganography

Steganography is a POC tool. The purpose of this is to become familiar with Steganography and to design a simple LSB stego application. 

## Installation

For Windows:

```bash
git clone https://github.com/fivestars10/Steganography.git
cd Steganography
pip install -r .\requirements\local.txt
```
For Linux:

```bash
git clone https://github.com/fivestars10/Steganography.git
cd Steganography
make install
```

## Usage

```python
python3 .\steg_cli.py -h

usage: Steg [-h] [--image IMAGE] [--encode] [--decode]

optional arguments:
  -h, --help            show this help message and exit
  --image IMAGE, -i IMAGE
                        Specify the path to an image file (with extension)

Encode:
  Encode message into an image file

  --encode, -e          Enable Encoding. Require to run with -i

Decode:
  Decode message from an image file

  --decode, -d          Enable Decoding. Require to run with -i

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)