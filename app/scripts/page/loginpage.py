# Login Page
# ---
# --------
# Kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Rectangle
from kivy.animation import Animation
from app.scripts.popup import Support
from app.config.settings import VersionInfo
from kivy.clock import Clock

import pymssql

connection = None

def change_to_screen(*args, screen):
    """ Changes the interface current shown to the user using Screen Manager object. """
    App.get_running_app().screen_manager.current = screen
    return

# Events
def login_success(*args):
    """ Event that is fired when the user logs in successfully. Proceeds to Inventory page with user data. """
    App.get_running_app().inventory.update_user(VersionInfo.get_user())
    change_to_screen(screen="Inventory Page")
    return

def about_released(instance):
    """ Event that is fired when the About Us button is released. """
    change_to_screen(screen="About Us Page")
    return

def apply_released(instance):
    """ Event that is fired when the Apply button is released. """
    change_to_screen(screen="Application Page")
    return

def login_released(instance):
    """ Event that is fired when the Login button is released. """
    App.get_running_app().login.db_connect()
    return

def support_released(instance):
    """ Event that is fired when the Support button is released. """
    Support()
    return

def float_effect(widget, yn, d):
    """ Floating animation that is used for some buttons, take yn, which is the distance to be covered in the y direction,
      and d, which is the duration taken to cover said distance. """
    anim = Animation(y=-yn, duration = d, t="in_out_cubic") + Animation(y=0, duration=d, t="in_out_cubic")
    anim.repeat = True
    anim.start(widget)
    return

class Login(Screen, FloatLayout):
    """ Login page logic """
    def _update_bg(self, instance, value):
        """ Resizes background(s) on window resizing event. """
        self.bg.pos = instance.pos
        self.bg.size = instance.size
    
    def db_connect(self):
        """ Connects to the database, checks if user exists and proceeds with login logic. """
        global connection
        try:
            connection = pymssql.connect(
                    host='localhost',
                    user=str(self.userBox.text).lower(),
                    password=str(self.passBox.text).lower(),
                    database='ElectronicsStore',
                    as_dict=True
                )  
            self.loginerror.color = "green"
            self.loginerror.text = "Successful Login!"
            VersionInfo.set_user(self.userBox.text)
        except pymssql.Error as error:
            self.loginerror.color = "red"
            self.loginerror.text = str(error) if len(str(error)) < 50 else str(error)[:50] + "..."
        if (connection):
            Clock.schedule_once(login_success, 2)

    def __init__(self, **kwargs):
        super(Login, self).__init__(**kwargs)
        with self.canvas.before:
            self.bg = Rectangle(source = "app/assets/background.png",
                                size = self.size,
                                pos = self.pos)

        self.bind(size = self._update_bg, pos = self._update_bg)

        # Header/Task Bar
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

        aboutusbut = Button(text="[b] ABOUT US [/b]", color = "#2f2f2f",
                            markup=True,
                            size_hint=(.12,.08),
                            font_size=16,
                            pos_hint={"center_x": .17, "center_y": .93},
                            background_normal=
                            "app/assets/invis-button.png",
                            background_down=
                            "app/assets/invis-button-down.png")
        aboutusbut.bind(on_release=about_released)
        self.taskbar.add_widget(aboutusbut)

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
        
        # Login Panel
        self.ui = FloatLayout()

        self.panel = Image(source="app/assets/panel-2.png",
                           pos_hint={"center_x": .5, "center_y": .5})
        self.ui.add_widget(self.panel)

        self.ieemslogo = Image(source="app/assets/ieemslogo.png",
                           size_hint=(.13,.13),
                           pos_hint={"center_x": .5, "center_y": .66})
        self.ui.add_widget(self.ieemslogo)

        # Username Textbox
        self.uicon = Image(source="app/assets/user-icon.png",
                    size_hint = (.08,.08),
                    pos_hint={"center_x": 0.36, "center_y": .535})
        self.ui.add_widget(self.uicon)

        self.userBox = TextInput(multiline=False,
                    size_hint = (.25,.05),
                    write_tab=False,
                    hint_text = "USERNAME",
                    pos_hint = {"center_x": .52, "center_y": .535})
        self.ui.add_widget(self.userBox)

        # Password Textbox
        self.picon = Image(source="app/assets/password-icon.png",
                    size_hint = (.08,.08),
                    pos_hint={"center_x": 0.36, "center_y": .435})
        self.ui.add_widget(self.picon)
        self.passBox = TextInput(multiline=False,
                    size_hint = (.25,.05),
                    write_tab=False,
                    password = True,
                    hint_text = "PASSWORD",
                    pos_hint = {"center_x": .52, "center_y": .435}) 
        self.ui.add_widget(self.passBox)

        loginbut = Button(text="LOGIN", color = "#21d74d",
                            outline_width=2, outline_color ="#ffffff",
                            size_hint=(.16,.08),
                            font_size=18,
                            pos_hint={"center_x": .5, "center_y": .325},
                            background_normal=
                            "app/assets/button.png",
                            background_down=
                            "app/assets/button-down.png")
        loginbut.bind(on_release=login_released)
        self.ui.add_widget(loginbut)
        
        self.loginerror = Label(text="",
                                halign="center",
                                color = "red",
                                pos_hint={"center_x": .5, "center_y": .385}, font_size=12)
        self.ui.add_widget(self.loginerror)

        # Hiring Panel
        self.hireui = FloatLayout()
        self.hirepanel = Image(source="app/assets/panel-2.png",
                                size_hint=(.3,.2),
                                pos_hint={"center_x": .9, "center_y": .15})
        self.hireui.add_widget(self.hirepanel)

        hirebut = Button(text="APPLY", color = "#21d74d",
                            outline_width=2, outline_color ="#ffffff",
                            size_hint=(.15,.08),
                            font_size=18,
                            pos_hint={"center_x": .9, "center_y": .1},
                            background_normal=
                            "app/assets/button.png",
                            background_down=
                            "app/assets/button-down.png")
        hirebut.bind(on_release=apply_released)
        self.hireui.add_widget(hirebut)
        
        hirejobs = Label(text="[b] Hiring Employees \n&\n Workers! [/b]",
                             halign='center',
                             color = "#2f2f2f",
                             markup=True,
                             pos_hint={"center_x": .9, "center_y": .19}, font_size=16)
        self.hireui.add_widget(hirejobs)
        
        float_effect(self.hireui, -10, 2)
        self.add_widget(self.ui)
        self.add_widget(self.hireui)
        self.add_widget(self.taskbar)

        # Footer
        self.footer = Label(text="DEPI Microsoft Data Engineer Graduation Project - ONL1_AIS4_M9e - @github.com/37743",
                             color = "##6ee58b",
                             pos_hint={"center_x": .5, "center_y": .04}, font_size=11)
        self.add_widget(self.footer)