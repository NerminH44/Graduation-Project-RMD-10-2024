# Sign-up Page
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
from app.scripts.popup import SignedUp
from app.config.settings import VersionInfo
from kivy.core.window import Window

import pymssql
connection = None

def change_to_screen(*args, screen):
    App.get_running_app().screen_manager.current = screen
    return

# Events
def signup_success(user):
    SignedUp(user)
    return

def signup_released(instance):
    App.get_running_app().signup.signupscroll.signup()
    return

def loginpg_released(instance):
    change_to_screen(screen="Login Page")
    return

def return_released(instance):
    change_to_screen(screen="About Us Page")
    return

def support_released(instance):
    Support()
    return


class Scroll(ScrollView, FloatLayout):
    def signup(self):
        boxtext = [
            self.location.text, 
            self.password.text, 
            self.city.text,
            self.postalcode.text, 
            self.pnumber.text, 
            self.email.text,
            self.firstname.text, 
            self.lastname.text
        ]

        for text in boxtext:
            if len(text) == 0:
                self.signuperror.color = "red"
                self.signuperror.text = "Kindly fill all the designated textboxes!"
                return

        cursor = None
        transaction_started = False  # Track if a transaction has started

        try:
            global connection
            connection = pymssql.connect(
                host='localhost',
                user='Yousef',
                password='123',
                database='ElectronicsStore',
            )
            cursor = connection.cursor()

            # Begin a transaction
            cursor.execute("BEGIN TRANSACTION")
            transaction_started = True  # Mark that the transaction has started

            # Insert new location
            cursor.execute("""
                INSERT INTO locations (location_name, city, postal_code) 
                VALUES (%s, %s, %s)
            """, (self.location.text, self.city.text, self.postalcode.text))

            # Get the newly inserted location_id
            cursor.execute("""
                SELECT location_id 
                FROM locations 
                WHERE location_name = %s
            """, (self.location.text,))
            location_id = cursor.fetchone()[0]

            # Insert new retailer
            cursor.execute("""
                INSERT INTO retailers (first_name, last_name, phone_number, email, location_id) 
                VALUES (%s, %s, %s, %s, %s)
            """, (self.firstname.text, self.lastname.text, self.pnumber.text, self.email.text, location_id))

            # Create SQL Server login
            username = self.location.text.replace(" ", "_").lower()
            cursor.execute(f"""
                CREATE LOGIN [{username}] WITH PASSWORD = '{self.password.text}';
            """)

            # Add user to retailer role
            cursor.execute(f"""
                EXEC sp_addrolemember 'retailer', '{username}';
            """)

            # If all commands succeed, commit the transaction
            cursor.execute("COMMIT TRANSACTION")

            # Success message
            self.signuperror.color = "green"
            self.signuperror.text = "Successful Sign-up!"
            signup_success(username)

        except pymssql.Error as error:
            print(f"Error occurred: {error}")
            self.signuperror.color = "red"
            self.signuperror.text = str(error) if len(str(error)) < 50 else str(error)[:50] + "..."

            # Rollback in case of error only if a transaction was started
            if transaction_started:
                cursor.execute("ROLLBACK TRANSACTION")

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    def __init__(self, **kwargs):
        super(Scroll, self).__init__(**kwargs)
        scrollbox = BoxLayout(orientation="vertical", spacing=-20, padding=(360,16), size_hint_y=None)
        scrollbox.bind(minimum_height=scrollbox.setter('height'))
        # Retailer Data Entry:
        # ---
        # -----
        box0 = BoxLayout(size_hint_y=None)
        self.ieemslogo = Image(source="app/assets/ieemslogo.png",
                           size_hint=(1,1),
                           pos_hint={"center_y": .6})
        box0.add_widget(self.ieemslogo)
        box00 = BoxLayout(size_hint_y=None)
        message = Label(text="Note that you are signing up with our company\n [i] (Electronics Inventory Management System)"\
                        +"[/i]\n as a contracted retailer. Kindly provide your store's location along with your [u]manager's identification information.[/u]\n"\
                            +"[b]Carefully revise your credentials before submitting![/b]",
                    halign="center",
                    valign="center",
                    markup=True,
                    pos_hint={"center_y": .3},
                    text_size=(400,None),
                    color="black")
        box00.add_widget(message)
        scrollbox.add_widget(box0)
        scrollbox.add_widget(box00)

        # Location Name
        box4 = BoxLayout(orientation="horizontal", size_hint_y=None)
        sicon = Image(source="app/assets/store-icon.png",
                    size_hint = (.3,.5))
        box4.add_widget(sicon)
        self.location = TextInput(multiline=False,
                    write_tab=False,
                    pos_hint={"center_y": .25},
                    size_hint = (1,.3),
                    hint_text = "STORE NAME")
        box4.add_widget(self.location)
        scrollbox.add_widget(box4)

        # Password
        box10 = BoxLayout(orientation="horizontal", size_hint_y=None)
        pwicon = Image(source="app/assets/password-icon.png",
                    size_hint = (.3,.5))
        box10.add_widget(pwicon)
        self.password = TextInput(multiline=False,
                    write_tab=False,
                    password = True,
                    pos_hint={"center_y": .25},
                    size_hint = (1,.3),
                    hint_text = "PASSWORD")
        box10.add_widget(self.password)
        scrollbox.add_widget(box10)
        
        
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
                    input_filter = 'int',
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

        # City
        box5 = BoxLayout(orientation="horizontal", size_hint_y=None)
        cicon = Image(source="app/assets/city-icon.png",
                    size_hint = (.3,.5))
        box5.add_widget(cicon)
        self.city = TextInput(multiline=False,
                    write_tab=False,
                    pos_hint={"center_y": .25},
                    size_hint = (1,.3),
                    hint_text = "CITY")
        box5.add_widget(self.city)
        scrollbox.add_widget(box5)

        # Postal Code
        box6 = BoxLayout(orientation="horizontal", size_hint_y=None)
        pcicon = Image(source="app/assets/postalcode-icon.png",
                    size_hint = (.3,.5))
        box6.add_widget(pcicon)
        self.postalcode = TextInput(multiline=False,
                    write_tab=False,
                    input_filter = 'int',
                    pos_hint={"center_y": .25},
                    size_hint = (1,.3),
                    hint_text = "POSTAL CODE")
        box6.add_widget(self.postalcode)
        scrollbox.add_widget(box6)

        # Sign-up Button
        box7 = BoxLayout(orientation="vertical", size_hint_y=None)
        self.signuperror = Label(text="",
                            halign="center",
                            color = "red",
                            size_hint=(1,1),
                            font_size=12)
        box7.add_widget(self.signuperror)
        self.signupbut = Button(text="SIGN-UP", color = "#21d74d",
                            outline_width=2, outline_color ="#ffffff",
                            size_hint=(1,1),
                            font_size=18,
                            background_normal=
                            "app/assets/button.png",
                            background_down=
                            "app/assets/button-down.png")
        self.signupbut.bind(on_release=signup_released)
        box7.add_widget(self.signupbut)
        scrollbox.add_widget(box7)

        self.size_hint=(1, None)
        self.size=(Window.width, Window.height-140)
        self.pos_hint = {'center_x': 0.5, 'center_y': 0.465}
        self.bar_color = utils.get_color_from_hex("ffffff")
        self.bar_inactive_color = utils.get_color_from_hex("757575")
        self.bar_width = 10
        self.scroll_type = ['bars','content']  
        self.add_widget(scrollbox)
  
class Signup(Screen, FloatLayout):
    def _update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size
        
    def __init__(self, **kwargs):
        super(Signup, self).__init__(**kwargs)
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

        self.panel = Image(source="app/assets/panel-4.png",
                           pos_hint={"center_x": .5, "center_y": .465})
        self.add_widget(self.panel)
        
        self.signupscroll = Scroll()
        self.add_widget(self.signupscroll)

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