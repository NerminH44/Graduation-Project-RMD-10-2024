# Inventory Page
# ---
# --------
from kivy import utils
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.graphics import Rectangle
from app.scripts.popup import Support
from app.scripts.popup import Purchased
from app.scripts.popup import Orders
from app.config.settings import VersionInfo
from functools import partial
from kivy.core.window import Window

import pymssql

connection = None

def change_to_screen(*args, screen):
    App.get_running_app().screen_manager.current = screen
    return

# Events
def logout_released(instance):
    change_to_screen(screen="Login Page")
    return

def orders_released(instance):
    App.get_running_app().inventory.list_orders()
    return

def purchase_released(instance):
    success = App.get_running_app().inventory.change_stock()
    print(success)
    if (success == 0):
        Purchased()
    return

def add_released(instance, sku, name, idx):
    quantity = App.get_running_app().inventory.inventoryscroll.productList[idx].quantityinput.text
    if (quantity != ""):
        if (int(quantity) > 0):
            App.get_running_app().inventory.add_product(sku, name, quantity)
    return

def support_released(instance):
    Support()
    return

class Product(BoxLayout, FloatLayout):
    def __init__(self, product, idx, **kwargs):
        super(Product, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 20

        # Product Image
        self.productimg = Image(source = "app/assets/products/sku_"+str(product['SKU'])+".jpg",
                    pos_hint = {'center_x':.5,'center_y':.5},
                    height = 180,
                    size_hint_y=None)
        # Product Name Label
        self.productname = Label(text = product['product_name'],
                    color = "#2f2f2f",
                    font_size = 16,
                    pos_hint = {'center_x': .5,'center_y':.5},
                    halign = 'center')
        # Price Tag Label
        self.productprice = Label(text = "Quantity: {q} - Price: £{p}".format(q=product['Stock_quantity'],p=product['unit_price']),
                    color = "red",
                    font_size = 16,
                    pos_hint = {'center_x': .5,'center_y':.5},
                    halign = 'center')

        # Add Button
        addlayout = BoxLayout(orientation="horizontal", spacing=10, size_hint_y=None)
        self.quantityinput = TextInput(multiline=False,
                    size_hint = (1,.3),
                    input_filter = 'int',
                    pos_hint={"center_y": .5},
                    write_tab=False,
                    hint_text = "QUANTITY")
        addlayout.add_widget(self.quantityinput)
        self.addbut = Button(text="Add", color = "#21d74d",
                            outline_width=2, outline_color ="#ffffff",
                            size_hint=(.6, .65),
                            pos_hint={"center_y": .5},
                            font_size=18,
                            background_normal=
                            "app/assets/empty-icon.png",
                            background_down=
                            "app/assets/empty-icon-down.png")
        addlayout.add_widget(self.addbut)
        self.addbut.bind(on_release=partial(add_released,
                                            sku=product['SKU'],
                                            name=str(product['product_name'][:10])+"...",
                                            idx=idx))
        # Adding all widgets
        self.add_widget(self.productimg)
        self.add_widget(self.productname)
        self.add_widget(self.productprice)
        self.add_widget(addlayout)

class Scroll(ScrollView, FloatLayout):
    def get_products(self):
        global connection
        connection = pymssql.connect(
                    host='localhost',
                    user='Yousef',
                    password='123',
                    database='ElectronicsStore',
                    as_dict=True
                ) 
        cursor = connection.cursor()
        try:
            cursor.execute("""SELECT * FROM products""")
            results = cursor.fetchall()
            connection.close()
            return results
        except pymssql.Error as error:
            print(error)

    def __init__(self, **kwargs):
        super(Scroll, self).__init__(**kwargs)
        scrollbox = GridLayout(cols=2, spacing=(150,350), padding=(150,320), size_hint_y=None)
        scrollbox.bind(minimum_height=scrollbox.setter('height'))

        # Data Query
        self.productList = []
        for idx,product in enumerate(self.get_products()):
            print(product)
            currProduct = Product(product, idx)
            self.productList.append(currProduct)
            scrollbox.add_widget(currProduct)

        self.size_hint=(.8, None)
        self.size=(Window.width, Window.height-140)
        self.pos_hint = {'center_x': 0.4, 'center_y': 0.465}
        self.bar_color = utils.get_color_from_hex("ffffff")
        self.bar_inactive_color = utils.get_color_from_hex("757575")
        self.bar_width = 10
        self.scroll_type = ['bars','content']  
        self.add_widget(scrollbox)
  
class Inventory(Screen, FloatLayout):
    def _update_bg(self, instance, value):
        self.bg.pos = instance.pos
        self.bg.size = instance.size
    
    def update_user(self, new_user):
        self.currUser.text = "[b]Current User:[/b] {db}".format(db=new_user)

    def list_orders(self):
        global connection
        username = str(App.get_running_app().login.userBox.text).lower()
        password = str(App.get_running_app().login.passBox.text).lower()
        connection = pymssql.connect(
                    host='localhost',
                    user=username,
                    password=password,
                    database='ElectronicsStore',
                    as_dict=True
        ) 
        cursor = connection.cursor()
        try:
            location_name = self.currUser.text[21:]
            cursor.execute("""
                SELECT retailer_id 
                FROM retailers 
                INNER JOIN locations ON retailers.location_id = locations.location_id
                WHERE REPLACE(LOWER(location_name), ' ', '_') = %s
            """, (location_name,))

            retailer_id = cursor.fetchone()[0]

            cursor.execute("""
                SELECT * 
                FROM orders 
                WHERE retailer_id = %s AND order_status = 'Pending'
            """, (retailer_id,))

            retailer_orders = cursor.fetchall()
            connection.commit()
            connection.close()
            Orders(retailer_orders, username, password)
        except pymssql.Error as error:
            print(error)

    def change_stock(self):
        if (len(self.orders) == 0):
            return 1
        global connection
        username = str(App.get_running_app().login.userBox.text).lower()
        password = str(App.get_running_app().login.passBox.text).lower()
        connection = pymssql.connect(
                    host='localhost',
                    user=username,
                    password=password,
                    database='ElectronicsStore',
                    as_dict=True
        ) 
        cursor = connection.cursor()
        try:
            location_name = self.currUser.text[21:]
            cursor.execute("""
                SELECT retailer_id 
                FROM retailers 
                INNER JOIN locations ON retailers.location_id = locations.location_id
                WHERE REPLACE(LOWER(location_name), ' ', '_') = %s
            """, (location_name,))

            retailer_id = cursor.fetchone()
            print(retailer_id)

            cursor.execute("SET IDENTITY_INSERT orders ON;")

            for order in self.orders:
                sku = order[0]
                quantity = order[1]
                
                cursor.execute("""
        INSERT INTO orders (order_date, sku, quantity, shipment_id, retailer_id, employee_id, payment_id, order_status)
        VALUES (GETDATE(), %s, %s,
                NEXT VALUE FOR shipments_shipment_id_seq, %s, 
                21, NEXT VALUE FOR ems.payments_payment_id_seq, %s)
    """, (order[0], order[1], retailer_id, 'Pending'))

                cursor.execute("""
                    UPDATE products 
                    SET stock_quantity = stock_quantity - %s
                    WHERE sku = %s
                """, (quantity, sku))

            cursor.execute("SET IDENTITY_INSERT orders OFF;")
            self.orders=[]
            widgets = [i for i in self.orderlayout.children]
            for currWidget in widgets:
                self.orderlayout.remove_widget(currWidget)
            connection.close()
        except pymssql.Error as error:
            print(error)
        return 0
    
    def add_product(self, sku, name, quantity):
        order = [sku, quantity, Button(text="[b] {n} - Q: {q}[/b]".format(n=name, q=quantity), color = "#2f2f2f",
                            markup=True,
                            size_hint=(.12,.08),
                            font_size=16,
                            pos_hint={"center_x": .5, "center_y": .5},
                            background_normal=
                            "app/assets/invis-button.png",
                            background_down=
                            "app/assets/invis-button-down.png")]
        self.orders.append(order)
        self.orderlayout.add_widget(order[2])
    
    def __init__(self, **kwargs):
        super(Inventory, self).__init__(**kwargs)
        with self.canvas.before:
            self.bg = Rectangle(source = "app/assets/background.png",
                                size = self.size,
                                pos = self.pos)

        self.bind(size = self._update_bg, pos = self._update_bg)
        
        self.orders = []
        taskbar = FloatLayout()

        ribbon = Image(source="app/assets/ribbon-taskbar.png",
                            pos_hint={"center_x": .5, "center_y": .94})
        taskbar.add_widget(ribbon)

        self.currUser = Label(text="[b] Current User:[/b] {db}".format(db=VersionInfo.get_user()),
                             halign='center',
                             color = "#2f2f2f",
                             markup=True,
                             pos_hint={"center_x": .9, "center_y": .93}, font_size=16)
        taskbar.add_widget(self.currUser)
        
        ordersbut = Button(text="[b] ORDERS [/b]", color = "#2f2f2f",
                            markup=True,
                            size_hint=(.12,.08),
                            font_size=16,
                            pos_hint={"center_x": .17, "center_y": .93},
                            background_normal=
                            "app/assets/invis-button.png",
                            background_down=
                            "app/assets/invis-button-down.png")
        ordersbut.bind(on_release=orders_released)
        taskbar.add_widget(ordersbut)

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
        taskbar.add_widget(supportbut)

        logoutbut = Button(text="[b] LOGOUT [/b]", color = "#2f2f2f",
                            markup=True,
                            size_hint=(.12,.08),
                            font_size=16,
                            pos_hint={"center_x": .41, "center_y": .93},
                            background_normal=
                            "app/assets/invis-button.png",
                            background_down=
                            "app/assets/invis-button-down.png")
        logoutbut.bind(on_release=logout_released)
        taskbar.add_widget(logoutbut)
        
        self.gpanel = Image(source="app/assets/panel-3.png",
                           pos_hint={"center_x": .905, "center_y": .4})
        self.add_widget(self.gpanel)

        self.add_widget(taskbar)

        self.panel = Image(source="app/assets/panel-5.png",
                           pos_hint={"center_x": .4, "center_y": .465})
        self.add_widget(self.panel)
        
        self.inventoryscroll = Scroll()
        self.add_widget(self.inventoryscroll)

        self.orderlabel = Label(text="[b]Order[/b]",
                             color = "#2f2f2f",
                             markup=True,
                             pos_hint={"center_x": .9, "center_y": .85},
                             font_size=20)
        self.add_widget(self.orderlabel)

        self.orderlayout = GridLayout(cols=1,
                                      spacing=25,
                                      size_hint=(.16, None),
                                      pos_hint={"center_x": .9, "center_y": .72},
                                      size_hint_y=None)
        self.add_widget(self.orderlayout)

        self.purchasebut = Button(text="PURCHASE", color = "#21d74d",
                            outline_width=2, outline_color ="#ffffff",
                            size_hint=(.15,.08),
                            pos_hint={"center_x": .9, "center_y": .1},
                            font_size=18,
                            background_normal=
                            "app/assets/button.png",
                            background_down=
                            "app/assets/button-down.png")
        self.purchasebut.bind(on_release=purchase_released)
        self.add_widget(self.purchasebut)

        self.footer = Label(text="DEPI Microsoft Data Engineer Graduation Project - ONL1_AIS4_M9e - @github.com/37743",
                             color = "##6ee58b",
                             pos_hint={"center_x": .4, "center_y": .04},
                             font_size=11)
        self.add_widget(self.footer)