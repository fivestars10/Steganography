import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog,QMainWindow, QTabWidget
from PyQt5.uic import loadUi
import PIL.Image
import os
import io
import time
import util



class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("gui.ui", self)
        self.debug.setStyleSheet("background-color: rgb(36, 49, 60);")
        self.browse_cover.clicked.connect(self.enc_browsecover)
        self.browse_secret.clicked.connect(self.enc_browsesecret)
        self.browse_output.clicked.connect(self.enc_browseoutput)
        self.dec_btnCover.clicked.connect(self.dec_btnCover_Click)
        self.dec_btnSave.clicked.connect(self.dec_btnSave_Click)

        self.encode.clicked.connect(self.enc_encodeButton)
        self.decode.clicked.connect(self.dec_decodeButton)


    def check_image_file(self, image, secret):
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
            self.debug.append("<div style='color:red'>[!] Cover image is not large enough to hold secret data.</div>")

    def image_to_bytes(self, path):
        count = os.stat(path).st_size / 2
        with open(path, 'rb') as f:
            return f.read()

    def bytes_to_image(self, bytes_data, saveas):
        image = PIL.Image.open(io.BytesIO(bytes_data))
        image.save(saveas)

    def embed(self, cover, secret, output, password):
        if self.check_image_file(cover, secret):
            plain_text_message = self.image_to_bytes(secret)
            key = password
            saveas = output
            util.encode(cover, bytes(key, 'utf-8'), saveas, plain_text_message)
            self.debug.append("<div style='color:green'>[+] Processing...</div>")
            time.sleep(2)
            self.progress_bar()
            time.sleep(2)
            self.debug.append("<div style='color:green'>[+] Process Completed! " + str(output) + " has been created.</div>")

    def extract(self, cover, output, password):
        decrypt_key = password
        bytes_data = util.decode(cover, bytes(decrypt_key, 'utf-8'))
        if bytes_data == "Wrong passphrase!":
            self.debug.append("<div style='color:red'>[!] Wrong passphrase!</div>")
        else:
            self.bytes_to_image(bytes_data, output)
            self.debug.append("<div style='color:green'>[+] Processing...</div>")
            time.sleep(2)
            self.progress_bar()
            time.sleep(2)
            self.debug.append("<div style='color:green'>[+] Process Completed! " + str(output) + " has been created.</div>")

    def progress_bar(self):
        # setting for loop to set value of progress bar
        for i in range(101):
            # slowing down the loop
            time.sleep(0.01)

            # setting value to progress bar
            self.progressBar.setValue(i)

    def enc_browsecover(self):
        fname = QFileDialog.getOpenFileName(self, "Open file", "images", "Images (*.png *.bmp *.jpeg *.jpg)")
        self.enc_cover_image.setText(fname[0])

    def enc_browsesecret(self):
        fname = QFileDialog.getOpenFileName(self, "Open file", "images", "Images (*.png *.bmp *.jpeg *.jpg)")
        self.enc_secret_image.setText(fname[0])

    def enc_browseoutput(self):
        fname = QFileDialog.getSaveFileName(self, "Save as", "output", "Images (*.png)")
        self.enc_output_image.setText(fname[0])

    def enc_encodeButton(self):
        if self.enc_cover_image.text() and self.enc_secret_image.text() and self.enc_output_image.text() and self.enc_encode_pass.text():
            cover = self.enc_cover_image.text()
            secret = self.enc_secret_image.text()
            output = self.enc_output_image.text()
            password = self.enc_encode_pass.text()
            self.debug.append("<div style='color:cyan'>[+] Cover Image selected: " + cover + "</div>")
            self.debug.append("<div style='color:cyan'>[+] Secret Image selected: " + secret + "</div>")
            self.debug.append("<div style='color:cyan'>[+] Output Image selected: " + output + "</div>")
            self.debug.append("<div style='color:cyan'>[+] Password set: True </div>")
            self.embed(cover, secret, output, password)
        else:
            self.debug.append("<div style='color:red'>[!] Invalid Inputs!</div>")

    def dec_btnCover_Click(self):
        fname = QFileDialog.getOpenFileName(self, "Open file", "output", "Images (*.png *.bmp *.jpeg *.jpg)")
        self.dec_cover_image.setText(fname[0])

    def dec_btnSave_Click(self):
        fname = QFileDialog.getSaveFileName(self, "Save as", "output", "Images (*.png)")
        self.dec_output_image.setText(fname[0])

    def dec_decodeButton(self):
        if self.dec_cover_image.text() and self.dec_output_image.text() and self.dec_decode_pass.text():
            cover = self.dec_cover_image.text()
            output = self.dec_output_image.text()
            password = self.dec_decode_pass.text()
            self.debug.append("<div style='color:cyan'>[+] Cover Image selected: " + cover + "</div>")
            self.debug.append("<div style='color:cyan'>[+] Output Image selected: " + output + "</div>")
            self.debug.append("<div style='color:cyan'>[+] Password set: True </div>")
            self.extract(cover, output, password)
        else:
            self.debug.append("<div style='color:red'>[!] Invalid Inputs!</div>")




app = QApplication(sys.argv)
app.setApplicationName("Steganography Project")
mainwindow = MainWindow()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(500)
widget.setFixedHeight(650)
widget.show()
sys.exit(app.exec_())