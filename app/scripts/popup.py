# Popups
# ---
# --------
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup 
from functools import partial

import pymssql
connection = None

class Support():
    def __init__(self, **kwargs):
        boxlayout = BoxLayout(orientation="vertical")
        gridlayout = GridLayout(cols=1)
        message = Label(text="Kindly send us an email specifying your problem so we can get you the right help and support.",
                    halign="center",
                    valign="center",
                    text_size=(360,None),
                    color="black")
        # TODO: Change this email to company email. vvv
        suppemail = Label(text="[u]{e}[/u]".format(e="yousef.gomaa@ejust.edu.eg"),
                    markup=True,
                    halign="center",
                    color="#21d74d")
        dismiss = Button(text="OK", color = "#21d74d",
                        outline_width=2, outline_color ="#ffffff",
                        size_hint=(.5,.5),
                        font_size=18,
                        pos_hint={"center_x": .5, "center_y": .325},
                        background_normal=
                        "app/assets/button.png",
                        background_down=
                        "app/assets/button-down.png")
        gridlayout.add_widget(message)
        gridlayout.add_widget(suppemail)
        gridlayout.add_widget(dismiss)
        boxlayout.add_widget(gridlayout)
        popup = Popup(title="Support",
                    title_color="black",
                    background="app/assets/panel.png",
                    content=boxlayout,
                    size_hint=(None, None), size=(400, 360))
        dismiss.bind(on_press=popup.dismiss)
        popup.open()

class SignedUp():
    """ Successful sign-up popup logic"""
    def __init__(self, username):
        boxlayout = BoxLayout(orientation="vertical")
        gridlayout = GridLayout(cols=1)
        cicon = Image(source="app/assets/check-icon.png",
                    size_hint = (1,1))
        message = Label(text="Congratulations!\n"+\
                        "You have signed up as a retailer successfully!",
                    halign="center",
                    valign="center",
                    text_size=(360,None),
                    color="black")
        message2 = Label(text="Use the username given below along with your password to login.",
                    halign="center",
                    valign="center",
                    text_size=(360,None),
                    color="black")
        user = Label(text="[b]{u}[/b]".format(u=str(username)),
                    markup=True,
                    font_size=24,
                    halign="center",
                    color="#21d74d")
        dismiss = Button(text="OK", color = "#21d74d",
                        outline_width=2, outline_color ="#ffffff",
                        size_hint=(.7,.7),
                        font_size=18,
                        pos_hint={"center_x": .5, "center_y": .325},
                        background_normal=
                        "app/assets/button.png",
                        background_down=
                        "app/assets/button-down.png")
        gridlayout.add_widget(message)
        gridlayout.add_widget(cicon)
        gridlayout.add_widget(message2)
        gridlayout.add_widget(user)
        gridlayout.add_widget(dismiss)
        boxlayout.add_widget(gridlayout)
        popup = Popup(title="Success",
                    title_color="black",
                    background="app/assets/panel.png",
                    content=boxlayout,
                    size_hint=(None, None), size=(400, 360))
        dismiss.bind(on_press=popup.dismiss)
        popup.open()

class Purchased():
    """ Successful purchase popup logic"""
    def __init__(self):
        boxlayout = BoxLayout(orientation="vertical")
        gridlayout = GridLayout(cols=1)
        cicon = Image(source="app/assets/check-icon.png",
                    size_hint = (1,1))
        message = Label(text="Transaction Made Successfully!",
                    halign="center",
                    valign="center",
                    text_size=(360,None),
                    color="black")
        message2 = Label(text="You will soon be contacted by a sales representative of our company!",
                    halign="center",
                    valign="center",
                    text_size=(360,None),
                    color="black")
        dismiss = Button(text="OK", color = "#21d74d",
                        outline_width=2, outline_color ="#ffffff",
                        size_hint=(.7,.7),
                        font_size=18,
                        pos_hint={"center_x": .5, "center_y": .325},
                        background_normal=
                        "app/assets/button.png",
                        background_down=
                        "app/assets/button-down.png")
        gridlayout.add_widget(message)
        gridlayout.add_widget(cicon)
        gridlayout.add_widget(message2)
        gridlayout.add_widget(dismiss)
        boxlayout.add_widget(gridlayout)
        popup = Popup(title="Success",
                    title_color="black",
                    background="app/assets/panel.png",
                    content=boxlayout,
                    size_hint=(None, None), size=(400, 360))
        dismiss.bind(on_press=popup.dismiss)
        popup.open()
        
def delete_order(instance, obj, item, user, passwd):
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
        cursor.execute("""
            UPDATE ems.products 
            SET stock_quantity = stock_quantity + @q 
            WHERE sku = @p
        """,
        q=item[3],
        p=item[2])

        cursor.execute("""
            DELETE FROM ems.orders 
            WHERE order_id = @o
        """,
        o=item[0])
        
        connection.commit()
        connection.close()
    except pymssql.Error as error:
        print(error)
    finally:
        obj.remove_widget(instance)

class Orders():
    """ A layout to show the retailer's orders """

    def __init__(self, retailer_orders, username, password):
        self.boxlayout = BoxLayout(orientation="vertical", spacing=-10)
        self.gridlayout = GridLayout(cols=1, spacing=5)
        orderlabel = Label(text="[b]WARNING:\nClicking an order deletes it![/b]",
                    markup=True,
                    size_hint=(.3,.3),
                    font_size=24,
                    halign="center",
                    color="#21d74d")
        self.orderbox = GridLayout(cols=1)
        ordercols = Label(text="[b]ORDER_ID\
                ORDER_DATE\
                SKU\
            QUANTITY\
            SHIPMENT_ID\
        PAYMENT_ID\
        ORDER_STATUS[/b]",
                          color = "#2f2f2f",
                          markup=True,
                          halign="center",
                          font_size=16,
                          size_hint=(.1,.1)
                          )
        self.orderlist = []
        for item in retailer_orders:
            order = Button(text="{id}\
                            {date}\
                        {sku}\
                        {q}\
                                {ship_id}\
                                    {payment_id}\
                            {status}"\
                           .format(id=item[0],
                                   date=str(item[1])[:10],
                                   sku=item[2],
                                   q=item[3],
                                   ship_id=item[4],
                                   payment_id=item[7],
                                   status=item[8]
                                   ),
                            color = "#2f2f2f",
                            markup=True,
                            halign="center",
                            size_hint=(1,.1),
                            font_size=16,
                            pos_hint={"center_x": .5, "center_y": .5},
                            background_normal=
                            "app/assets/invis-button.png",
                            background_down=
                            "app/assets/invis-button-down.png")
            self.orderlist.append(item)
            order.bind(on_release=partial(delete_order, obj=self.orderbox, item=item, user=username, passwd=password))
            self.orderbox.add_widget(order)

        dismiss = Button(text="OK", color = "#21d74d",
                        outline_width=2, outline_color ="#ffffff",
                        size_hint=(.7,.2),
                        font_size=18,
                        pos_hint={"center_x": .5, "center_y": .325},
                        background_normal=
                        "app/assets/button.png",
                        background_down=
                        "app/assets/button-down.png")
        self.gridlayout.add_widget(orderlabel)
        self.gridlayout.add_widget(ordercols)
        self.gridlayout.add_widget(self.orderbox)
        self.gridlayout.add_widget(dismiss)
        self.boxlayout.add_widget(self.gridlayout)
        popup = Popup(title="Retailer's Orders",
                    title_color="black",
                    background="app/assets/panel.png",
                    content=self.boxlayout,
                    size_hint=(None, None), size=(992, 512))
        dismiss.bind(on_press=popup.dismiss)
        popup.open()