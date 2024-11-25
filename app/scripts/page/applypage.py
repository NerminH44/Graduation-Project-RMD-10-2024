# Employee Application Page
# ---
# --------
from kivy import utils
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Rectangle
from app.scripts.popup import Support
from app.config.settings import VersionInfo
from kivy.core.window import Window

import pymssql
connection = None

def change_to_screen(*args, screen):
    """ Orders the application's screen maanger to change
      to screen given by the parameter "screen" """
    App.get_running_app().screen_manager.current = screen
    return

# Events
def about_released(instance):
    change_to_screen(screen="About Us Page")
    return

def apply_released(instance):
    App.get_running_app().apply.hirescroll.apply()
    return

def return_released(instance):
    change_to_screen(screen="Login Page")
    return

def support_released(instance):
    Support()
    return

class Scroll(ScrollView, FloatLayout):
    def apply(self):
        boxtext = [self.firstname.text, self.lastname.text,
                   self.pnumber.text, self.email.text]
        for text in boxtext:
            if (len(text) == 0):
                self.applyerror.color = "red"
                self.applyerror.text = "Kindly fill all the designated textboxes!"
                return
        try:
            global connection
            connection = pymssql.connect(
                    host='localhost',
                    user='Yousef',
                    password='123',
                    database='ElectronicsStore',
                    as_dict=True
            ) 
        except pymssql.Error as error:
            self.applyerror.color = "red"
            self.applyerror.text = str(error) if len(str(error)) < 50 else str(error)[:50] + "..."
        finally:
            cursor = connection.cursor()
            
            cursor.execute("""
                INSERT INTO employees (first_name, last_name, phone_number, email, job_id, salary, hire_date, department_id) 
                VALUES (@fname, @lname, @pnum, @email, @jobid, @sal, GETDATE(), @dept)
            """,
            fname=self.firstname.text,
            lname=self.lastname.text,
            pnum=self.pnumber.text,
            email=self.email.text,
            jobid=7,
            sal=5500,
            dept=50)

            connection.commit()
            connection.close()
            self.applyerror.color = "green"
            self.applyerror.text = "Welcome! You have been accepted!"

    def __init__(self, **kwargs):
        super(Scroll, self).__init__(**kwargs)
        scrollbox = BoxLayout(orientation="vertical", spacing=-20, padding=(360,16), size_hint_y=None)
        scrollbox.bind(minimum_height=scrollbox.setter('height'))
        # Application Data Entry:
        # ---
        # -----
        box0 = BoxLayout(size_hint_y=None)
        self.ieemslogo = Image(source="app/assets/ieemslogo.png",
                           size_hint=(1,1),
                           pos_hint={"center_y": .6})
        box0.add_widget(self.ieemslogo)
        box00 = BoxLayout(size_hint_y=None)
        message = Label(text="Welcome our  beloved employee to-be!\n"\
        +"Kindly fill the form below with your personal identification details!",
                    halign="center",
                    valign="center",
                    markup=True,
                    pos_hint={"center_y": .3},
                    text_size=(400,None),
                    color="black")
        box00.add_widget(message)
        scrollbox.add_widget(box0)
        scrollbox.add_widget(box00)
        # First Name
        box1 = BoxLayout(orientation="horizontal", size_hint_y=None)
        ficon = Image(source="app/assets/user-icon.png",
                    size_hint = (.3,.5))
        box1.add_widget(ficon)
        self.firstname = TextInput(multiline=False,
                    size_hint = (1,.3),
                    pos_hint={"center_y": .25},
                    write_tab=False,
                    hint_text = "FIRST NAME")
        box1.add_widget(self.firstname)
        scrollbox.add_widget(box1)

        # Last Name
        box2 = BoxLayout(orientation="horizontal", size_hint_y=None)
        licon = Image(source="app/assets/user-icon.png",
                    size_hint = (.3,.5))
        box2.add_widget(licon)
        self.lastname = TextInput(multiline=False,
                    size_hint = (1,.3),
                    pos_hint={"center_y": .25},
                    write_tab=False,
                    hint_text = "LAST NAME")
        box2.add_widget(self.lastname)
        scrollbox.add_widget(box2)

        # Phone Number
        box3 = BoxLayout(orientation="horizontal", size_hint_y=None)
        picon = Image(source="app/assets/phone-icon.png",
                    size_hint = (.3,.5))
        box3.add_widget(picon)
        self.pnumber = TextInput(multiline=False,
                    input_filter = 'float',
                    write_tab=False,
                    pos_hint={"center_y": .25},
                    size_hint = (1,.3),
                    hint_text = "PHONE NUMBER")
        box3.add_widget(self.pnumber)
        scrollbox.add_widget(box3)

        # Email
        box4 = BoxLayout(orientation="horizontal", size_hint_y=None)
        eicon = Image(source="app/assets/email-icon.png",
                    size_hint = (.3,.5))
        box4.add_widget(eicon)
        self.email = TextInput(multiline=False,
                    write_tab=False,
                    pos_hint={"center_y": .25},
                    size_hint = (1,.3),
                    hint_text = "EMAIL")
        box4.add_widget(self.email)
        scrollbox.add_widget(box4)

        box5 = BoxLayout(orientation="vertical", size_hint_y=None)
        self.applyerror = Label(text="",
                            halign="center",
                            color = "red",
                            size_hint=(1,1),
                            font_size=12)
        box5.add_widget(self.applyerror)
        applybut = Button(text="SIGN-UP", color = "#21d74d",
                            outline_width=2, outline_color ="#ffffff",
                            size_hint=(1,1),
                            font_size=18,
                            background_normal=
                            "app/assets/button.png",
                            background_down=
                            "app/assets/button-down.png")
        applybut.bind(on_release=apply_released)
        box5.add_widget(applybut)
        scrollbox.add_widget(box5)

        self.size_hint=(1, None)
        self.size=(Window.width, Window.height-140)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.465}
        self.bar_color = utils.get_color_from_hex("ffffff")
        self.bar_inactive_color = utils.get_color_from_hex("757575")
        self.bar_width = 10
        self.scroll_type = ['bars','content']  
        self.add_widget(scrollbox)
  
class Application(Screen, FloatLayout):
    def _update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size

    def __init__(self, **kwargs):
        super(Application, self).__init__(**kwargs)
        with self.canvas.before:
            self.bg = Rectangle(source = "app/assets/background.png",
                                size = self.size,
                                pos = self.pos)

        self.bind(size = self._update_bg, pos = self._update_bg)

        self.taskbar = FloatLayout()

        ribbon = Image(source="app/assets/ribbon-taskbar.png",
                            pos_hint={"center_x": .5, "center_y": .94})
        self.taskbar.add_widget(ribbon)

        currUser = Label(text="[b] Current User:[/b] {db}".format(db=VersionInfo.get_user()),
                             halign='center',
                             color = "#2f2f2f",
                             markup=True,
                             pos_hint={"center_x": .9, "center_y": .93}, font_size=16)
        self.taskbar.add_widget(currUser)
        
        aboutbut = Button(text="[b] ABOUT US [/b]", color = "#2f2f2f",
                            markup=True,
                            size_hint=(.12,.08),
                            font_size=16,
                            pos_hint={"center_x": .17, "center_y": .93},
                            background_normal=
                            "app/assets/invis-button.png",
                            background_down=
                            "app/assets/invis-button-down.png")
        aboutbut.bind(on_release=about_released)
        self.taskbar.add_widget(aboutbut)

        supportbut = Button(text="[b] SUPPORT [/b]", color = "#2f2f2f",
                            markup=True,
                            size_hint=(.12,.08),
                            font_size=16,
                            pos_hint={"center_x": .29, "center_y": .93},
                            background_normal=
                            "app/assets/invis-button.png",
                            background_down=
                            "app/assets/invis-button-down.png")
        supportbut.bind(on_release=support_released)
        self.taskbar.add_widget(supportbut)
        
        self.add_widget(self.taskbar)

        self.panel = Image(source="app/assets/panel-4.png",
                           pos_hint={"center_x": .5, "center_y": .465})
        self.add_widget(self.panel)
        
        self.hirescroll = Scroll()
        self.add_widget(self.hirescroll)

        returnbut = Button(size_hint=(None,None),
                           size=(75,75),
                           pos_hint={"center_x": .93, "center_y": .8},
                           background_normal="app/assets/back-icon.png",
                           background_down="app/assets/back-icon-down.png")
        returnbut.bind(on_release=return_released)
        self.add_widget(returnbut)

        self.footer = Label(text="DEPI Microsoft Data Engineer Graduation Project - ONL1_AIS4_M9e - @github.com/37743",
                             color = "##6ee58b",
                             pos_hint={"center_x": .5, "center_y": .04},
                             font_size=11)
        self.add_widget(self.footer)