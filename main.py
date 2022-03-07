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
from kivymd.uix.list import OneLineAvatarIconListItem, OneLineIconListItem,OneLineListItem, TwoLineListItem
from datetime import datetime

#Window.size = (1000, 1000)
import socket
kivy.require("2.0.0")

confirmed_username = ''
confirmed_address = ''
confirmed_port = ''

class StartPage (GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start_button(self):

        project_5327.screen_manager.current = 'login'



class LoginPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


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

                            global confirmed_username
                            confirmed_username = str(self.ids.username.text)

                            self.ids.username.text = ''
                            self.ids.pw.text = ''

                            s.close()

                            global confirmed_address
                            global confirmed_port

                            confirmed_address = input_address
                            confirmed_port = input_port

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

        global confirmed_username
        self.ids.username.text = str(confirmed_username)

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
        self.ids.time_label.text = 'Selected Timeslot: N/A'
        self.ids.slot_id_label.text = ''

    def Show_Date_Picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.date_on_save)
        date_dialog.open()

    def timeslot_on_save(self, instance, instance2):

        self.ids.time_label.text = str(instance)
        self.ids.slot_id_label.text = str("ID: "+instance2)
    def time_slot_picker(self):

        if self.ids.date_label.text != "Selected Date: N/A":
            try:
                s = socket.socket()

                global confirmed_port
                global confirmed_address

                port = int(confirmed_port)
                full_address = str(confirmed_address) + '.tcp.ngrok.io'
                s.connect((full_address, port))

                option = "timeslot_display"
                s.sendall((option).encode('utf-8'))

                feedback = str(s.recv(1024).decode('utf-8'))
                if feedback == "OK":
                    date_option = str(self.ids.date_label.text)
                    s.sendall((date_option).encode('utf-8'))
                    feedback_timeslot = str(s.recv(1024).decode('utf-8'))
                    s.close()

                    print(feedback_timeslot)

                    i=0
                    var_order = 1
                    location_a = 0
                    location_b = 0

                    slot_id_list = []
                    time_slot_list = []

                    while i < len(feedback_timeslot):

                        if feedback_timeslot[i] == ':' and var_order == 1:
                            location_a = i
                        elif feedback_timeslot[i] == ',' and var_order == 1:
                            location_b = i
                            var_order = 2
                            slot_id_list.append(feedback_timeslot[location_a+2:location_b])

                        elif feedback_timeslot[i] == ':' and var_order == 2:
                            location_a = i
                        elif feedback_timeslot[i] == '}' and var_order == 2:
                            location_b = i
                            var_order = 1
                            time_slot_list.append(feedback_timeslot[location_a + 3:location_b - 1])
                        i+=1

                    if slot_id_list == [] or time_slot_list == []:
                        my_dialog = MDDialog(title="Full booking",
                                             text="Please select another date",
                                             )
                        my_dialog.open()
                    else:

                        i = 0
                        option_list = []

                        while i < len(time_slot_list):
                            option_str_timeslot = str(time_slot_list[i])
                            option_str_id = str(slot_id_list[i])
                            f = lambda x, option_str_timeslot=option_str_timeslot, option_str_id=option_str_id: self.timeslot_on_save(option_str_timeslot,option_str_id)
                            option_list.append(OneLineIconListItem(text= option_str_timeslot, on_release=f))
                            i+=1


                        my_dialog = MDDialog(
                            title="Timeslot",
                            type="confirmation",
                            items=option_list,
                        )
                        my_dialog.open()

                else:
                    s.close()

            except:
                my_dialog = MDDialog(title="Cannot connect server",
                                     text="Please check your input and Internet connection",
                                     )
                my_dialog.open()
                pass

        else:
            my_dialog = MDDialog(title="Date not found",
                                 text="Please select date to continue")
            my_dialog.open()
            pass


    def confirm_booking(self):
        if self.ids.slot_id_label.text == '':
            my_dialog = MDDialog(title="Error",
                                 text="Please select date and timeslot to continue",
                                 )
            my_dialog.open()
            pass
        else:

            try:
                s = socket.socket()

                global confirmed_port
                global confirmed_address

                port = int(confirmed_port)
                full_address = str(confirmed_address) + '.tcp.ngrok.io'
                s.connect((full_address, port))

                option = "confirm_booking"
                s.sendall((option).encode('utf-8'))

                feedback = str(s.recv(1024).decode('utf-8'))
                if feedback == "OK":
                    selected_id = str(self.ids.slot_id_label.text)[4:]
                    s.sendall((selected_id).encode('utf-8'))

                    feedback2 = str(s.recv(1024).decode('utf-8'))
                    if feedback2 == 'id received':
                        global confirmed_username
                        s.sendall((confirmed_username).encode('utf-8'))

                        feedback3 = str(s.recv(1024).decode('utf-8'))
                        s.close()

                        if feedback3 == "full":
                            my_dialog = MDDialog(title="Full booking",
                                                text="Please select another date or timeslot",
                                                )
                            my_dialog.open()

                        elif feedback3 == "already":
                            my_dialog = MDDialog(title='Error',
                                                 text="You have already reserved this timeslot",
                                                 )
                            my_dialog.open()

                        elif feedback3 == "done":
                            my_dialog = MDDialog(title="Success",
                                                 text="You can check the reservation record in History page",
                                                 )
                            my_dialog.open()
                        self.ids.date_label.text = 'Selected Date: N/A'
                        self.ids.time_label.text = 'Selected Timeslot: N/A'
                        self.ids.slot_id_label.text = ''
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

    def cancel_booking(self,option_booking,option_slot_id,option_apply_date,option_date,option_time):
        now = datetime.now()
        current_date = str(now.strftime("%Y-%m-%d"))

        print("print")
        if int(current_date[:4]) <= int(option_date[:4]):

            if int(current_date[4:7]) <= int(option_date[4:7]):


                if int(current_date[8:10]) <= int(option_date[8:10]):
                    try:
                        s = socket.socket()

                        global confirmed_port
                        global confirmed_address

                        port = int(confirmed_port)
                        full_address = str(confirmed_address) + '.tcp.ngrok.io'
                        s.connect((full_address, port))

                        option = "cancel_booking"
                        s.sendall((option).encode('utf-8'))

                        feedback = str(s.recv(1024).decode('utf-8'))
                        if feedback == "OK":
                            s.sendall((option_booking).encode('utf-8'))
                            cancel_feedback = str(s.recv(1024).decode('utf-8'))

                            if cancel_feedback == 'Done':
                                my_dialog = MDDialog(title="Booking Canceled",
                                                     text="Refresh this page to view your booking",
                                                     )
                                my_dialog.open()
                                s.close()
                            elif cancel_feedback == 'already':
                                my_dialog = MDDialog(title="Booking Canceled Before",
                                                     text="Refresh this page to view your booking",
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



                else:
                    my_dialog = MDDialog(title="Error",
                                         text='Cancel booking period expired')
                    my_dialog.open()
            else:
                my_dialog = MDDialog(title="Error",
                                     text='Cancel booking period expired')
                my_dialog.open()
        else:
            my_dialog = MDDialog(title="Error",
                                 text='Cancel booking period expired')
            my_dialog.open()

        '''
        print(current_date[:4])
        print(option_date[:4])

        print(option_date[5:7])
        print(option_date[8:10])
        '''
        pass
    def booking_history_popup(self,option_booking,option_slot_id,option_apply_date,option_date,option_time):
        btn1 = MDFlatButton(text="Cancel Booking", text_color=[0, 0, 1, 0])
        btn1.bind(on_press=lambda x: self.cancel_booking(option_booking,option_slot_id,option_apply_date,option_date,option_time))
        my_dialog = MDDialog(title="Reservation Details",
                             text="Booking ID: "+option_booking+"\nSlot ID: "+option_slot_id+"\nDate: "+option_date+"\nTime: "+option_time+"\nApply time: "+option_apply_date,
                             buttons=[btn1])
        my_dialog.open()

    def cancel_history_popup(self, option_booking, option_slot_id, option_apply_date, option_date, option_time, option_cancel_date):

        my_dialog = MDDialog(title="Reservation Details",
                             text="Booking ID: " + option_booking + "\nSlot ID: " + option_slot_id + "\nDate: " + option_date + "\nTime: " + option_time + "\nApply time: " + option_apply_date + "\nCanceled time: " + option_cancel_date)
        my_dialog.open()

    def booking_history(self,input):
        try:
            s = socket.socket()

            global confirmed_port
            global confirmed_address

            port = int(confirmed_port)
            full_address = str(confirmed_address) + '.tcp.ngrok.io'
            s.connect((full_address, port))

            option = "booking_history"
            s.sendall((option).encode('utf-8'))

            feedback = str(s.recv(1024).decode('utf-8'))
            if feedback == "OK":
                global confirmed_username

                s.sendall((confirmed_username).encode('utf-8'))

                feedback_history = str(s.recv(1024).decode('utf-8'))
                s.close()


                i = 0
                var_order=1
                a_or_b = 1
                done= False
                location_a = 0
                location_b = 0

                booking_id_list=[]
                slot_id_list=[]
                apply_date_list=[]
                date_list=[]
                time_slot_list=[]
                cancel_list=[]
                cancel_date_list=[]
                while i < len(feedback_history):
                    if feedback_history[i] == ':' and var_order == 1 and a_or_b == 1:
                        location_a = i
                        a_or_b = 2
                    elif feedback_history[i] == ',' and var_order == 1 and a_or_b == 2:
                        location_b = i
                        a_or_b = 1
                        done = True
                        booking_id_list.append(feedback_history[location_a + 2:location_b])

                    if feedback_history[i] == ':' and var_order == 2 and a_or_b == 1:
                        location_a = i
                        a_or_b = 2
                    elif feedback_history[i] == ',' and var_order == 2 and a_or_b == 2:
                        location_b = i
                        a_or_b = 1
                        done = True
                        slot_id_list.append(feedback_history[location_a + 2:location_b])

                    if feedback_history[i] == ':' and var_order == 3 and a_or_b == 1:
                        location_a = i
                        a_or_b = 2
                    elif feedback_history[i] == ',' and var_order == 3 and a_or_b == 2:
                        location_b = i
                        a_or_b = 1
                        done = True
                        apply_date_list.append(feedback_history[location_a+3:location_b-1])

                    if feedback_history[i] == ':' and var_order == 4 and a_or_b == 1:
                        location_a = i
                        a_or_b = 2
                    elif feedback_history[i] == ',' and var_order == 4 and a_or_b == 2:
                        location_b = i
                        a_or_b = 1
                        done = True
                        date_list.append(feedback_history[location_a+3:location_b-1])

                    elif feedback_history[i] == ':' and var_order == 5 and a_or_b == 1:
                        location_a = i
                        a_or_b = 2
                    elif feedback_history[i] == ',' and var_order == 5 and a_or_b == 2:
                        location_b = i
                        a_or_b = 1
                        done = True
                        time_slot_list.append(feedback_history[location_a + 3:location_b - 1])

                    elif feedback_history[i] == ':' and var_order == 6 and a_or_b == 1:
                        location_a = i
                        a_or_b = 2
                    elif feedback_history[i] == ',' and var_order == 6 and a_or_b == 2:
                        location_b = i
                        a_or_b = 1
                        done = True
                        cancel_list.append(feedback_history[location_a + 3:location_b - 1])

                    elif feedback_history[i] == ':' and var_order == 7 and a_or_b == 1:
                        location_a = i
                        a_or_b = 2
                    elif feedback_history[i] == '}' and var_order == 7 and a_or_b == 2:
                        location_b = i
                        a_or_b = 1
                        done = True
                        cancel_date_list.append(feedback_history[location_a + 3:location_b - 1])


                    if var_order == 7 and a_or_b == 1 and done == True:
                        var_order = 1
                        done = False
                    elif var_order < 7 and a_or_b == 1 and done == True:
                        var_order += 1
                        done = False

                    i += 1


                print("print")
                print(booking_id_list)
                print(slot_id_list)
                print(apply_date_list)
                print(date_list)
                print(time_slot_list)
                print(cancel_list)
                print(cancel_date_list)
                print(input)

                x=0
                self.ids.history.clear_widgets()
                self.ids.cancel_list.clear_widgets()
                while x < len(booking_id_list):
                    option_booking = booking_id_list[x]
                    option_slot_id = slot_id_list[x]
                    option_apply_date = apply_date_list[x]
                    option_date = date_list[x]
                    option_time = time_slot_list[x]
                    option_cancel_date = cancel_date_list[x]

                    f = lambda y, option_booking=option_booking, option_slot_id=option_slot_id, option_apply_date=option_apply_date, option_date=option_date, option_time=option_time: self.booking_history_popup(option_booking,option_slot_id,option_apply_date,option_date,option_time)
                    f2 = lambda y, option_booking=option_booking, option_slot_id=option_slot_id,option_apply_date=option_apply_date, option_date=option_date, option_time=option_time, option_cancel_date=option_cancel_date : self.cancel_history_popup(option_booking, option_slot_id,option_apply_date, option_date,option_time,option_cancel_date)

                    if str(cancel_list[x]) == '' and input == "history":
                        self.ids.history.add_widget(TwoLineListItem(text="Date & Timeslot: "+str(date_list[x]+" "+str(time_slot_list[x])),secondary_text="Booking ID: "+str(booking_id_list[x]), on_release=f))
                    elif str(cancel_list[x]) != '' and input == "cancel":
                        self.ids.cancel_list.add_widget(TwoLineListItem(text="Date & Timeslot: " + str(date_list[x] + " " + str(time_slot_list[x])),secondary_text="Booking ID: " + str(booking_id_list[x]), on_release=f2))

                    x+=1

            else:
                s.close()

        except:
            my_dialog = MDDialog(title="Cannot connect server",
                                 text="Please check your input and Internet connection",
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

        global confirmed_username
        confirmed_username = ''
        self.ids.username.text = 'Please refresh this page to view the username'
        self.ids.date_label.text = 'Selected Date: N/A'
        self.ids.time_label.text = 'Selected Timeslot: N/A'
        self.ids.slot_id_label.text = ''

        project_5327.screen_manager.current = 'start'
        pass


class FilePage(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def back_button(self):
        project_5327.screen_manager.current = 'test'
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

        self.TestPage = TestPage()
        screen = Screen(name='test')
        screen.add_widget(self.TestPage)
        self.screen_manager.add_widget(screen)

        return self.screen_manager




if __name__ == "__main__":
    project_5327 = ProjectApp()
    project_5327.run()