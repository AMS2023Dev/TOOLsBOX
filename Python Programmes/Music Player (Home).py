import tkinter as tk
from tkinter import filedialog
import pygame
from PIL import Image, ImageTk
import os

class MusicPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player (Home (beta))")
        self.root.configure(bg="lightgray")
        
        self.song_list = []
        self.current_song_index = 0
        self.paused = False
        
        self.create_widgets()
        
        pygame.init()
        pygame.mixer.init()
    
    def create_widgets(self):
        self.create_song_label()
        self.create_song_listbox()
        self.create_control_buttons()
        self.create_song_image_label()
    
    def create_song_label(self):
        self.song_label = tk.Label(self.root, text="Songs:", bg="lightgray", font=("Helvetica", 14, "bold"))
        self.song_label.pack(pady=10)
    
    def create_song_listbox(self):
        self.song_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, width=50, bg="white", font=("Helvetica", 12))
        self.song_listbox.pack()
        self.song_listbox.bind("<Double-Button-1>", self.play_selected_song)
    
    def create_control_buttons(self):
        button_configs = [
            ("Browse", self.browse_songs),
            ("Play", self.play_song),
            ("Pause", self.pause_song),
            ("Stop", self.stop_song)
        ]
        
        for text, command in button_configs:
            button = tk.Button(self.root, text=text, command=command, font=("Helvetica", 12, "bold"))
            button.pack(pady=5)
    
    def create_song_image_label(self):
        self.song_image_label = tk.Label(self.root, bg="lightgray")
        self.song_image_label.pack()
    
    def browse_songs(self):
        song_paths = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3")])
        if song_paths:
            self.song_list.extend(song_paths)
            self.update_song_listbox()
    
    def update_song_listbox(self):
        self.song_listbox.delete(0, tk.END)
        for song_path in self.song_list:
            song_name = os.path.basename(song_path)
            self.song_listbox.insert(tk.END, song_name)
        
        self.play_button.config(state="normal")
        self.update_song_info()
    
    def play_song(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        
        song_path = self.song_list[self.current_song_index]
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        
        self.update_song_info()
        self.update_song_image(song_path)
    
    def pause_song(self):
        if not self.paused:
            pygame.mixer.music.pause()
            self.paused = True
        else:
            pygame.mixer.music.unpause()
            self.paused = False
    
    def stop_song(self):
        pygame.mixer.music.stop()
    
    def play_selected_song(self, event):
        selected_song_index = self.song_listbox.curselection()
        if selected_song_index:
            self.current_song_index = selected_song_index[0]
            self.play_song()
    
    def update_song_info(self):
        song_path = self.song_list[self.current_song_index]
        song_name = os.path.basename(song_path)
        self.song_label.config(text="Now Playing: " + song_name)
    
    def update_song_image(self, song_path):
        image_path = song_path.replace(".mp3", ".jpg")
        try:
            image = Image.open(image_path)
            image = image.resize((150, 150), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            self.song_image_label.config(image=photo)
            self.song_image_label.image = photo
        except:
            self.song_image_label.config(image="")
            self.song_image_label.image = None
    
if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayerApp(root)
    root.mainloop()
