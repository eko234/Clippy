import win32clipboard
import keyboard
from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'resizable',(0))
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from winsound import Beep
Window.size = (250, 500)
clips = globals()


class MainLayout(FloatLayout):

    def __init__(self, **kwargs):
        super(MainLayout, self).__init__(**kwargs)

        with self.canvas:
            Color(1, 1, 1, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=Window.size)


class ClipButton(Button):
    def __init__(self, **kwargs):
        super(ClipButton, self).__init__(**kwargs)

    def returnClipBoardValue(self, *args):
        try:
            win32clipboard.OpenClipboard()
            win32clipboard.EmptyClipboard()
            win32clipboard.SetClipboardData(1,self.text)
            win32clipboard.CloseClipboard()

        except:
            print "somer error at returnclipboardvalue"


def readClipboard():

    try:
        win32clipboard.OpenClipboard()
        result = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        return str(result)

    except TypeError:
        Beep(500, 100)
        Beep(400, 100)
        Beep(300, 100)
        Beep(200, 100)
        win32clipboard.CloseClipboard()
        return "only text for now :/"


class BoxBoard(GridLayout):

    def __init__(self, **kwargs):
            super(BoxBoard, self).__init__(**kwargs)
    childCounter = 0

    def newClipboardRecord(self, *args):

        #try:
            clips["entry" + str(self.childCounter)] = ClipButton(shorten=True,color=(.2, .2, .2, .4), font_size=18, text_size=(220, 20), background_normal="", background_color=(.2, .2, .2, .2), size_hint=(1, None), height=40, text=str(self.childCounter) + ". " + str(readClipboard()))
            clipBox.add_widget(clips["entry" + str(self.childCounter)])
            clips["entry" + str(self.childCounter)].bind(on_press=clips["entry" + str(self.childCounter)].returnClipBoardValue)
            self.childCounter = self.childCounter + 1
            Beep(700, 100)
            Beep(1050, 100)
        #except :
           # print "somer error at new clipboard record"

class ClipboardUpdater:#insted of a infinite loop with a schedueler, i think i might better usea keybindings
    def __init__(self):
        self.clipdata = ""

    def updateClipboardState(self,*args,**kwargs): #this boi will lock the fuking clipboard, but one might wanto to use it... eventually
        """"""""""
               try:
                   win32clipboard.OpenClipboard()
                   if self.clipdata == win32clipboard.GetClipboardData():
                       win32clipboard.CloseClipboard()
                       return
                   else:
                       self.clipdata = win32clipboard.GetClipboardData()
                       win32clipboard.CloseClipboard()
                       clipBox.newClipboardRecord(self.clipdata)
               except:
                   return

       """""""""""
    pass


scrollBox = ScrollView(size_hint=(1,.8475),pos_hint={'center_y':0.425, 'center_x': 0.5075}) #size_hint=(1,.8475)
frame = MainLayout(orientation="vertical")
but1 = Button(font_size=25,color=(.2,.2,.2,.8),background_color=(.2,.2,.2,.1),text="Clippy!",size_hint=(1,0.15),pos_hint={'center_y':0.9245, 'center_x': 0.5})
clipBox = BoxBoard(spacing=1,cols =1,orientation="vertical",size_hint=(.985,None),)  #,size_hint=(1,1),pos_hint={'center_y':0.425, 'center_x': 0.5}
scrollBox.add_widget(clipBox)
frame.add_widget(but1)
frame.add_widget(scrollBox)
clipBox.bind(minimum_height=clipBox.setter('height'))

keyboard.add_hotkey('ctrl+shift+a',clipBox.newClipboardRecord)


class MainApp(App):

    def build(self):

        return frame

MainApp().run()

