from kivy.app import App
from kivy.config import Config
Config.set('graphics', 'resizable',(0))
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
import win32clipboard

from kivy.clock import Clock
Window.size = (250, 500)
clips = globals()

class main_layout(FloatLayout):

    def __init__(self,**kwargs):
        super(main_layout, self).__init__(**kwargs)

        with self.canvas:
            Color(1, 1, 1, 1)  # green; colors range from 0-1 instead of 0-255
            self.rect = Rectangle(size=Window.size)


class ClipButton(Button):
    def __init__(self,**kwargs):
        super(ClipButton, self).__init__(**kwargs)

    def returnClipBoardValue(self,*args):
        print "nigger"# this is only for testing still, it is suposed to retrieve the texto to the clipboard




class BoxBoard(GridLayout):

    def __init__(self, **kwargs):
        super(BoxBoard, self).__init__(**kwargs)
    childcounter = 0

    def newClipboardRecord(self, testext, *args):
        clips["entry"+str(self.childcounter)] = ClipButton(color=(.2,.2,.2,.4),font_size=18,text_size=(220,20),background_normal="", background_color=(.2,.2,.2,.2),size_hint=(1,None),height=40,text=testext)
        clipBox.add_widget(clips["entry"+str(self.childcounter)])
        clips["entry" + str(self.childcounter)].bind(on_press=clips["entry" + str(self.childcounter)].returnClipBoardValue)
        self.childcounter = self.childcounter + 1



class ClipboardUpdater():#insted of a infinite loop with a schedueler, i think i might better usea keybindings
    def __init__(self):
        self.clipdata = ""

    def updateClipboardState(self,*args,**kwargs):
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



scrollBox = ScrollView(size_hint=(1,.8475),pos_hint={'center_y':0.425, 'center_x': 0.5075}) #size_hint=(1,.8475)
frame = main_layout(orientation="vertical")
but1 = Button(font_size=30,color=(.2,.2,.2,.8),background_color=(.2,.2,.2,.1),text="Clippy!",size_hint=(1,0.15),pos_hint={'center_y':0.9245, 'center_x': 0.5})
clipBox = BoxBoard(spacing=1,cols =1,orientation="vertical",size_hint=(.985,None),)#,size_hint=(1,1),pos_hint={'center_y':0.425, 'center_x': 0.5}

scrollBox.add_widget(clipBox)
frame.add_widget(but1)
frame.add_widget(scrollBox)

clipBox.bind(minimum_height=clipBox.setter('height'))
but1.bind(on_press=clipBox.newClipboardRecord)

clipboardManager = ClipboardUpdater()

class MainApp(App):
    def build(self):

        Clock.schedule_interval(clipboardManager.updateClipboardState, 10 / 60.0)
        return frame

MainApp().run()

