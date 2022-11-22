import time

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
from filesharer import FileSharer
import webbrowser

Builder.load_file('frontend.kv')

class CameraScreen(Screen):
    def start(self):
        self.ids.camera.play = True
        self.ids.start_stop.text = "Stop Camera"

    def stop(self):
        self.ids.camera.play = False
        self.ids.start_stop.text = "Start Camera"

    def capture(self):
        current_time = time.strftime('%Y%m%d-%H%M%S')
        filepath = 'files/' + current_time + ".png"
        self.ids.camera.export_to_png(filepath)
        self.manager.current = 'image_screen'
        self.manager.current_screen.ids.img.source = filepath

class ImageScreen(Screen):
    link_message = "Create a link first"

    def create_link(self):
        filepath = self.manager.current_screen.ids.img.source
        filesharer = FileSharer(filepath = filepath)
        self.url = filesharer.share()
        self.ids.img_link.text = self.url

    def copy_link(self):
        """Copy link to the clipboard available for pasting"""
        try:
            Clipboard.copy(self.url)
        except:
            print("Nothing to copy...")
            self.ids.img_link.text = self.link_message

    def open_link(self):
        """Open link with default browser"""
        try:
            webbrowser.open(self.url)
        except:
            self.ids.img_link.text = self.link_message

    def start_over(self):
        self.manager.current = 'camera_screen'


class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()

MainApp().run()

