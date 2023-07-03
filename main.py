from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFillRoundFlatButton
from kivy.clock import Clock
from plyer import filechooser
from pyzbar.pyzbar import decode
from cv2 import imread
from cryptography.fernet import Fernet
import cryptography
import arabic_reshaper
from bidi.algorithm import get_display
from kivymd.app import MDApp

kv="""
<CameraApp>:   
    MDScreen:    
        MDNavigationLayout:
            ScreenManager:
                id:scren_manager
                name:scren_manager
                MDScreen:
                    name:'cm_scr'    
                    MDBoxLayout:
                        orientation:'vertical'
                        MDToolbar:
                            id: toolbar
                            pos_hint: {"top": 1}
                            elevation: 10
                            title:'First App'
                            left_action_items:[['atom',lambda x:nav_drawer.set_state('toggle')]]
                        MDBoxLayout:
                            orientation:'vertical'
                            #:import ZBarCam kivy_garden.zbarcam.ZBarCam
                            #:import ZBarSymbol pyzbar.pyzbar.ZBarSymbol
                            ZBarCam:
                                id: zbarcam
                                # optional, by default checks all types
                                code_types: ZBarSymbol.QRCODE, ZBarSymbol.EAN13
                                allow_stretch: True
                                keep_ratio: True
                            MDFloatingActionButton:
                                id: select_image
                                icon:  "image-multiple"
                                #md_bg_color: app.theme_cls.primary_color
                                on_press:root.select()
                                pos_hint: {'center_x':0.5,'center_y':0.5}
                MDScreen:
                    name:'bgs_scr'
                    MDBoxLayout:
                        orientation:'vertical'
                        MDToolbar:
                            id: toolbar
                            pos_hint: {"top": 1}
                            elevation: 10
                            title:'First App'
                            left_action_items:[['atom',lambda x:nav_drawer.set_state('toggle')]]
                        MDLabel:
                            text:'Bugs'
                            halign:'center'
                MDScreen:
                    name:'stg_scr'
                    MDBoxLayout:
                        orientation:'vertical'
                        MDToolbar:
                            id: toolbar
                            pos_hint: {"top": 1}
                            elevation: 10
                            title:'First App'
                            left_action_items:[['atom',lambda x:nav_drawer.set_state('toggle')]]
                        MDLabel:
                            text:'Setting'
                            halign:'center'

            MDNavigationDrawer:
                id:nav_drawer
                MDBoxLayout:
                    orientation:'vertical'

                    Image:
                        source:'logo.jpg'

                    MDLabel:
                        text: 'Bahrib665@Gmail.com'
                        font_style: 'Subtitle1'
                        halign:'center'
                        size_hint_y:0.2
                    ScrollView:
                        MDList:
                            size_hint_y:None
                            OneLineIconListItem:
                                text:'Camera'
                                on_press:
                                    nav_drawer.set_state("close") 
                                    scren_manager.current="cm_scr"
                                IconLeftWidget:
                                    icon:'camera'

                            OneLineIconListItem:
                                text:'Report Bugs'
                                on_press:
                                    nav_drawer.set_state("close")
                                    scren_manager.current="bgs_scr"
                                IconLeftWidget:
                                    icon:'send'

                            OneLineIconListItem:
                                on_press:
                                    nav_drawer.set_state("close")
                                    scren_manager.current='stg_scr'
                                text:'Setting'
                                IconLeftWidget:
                                    icon:'cog'
"""

class CameraApp(MDScreen):
    Builder.load_string(kv)
    def __init__(self):
        super(CameraApp, self).__init__()
        self.dialogue = None
        self.key_1 = "icL5BirdckXVHl_lHUS5ezrSDYChH1myFWzVfYUbrj4="#for Adistation
        self.key_2 = "M2HJRHdC4PYzVNbGfW8QuNmRK47zJnLPhMtQfBwZKb0="#for Diplome
        Clock.schedule_interval(self.info, 1.0 / 30.0)

    def info(self, instance):
        if not self.dialogue:
            for symbol in self.ids.zbarcam.symbols:
                close_button = MDFillRoundFlatButton(text="Close", on_release=self.close)
                data = str(symbol.data.decode())
                print(data[0])
                fernet = Fernet(self.key_1)
                try:
                    data = data.encode()
                    decMessage = fernet.decrypt(data).decode()
                    reshaped_text = arabic_reshaper.reshape(decMessage)
                    bidi_text = get_display(reshaped_text)
                    self.dialogue = MDDialog(title="QR DATA",
                                             text="[font=arial.ttf]" + str(bidi_text) + "[/font]",
                                             size_hint=(0.6, 1),
                                             buttons=[close_button],
                                             auto_dismiss=False)
                    self.dialogue.open()
                except cryptography.fernet.InvalidToken as e:
                    self.dialogue = MDDialog(title="QR DATA",
                                             text="[font=arial.ttf]" + "please contact us" + "[/font]",
                                             size_hint=(0.6, 1),
                                             buttons=[close_button],
                                             auto_dismiss=False)
                    self.dialogue.open()

    def select(self):
        filechooser.open_file(on_selection=self.image)

    def image(self, selection):
        if selection:
            image = imread(str(selection[0]))
            imageqr = decode(image)
            close_button = MDFillRoundFlatButton(text="Close", on_release=self.close)
            if imageqr:
                data = str(imageqr[0].data.decode())
                fernet = Fernet(self.key_1)
                try:
                    data = data.encode()
                    decMessage = fernet.decrypt(data).decode()
                    reshaped_text = arabic_reshaper.reshape(decMessage)
                    bidi_text = get_display(reshaped_text)
                    self.dialogue = MDDialog(title="QR DATA",
                                             text="[font=arial.ttf]" + str(bidi_text) + "[/font]",
                                             size_hint=(0.6, 1),
                                             buttons=[close_button],
                                             auto_dismiss=False)
                    self.dialogue.open()
                except cryptography.fernet.InvalidToken as e:
                    self.dialogue = MDDialog(title="QR DATA",
                                             text="[font=arial.ttf]" + "please contact us" + "[/font]",
                                             size_hint=(0.6, 1),
                                             buttons=[close_button],
                                             auto_dismiss=False)
                    self.dialogue.open()
            else:
                self.dialogue = MDDialog(title="ERROR",
                                         text="please insert an QR CODE", size_hint=(0.6, 1),
                                         buttons=[close_button],
                                         auto_dismiss=False)
                self.dialogue.open()

    def decrypt(self, string, shift):
        result = ''
        for c in string:
            if ord(c) - shift <= 0:
                result += chr(255 - shift)
            elif ord(c) - shift >= 0 and ord(c) <= 255:
                result += chr(ord(c) - shift)
            else:
                result += c
        return result

    def close(self, instance):
        self.dialogue.dismiss()
        self.dialogue = None


class TestNavigationDrawer(MDApp):
    def build(self):
        return CameraApp()


if __name__ == '__main__':
    try:
        TestNavigationDrawer().run()
    except SystemExit:
        print('Windows Close')
