# About Us Page
# ---
# --------
from kivy import utils
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Rectangle
from app.scripts.popup import Support
from app.config.settings import VersionInfo
from kivy.core.window import Window

def change_to_screen(*args, screen):
    App.get_running_app().screen_manager.current = screen
    return

# Events
def loginpg_released(instance):
    change_to_screen(screen="Login Page")
    return

def signup_released(instance):
    change_to_screen(screen="Signup Page")
    return

def support_released(instance):
    Support()
    return

class About(Screen, FloatLayout):
    def _update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size

    def __init__(self, **kwargs):
        super(About, self).__init__(**kwargs)
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

        loginpgbut = Button(text="[b] LOGIN [/b]", color = "#2f2f2f",
                            markup=True,
                            size_hint=(.12,.08),
                            font_size=16,
                            pos_hint={"center_x": .17, "center_y": .93},
                            background_normal=
                            "app/assets/invis-button.png",
                            background_down=
                            "app/assets/invis-button-down.png")
        loginpgbut.bind(on_release=loginpg_released)
        self.taskbar.add_widget(loginpgbut)

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
        self.add_widget(Scroll())

        self.footer = Label(text="DEPI Microsoft Data Engineer Graduation Project - ONL1_AIS4_M9e - @github.com/37743",
                             color = "##6ee58b",
                             pos_hint={"center_x": .5, "center_y": .04},
                             font_size=11)
        self.add_widget(self.footer)

# TODO: Fix the scrolling
class Scroll(ScrollView, FloatLayout):
    def __init__(self, **kwargs):
        super(Scroll, self).__init__(**kwargs)
        # grid = GridLayout(cols=1, size_hint_y=None)
        # grid.bind(minimum_height=grid.setter('height'))
        introlayout = FloatLayout()
        intropanel = Image(source="app/assets/intro.png", size_hint=(1,1))
        introlayout.add_widget(intropanel)
        welcome = Label(text="[b] Electronics Inventory Management System [/b]",
                             color = "#21d74d", markup = True,
                             halign="center",
                             valign="center",
                             size_hint=(1,1),
                             pos_hint={"center_x": .67, "center_y": .85},
                             font_size=26)
        introlayout.add_widget(welcome)
        intro1 = Label(text="[b] \"A system for managing the inventory of electronic\n devices through an website interface.\" [/b]",
                             color = "#ffffff", markup = True,
                             size_hint=(1,1),
                             pos_hint={"center_x": .63, "center_y": .7},
                             font_size=18)
        introlayout.add_widget(intro1)
        intro2 = Label(text="The purpose of the Electronic Devices Inventory Management System\n\
                        is to provide an comprehensive and user-friendly solution\n\
                        for efficiently managing the inventory of electronic devices\n\
                        within a retail or distribution environment.\n\
                        It aims to streamline inventory-related operations, enhance the sales process, improve\n\
                       inventory accuracy, and provide valuable insights for data-driven decision-making.",
                             color = "#ffffff",
                             size_hint=(1,1),
                             halign='justify',
                             pos_hint={"center_x": .7, "center_y": .5},
                             font_size=14)
        introlayout.add_widget(intro2)
        intro3 = Label(text="[b] If you wish to sign-up for our services, [u] kindly press the button\n\
                        below and follow the instructions given. [/u] [/b]",
                             color = "#ffffff",
                             size_hint=(1,1),
                             halign='justify',
                             markup = True,
                             pos_hint={"center_x": .632, "center_y": .35},
                             font_size=14)
        introlayout.add_widget(intro3)
        signupbut = Button(text="SIGN-UP", color = "#21d74d",
                            outline_width=2, outline_color ="#ffffff",
                            size_hint=(.16,.08),
                            font_size=18,
                            pos_hint={"center_x": .68, "center_y": .25},
                            background_normal=
                            "app/assets/button.png",
                            background_down=
                            "app/assets/button-down.png")
        signupbut.bind(on_release=signup_released)
        introlayout.add_widget(signupbut)
        # grid.add_widget(introlayout)
        self.size_hint=(1, None)
        self.size=(Window.width, Window.height-90)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.465}
        self.bar_color = utils.get_color_from_hex("ffffff")
        self.bar_inactive_color = utils.get_color_from_hex("757575")
        self.bar_width = 15
        self.scroll_type = ['bars','content']  
        self.add_widget(introlayout)