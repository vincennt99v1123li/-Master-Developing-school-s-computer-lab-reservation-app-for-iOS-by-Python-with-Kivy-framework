import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.app import runTouchApp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton, MDFlatButton

#Window.size = (1000, 1000)
import socket
kivy.require("2.0.0")

class StartPage (GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start_button(self):

        project_5327.screen_manager.current = 'login'
        pass

class LoginPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids.username.text = ''
        self.ids.pw.text = ''


    def login_button(self):
        username = self.username.text
        pw = self.pw.text

        if username == "test" and pw == "test":
            self.ids.username.text = ''
            self.ids.pw.text = ''
            project_5327.screen_manager.current = 'test'
        pass

class TestPage(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def send_button(self):
        input_box = self.input_box.text
        input_address = self.input_address.text
        input_port = self.input_port.text
        print(input_box)
        print(input_address)
        print(input_port)


        s = socket.socket()

        port = int(input_port)
        full_address = str(input_address) + '.tcp.ngrok.io'
        s.connect((full_address, port))


        feedback = str(s.recv(1024).decode())
        print(s.recv(1024).decode())
        s.close()

        project_5327.InfoPage.update_info(feedback)
        project_5327.screen_manager.current = 'info'

        pass

    def file_button(self):
        project_5327.screen_manager.current = 'file'
        pass

    def on_save(self, instance, value, date_range):
        print(instance, value, date_range)
        self.ids.date_label.text = str(value)

    def Show_Date_Picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()



    def confirm_logout_popup(self):
        btn1 = MDFlatButton(text="Yes",text_color=[0, 0, 1, 0])
        btn1.bind(on_press=self.logout_button)
        my_dialog = MDDialog(title="Confirm Logout",
                             text="Click 'Yes' to Logout",
                             buttons=[btn1])
        my_dialog.open()
        pass

    def logout_button(self,instance):
        project_5327.screen_manager.current = 'start'
        pass


class FilePage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def back_button(self):
        project_5327.screen_manager.current = 'test'
        pass

# Simple information/error page
class InfoPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.cols = 1
        self.message = Label(halign="center", valign="middle", font_size=30)
        self.message.bind(width=self.update_text_width)
        self.add_widget(self.message)

        self.join = Button(text="back")
        self.join.bind(on_press=self.back_button)
        self.add_widget(Label())  # just take up the spot.
        self.add_widget(self.join)

    # Called with a message, to update message text in widget
    def update_info(self, message):
        self.message.text = message

    # Called on label width update, so we can set text width properly - to 90% of label width
    def update_text_width(self, *_):
        self.message.text_size = (self.message.width * 0.9, None)

    def back_button(self,instance):

        project_5327.screen_manager.current = 'test'
        pass



class HomePage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def login_button(self):
        username = self.username.text
        pw = self.pw.text

        if username == "test" and pw == "test":
            print("hi")
        pass

class ProjectApp(MDApp):
    def build(self):
        self.screen_manager = ScreenManager()
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = "Blue"
        self.widget_style= "ios"


        #start page
        self.StartPage = StartPage()
        screen = Screen(name='start')
        screen.add_widget(self.StartPage)
        self.screen_manager.add_widget(screen)

        #login page
        self.LoginPage = LoginPage()
        screen = Screen(name='login')
        screen.add_widget(self.LoginPage)
        self.screen_manager.add_widget(screen)

        # home page
        self.HomePage = HomePage()
        screen = Screen(name='home')
        screen.add_widget(self.HomePage)
        self.screen_manager.add_widget(screen)

        self.TestPage = TestPage()
        screen = Screen(name='test')
        screen.add_widget(self.TestPage)
        self.screen_manager.add_widget(screen)

        self.InfoPage = InfoPage()
        screen = Screen(name='info')
        screen.add_widget(self.InfoPage)
        self.screen_manager.add_widget(screen)

        self.FilePage = FilePage()
        screen = Screen(name='file')
        screen.add_widget(self.FilePage)
        self.screen_manager.add_widget(screen)

        return self.screen_manager




if __name__ == "__main__":
    project_5327 = ProjectApp()
    project_5327.run()