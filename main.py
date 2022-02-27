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
from kivymd.uix.button import MDRaisedButton, MDFlatButton, MDFillRoundFlatButton
from kivymd.uix.list import OneLineAvatarIconListItem, OneLineIconListItem,OneLineListItem

#Window.size = (1000, 1000)
import socket
kivy.require("2.0.0")


class StartPage (GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start_button(self):

        project_5327.screen_manager.current = 'login'



class LoginPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.confirmed_username = "default"

    def login_button(self):
        username = self.username.text
        pw = self.pw.text
        input_address = self.address.text
        input_port = self.port.text

        if username == "" or pw == "":
            my_dialog = MDDialog(title="Error", text="Username or Password field should not be empty", )
            my_dialog.open()

        else:
            try:
                s = socket.socket()

                port = int(input_port)
                full_address = str(input_address) + '.tcp.ngrok.io'
                s.connect((full_address, port))

                option = "login"
                s.sendall((option).encode('utf-8'))

                feedback = str(s.recv(1024).decode('utf-8'))
                if feedback == 'OK':

                    #my_dialog = MDDialog(title="success",text=feedback,)
                    #my_dialog.open()

                    s.sendall((username).encode('utf-8'))
                    feedback2 = str(s.recv(1024).decode('utf-8'))

                    if feedback2 == 'input_username received':
                        s.sendall((pw).encode('utf-8'))
                        feedback3 = str(s.recv(1024).decode('utf-8'))

                        if feedback3 == "True":

                            f = open("Confirmed_user.txt", "w")
                            f.write(str(self.ids.username.text))
                            f.close()



                            self.ids.username.text = ''
                            self.ids.pw.text = ''

                            s.close()

                            project_5327.screen_manager.current = 'test'

                        else:
                            my_dialog = MDDialog(title="Login failed",
                                                 text="Username or Password not found/ incorrect",
                                                 )
                            my_dialog.open()
                            s.close()
                    else:
                        s.close()
                else:
                    s.close()


            except:
                my_dialog = MDDialog(title="Cannot connect server",
                                    text="Please check your input and Internet connection",
                                    )
                my_dialog.open()
                pass

        pass

class TestPage(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def update_username(self):
        f = open("Confirmed_user.txt", "r")
        self.ids.username.text = str(f.read())
        f.close()

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

        option="test"
        s.sendall((option).encode('utf-8'))

        feedback = str(s.recv(1024).decode())
        print(s.recv(1024).decode())
        s.close()

        project_5327.InfoPage.update_info(feedback)
        project_5327.screen_manager.current = 'info'

        pass

    def file_button(self):
        project_5327.screen_manager.current = 'file'
        pass

    def date_on_save(self, instance, value, date_range):
        #print(instance, value, date_range)
        self.ids.date_label.text = str(value)

    def Show_Date_Picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.date_on_save)
        date_dialog.open()

    def timeslot_on_save(self, instance):

        self.ids.time_label.text = str(instance)

    def time_slot_picker(self):
        btn1 = MDFlatButton(text="Confirm",text_color=[0, 0, 1, 0])
        btn1.bind(on_press=self.timeslot_on_save)
        my_dialog = MDDialog(
                title="Timeslot",
                type="confirmation",
                items=[
                    OneLineIconListItem(text="8am-10am",on_press=lambda x:self.timeslot_on_save('8am-10am')),
                    OneLineIconListItem(text="10am-12pm", on_press=lambda x: self.timeslot_on_save('10am-12pm')),
                    OneLineIconListItem(text="12pm-2pm", on_press=lambda x: self.timeslot_on_save('12pm-2pm')),
                    OneLineIconListItem(text="2pm-4pm", on_press=lambda x: self.timeslot_on_save('2pm-4pm')),
                    OneLineIconListItem(text="4pm-6pm", on_press=lambda x: self.timeslot_on_save('4pm-6pm')),
                    OneLineIconListItem(text="6pm-8pm", on_press=lambda x: self.timeslot_on_save('6pm-8pm')),
                    ],
                )
        my_dialog.open()
        pass


    def confirm_logout_popup(self):
        btn1 = MDFlatButton(text="Yes",text_color=[0, 0, 1, 0])
        btn1.bind(on_press=self.logout_button)
        my_dialog = MDDialog(title="Confirm Logout",
                             text="Click 'Yes' to Logout",
                             buttons=[btn1])
        my_dialog.open()
        pass

    def logout_button(self,instance):
        f = open("Confirmed_user.txt", "w")
        f.write('')
        f.close()
        self.ids.username.text = 'Please refresh this page to view the username'
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