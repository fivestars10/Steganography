from kivy.app import App
from kivy.uix.boxlayout import BoxLayout


class SigninWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def validate_user(self):
        user = self.ids.username_field
        pwd = self.ids.pwd_field
        info = self.ids.info

        uname = user.text
        passwd = pwd.text

        if uname == '' or passwd == '':
            info.text = '[color=#FF0000]Invalid Username or Password[/color]'
        else:
            if uname == 'admin' and passwd == 'admin':
                info.text = '[color=#00FF00]Logged In Successfully![/color]'
            else:
                info.text = '[color=#FF0000]Invalid Username or Password[/color]'

class SigninApp(App):
    def build(self):
        return SigninWindow()


if __name__ == "__main__":
    sa = SigninApp()
    sa.run()
