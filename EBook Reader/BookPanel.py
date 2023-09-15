import threading
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from PIL import ImageTk, Image
from BookPDF import BookPDF
from BookEPUB import BookEPUB
from Settings import *
from Audio import *


class BookPanel(ttk.Frame):
    def __init__(self, parent, settings):
        super().__init__(parent)
        self.place(relx=0.3, rely=0.95, relwidth=0.7, relheight=0.05)

        self.settings = settings
        self.audio = Audio(self, self.settings)
        self.audio_enabled = False
        self.book_pdf = None
        self.book_epub = None

        self.create_widgets()

    def create_widgets(self):
        self.button_left = ttk.Button(self, text='Prev. page', command=self.previous_page)
        self.button_settings = ttk.Button(self, text='Settings', command=self.open_settings)
        self.button_audiobook = ttk.Button(self, text='Audio', command=self.toggle_audio)
        self.button_right = ttk.Button(self, text='Next page', command=self.next_page)

        self.set_icons(self.button_left, 'icons/arrow_left.png')
        self.set_icons(self.button_right, 'icons/arrow_right.png')
        self.set_icons(self.button_settings, 'icons/settings.png')
        self.set_icons(self.button_audiobook, 'icons/speaker_disable.png')

        self.columnconfigure((0, 1, 2, 3), weight=1, uniform='b')

        self.button_left.grid(row=1, column=0, sticky='nswe')
        self.button_settings.grid(row=1, column=1, sticky='nswe')
        self.button_audiobook.grid(row=1, column=2, sticky='nswe')
        self.button_right.grid(row=1, column=3, sticky='nswe')

    def set_icons(self, button, icon_path):
        photo = ImageTk.PhotoImage(Image.open(icon_path))
        button.configure(image=photo)
        button.image = photo

    def toggle_audio(self):
        self.audio_enabled = not self.audio_enabled
        if self.book_pdf:
            text = self.book_pdf.return_text()
        elif self.book_epub:
            text = self.book_epub.return_text()
        
        text = text.replace('\n',' ')
        text = text.split('.')
        
        if self.audio_enabled:
            print("Starting audio")
            self.audio_enabled = True
            # Tworzymy wątek audio_thread, ale tylko jeśli go jeszcze nie mamy
            if not hasattr(self, 'audio_thread') or not self.audio_thread.is_alive():
                self.audio_thread = threading.Thread(target=self._play_audio, args=(text,))
                self.audio_thread.start()
        else:
            print("Stopping audio")
            # Wywołujemy funkcję stop_audio, aby zatrzymać odtwarzanie audio
            if hasattr(self, 'audio_thread') and self.audio_thread.is_alive():
                self.audio.stop_audio()
        
        self.set_icons(self.button_audiobook, 'icons/speaker_enable.png' if self.audio_enabled else 'icons/speaker_disable.png')

    def _play_audio(self, text):
        for sentence in text:
            if self.audio_enabled:
                print("Reading:", sentence.strip())
                self.audio.read_page(sentence.strip())
            else:
                break
    # def toggle_audio(self):
    #     self.audio_enabled = not self.audio_enabled
    #     if self.audio_enabled:
    #         self.audio_thread = threading.Thread(target=self.audio.read_page)
    #         self.audio_thread.start()
    #     self.set_icons(self.button_audiobook, 'icons/speaker_enable.png' if self.audio_enabled else 'icons/speaker_disable.png')

    def set_book_pdf(self, book_pdf):
        self.book_epub = None
        self.book_pdf = book_pdf

    def set_book_epub(self, book_epub):
        self.book_pdf = None
        self.book_epub = book_epub

    def previous_page(self):
        if self.book_pdf:
            self.book_pdf.previous_page()
        elif self.book_epub:
            self.book_epub.previous_page()

    def next_page(self):
        if self.book_pdf:
            self.book_pdf.next_page()
        elif self.book_epub:
            self.book_epub.next_page()
    
    def open_settings(self):
        self.settings.settings_window()
