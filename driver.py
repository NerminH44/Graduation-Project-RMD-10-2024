# Electronics Inventory Management System for Suppliers
# Driver Code
# ---
import kivy
kivy.require('2.2.0')

# Kivy Packages
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, WipeTransition
from app.config import settings
from app.scripts.page import loginpage
from app.scripts.page import aboutpage
from app.scripts.page import signuppage
from app.scripts.page import applypage
from app.scripts.page import inventorypage
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,disable_multitouch') # Disables graphical annotation
from kivy.core.window import Window
# Window settings, resizable
Window.size = (1024, 640)
Window.minimum_width = 768
Window.minimum_height = 512

class App(App):
    ''' Driver code for the application, contains a screen manager
    which controls which interface is shown to the user at a time.'''
    def build(self):
        self.title = settings.VersionInfo.get_title()
        self.icon = "app/assets/ieemslogo.png"
        self.about = aboutpage.About(name="About Us Page")
        self.login = loginpage.Login(name="Login Page")
        self.inventory = inventorypage.Inventory(name="Inventory Page")
        self.signup = signuppage.Signup(name="Signup Page")
        self.apply = applypage.Application(name="Application Page")
        self.screen_manager = ScreenManager(transition = WipeTransition())

        for screen in [self.about,
                       self.login,
                       self.inventory,
                       self.signup,
                       self.apply
                    ]:
            self.screen_manager.add_widget(screen)
        return self.screen_manager

if __name__ == '__main__':  
    main = App()
    main.run()