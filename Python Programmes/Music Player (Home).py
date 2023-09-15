import tkinter as tk
from tkinter import filedialog, simpledialog, colorchooser
import pygame
import os
import random
from mutagen.mp3 import MP3
from PIL import Image, ImageTk

class MusicPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player (Home - free)")
        self.root.geometry("800x600")
        self.root.configure(bg="lightgray")

        self.song_list = []
        self.current_song_index = 0
        self.paused = False
        self.shuffle = False
        self.repeat = False
        self.playlists = {}
        self.current_playlist = None
        self.bg_color = "lightgray"
        self.text_color = "blue"
        self.volume = 0.5  # مقدار پیش‌فرض میزان صدا

        self.create_widgets()

        pygame.init()
        pygame.mixer.init()

    def create_widgets(self):
        self.create_song_label()
        self.create_song_listbox()
        self.create_control_buttons()
        self.create_playlist_buttons()
        self.create_song_info_labels()
        self.create_volume_controls()
        self.create_color_change_buttons()
        self.create_image_change_button()

    def create_song_label(self):
        self.song_label = tk.Label(self.root, text="Songs:", bg=self.bg_color, fg=self.text_color, font=("Helvetica", 14, "bold"))
        self.song_label.pack(pady=10, anchor="w")

    def create_song_listbox(self):
        self.song_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, width=50, bg="white")
        self.song_listbox.pack()
        self.song_listbox.bind("<Double-Button-1>", self.play_selected_song)

    def create_control_buttons(self):
        button_configs = [
            ("Browse", self.browse_songs),
            ("Play", self.play_song),
            ("Pause", self.pause_song),
            ("Stop", self.stop_song),
            ("Next", self.next_song),
            ("Previous", self.prev_song),
            ("Shuffle: OFF", self.toggle_shuffle),
            ("Repeat: OFF", self.toggle_repeat),
            ("Remove Song", self.remove_song)
        ]

        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack()

        for text, command in button_configs:
            button = tk.Button(button_frame, text=text, command=command, bg="lightblue", fg="black", font=("Helvetica", 12, "bold"))
            button.pack(side="left", padx=10)

        self.create_seek_bar()

    def create_seek_bar(self):
        self.seek_scale = tk.Scale(self.root, from_=0, to=0, orient=tk.HORIZONTAL, showvalue=0, length=600, bg="lightgray")
        self.seek_scale.pack()

    def create_playlist_buttons(self):
        self.add_playlist_button = tk.Button(self.root, text="Add Playlist", command=self.add_playlist, bg="lightblue", fg="black", font=("Helvetica", 12, "bold"))
        self.add_playlist_button.pack()

        self.remove_playlist_button = tk.Button(self.root, text="Remove Playlist", command=self.remove_playlist, bg="lightblue", fg="black", font=("Helvetica", 12, "bold"))
        self.remove_playlist_button.pack()

        self.playlist_menu = tk.Menu(self.root)
        self.root.config(menu=self.playlist_menu)

    def create_song_info_labels(self):
        self.song_info_label = tk.Label(self.root, text="", font=("Helvetica", 12), bg=self.bg_color, fg=self.text_color)
        self.song_info_label.pack()

        self.song_duration_label = tk.Label(self.root, text="", font=("Helvetica", 10), bg=self.bg_color, fg=self.text_color)
        self.song_duration_label.pack()

    def create_volume_controls(self):
        self.volume_label = tk.Label(self.root, text="Volume:", bg=self.bg_color, fg=self.text_color)
        self.volume_label.pack()

        self.volume_scale = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume, bg=self.bg_color)
        self.volume_scale.set(int(self.volume * 100))
        self.volume_scale.pack()

    def create_color_change_buttons(self):
        self.change_bg_color_button = tk.Button(self.root, text="Change Background Color", command=self.change_bg_color, bg="lightblue", fg="black", font=("Helvetica", 12, "bold"))
        self.change_bg_color_button.pack()

        self.change_text_color_button = tk.Button(self.root, text="Change Text Color", command=self.change_text_color, bg="lightblue", fg="black", font=("Helvetica", 12, "bold"))
        self.change_text_color_button.pack()

    def create_image_change_button(self):
        self.change_image_button = tk.Button(self.root, text="Change Image", command=self.change_image, bg="lightblue", fg="black", font=("Helvetica", 12, "bold"))
        self.change_image_button.pack()

    def browse_songs(self):
        song_paths = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3 *.ogg")])
        if song_paths:
            self.song_list.extend(song_paths)
            self.update_song_listbox()

    def update_song_listbox(self):
        self.song_listbox.delete(0, tk.END)
        for song_path in self.song_list:
            song_name = os.path.basename(song_path)
            self.song_listbox.insert(tk.END, song_name)

        self.play_button.config(state="normal")
        self.next_button.config(state="normal")
        self.shuffle_button.config(state="normal")
        self.repeat_button.config(state="normal")
        self.remove_song_button.config(state="normal")

    def play_song(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

        song_path = self.song_list[self.current_song_index]
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()

        self.play_button.config(state="disabled")
        self.pause_button.config(state="normal")
        self.stop_button.config(state="normal")
        self.prev_button.config(state="normal")
        self.next_button.config(state="normal")
        self.update_song_info()
        self.update_song_image(song_path)

        # تنظیم مقدار حداکثر برای seek_scale به طول آهنگ
        audio = MP3(song_path)
        self.seek_scale.config(to=audio.info.length)
        self.seek_scale.set(0)
        self.update_seek_bar()

    def update_seek_bar(self):
        current_time = pygame.mixer.music.get_pos() / 1000
        self.seek_scale.set(current_time)
        if pygame.mixer.music.get_busy():
            self.seek_scale.after(1000, self.update_seek_bar)

    def pause_song(self):
        if not self.paused:
            pygame.mixer.music.pause()
            self.paused = True
            self.pause_button.config(text="Resume", bg="green")
        else:
            pygame.mixer.music.unpause()
            self.paused = False
            self.pause_button.config(text="Pause", bg="orange")

    def stop_song(self):
        pygame.mixer.music.stop()
        self.play_button.config(state="normal")
        self.pause_button.config(state="disabled")
        self.stop_button.config(state="disabled")
        self.seek_scale.set(0)

    def next_song(self):
        if self.shuffle:
            self.current_song_index = random.randint(0, len(self.song_list) - 1)
        else:
            if self.repeat:
                pass
            elif self.current_song_index < len(self.song_list) - 1:
                self.current_song_index += 1
        self.play_song()

    def prev_song(self):
        if self.shuffle:
            self.current_song_index = random.randint(0, len(self.song_list) - 1)
        else:
            if self.repeat:
                pass
            elif self.current_song_index > 0:
                self.current_song_index -= 1
        self.play_song()

    def toggle_shuffle(self):
        self.shuffle = not self.shuffle
        if self.shuffle:
            self.shuffle_button.config(text="Shuffle: ON", bg="purple")
        else:
            self.shuffle_button.config(text="Shuffle: OFF", bg="purple")

    def toggle_repeat(self):
        self.repeat = not self.repeat
        if self.repeat:
            self.repeat_button.config(text="Repeat: ON", bg="purple")
        else:
            self.repeat_button.config(text="Repeat: OFF", bg="purple")

    def play_selected_song(self, event):
        selected_song_index = self.song_listbox.curselection()
        if selected_song_index:
            self.current_song_index = selected_song_index[0]
            self.play_song()

    def update_song_info(self):
        song_path = self.song_list[self.current_song_index]
        song_name = os.path.basename(song_path)

        audio = MP3(song_path)
        song_duration = self.format_duration(audio.info.length)

        self.song_info_label.config(text=song_name, fg=self.text_color)
        self.song_duration_label.config(text=song_duration)

        self.song_info_label.after(1000, self.clear_song_info)

    def clear_song_info(self):
        self.song_info_label.config(text="")
        self.song_duration_label.config(text="")
        self.song_info_label.after(1000, self.update_song_info)

    def format_duration(self, duration):
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        return f"{minutes:02d}:{seconds:02d}"

    def add_playlist(self):
        playlist_name = simpledialog.askstring("Add Playlist", "Enter playlist name:")
        if playlist_name and playlist_name not in self.playlists:
            self.playlists[playlist_name] = []
            self.update_playlist_menu()

    def remove_playlist(self):
        if self.playlists:
            playlist_name = simpledialog.askstring("Remove Playlist", "Enter playlist name:")
            if playlist_name in self.playlists:
                del self.playlists[playlist_name]
                self.update_playlist_menu()

    def update_playlist_menu(self):
        self.playlist_menu.delete(0, tk.END)
        for playlist_name in self.playlists:
            self.playlist_menu.add_command(label=playlist_name, command=lambda name=playlist_name: self.load_playlist(name))

    def load_playlist(self, playlist_name):
        self.current_playlist = playlist_name
        self.song_list = self.playlists[playlist_name]
        self.update_song_listbox()

    def update_song_image(self, song_path):
        audio = MP3(song_path)
        try:
            image_path = song_path.replace(".mp3", ".jpg")
            image = Image.open(image_path)
            image = image.resize((150, 150), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(image)
            self.song_image_label.config(image=photo)
            self.song_image_label.image = photo
        except:
            self.song_image_label.config(image="")
            self.song_image_label.image = None

    def change_bg_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.bg_color = color
            self.root.configure(bg=color)
            for widget in self.root.winfo_children():
                widget.configure(bg=color)

    def change_text_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.text_color = color
            for label in [self.song_label, self.song_info_label, self.song_duration_label, self.volume_label]:
                label.config(fg=color)
            for button in [self.play_button, self.pause_button, self.stop_button, self.next_button, self.prev_button, self.shuffle_button, self.repeat_button, self.add_playlist_button, self.remove_playlist_button, self.change_bg_color_button, self.change_text_color_button, self.change_image_button]:
                button.config(fg=color)

    def set_volume(self, value):
        self.volume = float(value) / 100
        pygame.mixer.music.set_volume(self.volume)

    def change_image(self):
        selected_song_path = self.song_list[self.current_song_index]
        image_extensions = [".jpg", ".png", ".jpeg"]
        image_path = None

        for extension in image_extensions:
            if extension in selected_song_path:
                image_path = selected_song_path.replace(extension, ".jpg")
                break

        if image_path:
            self.update_song_image(image_path)

    def remove_song(self):
        selected_song_index = self.song_listbox.curselection()
        if selected_song_index:
            index_to_remove = selected_song_index[0]
            del self.song_list[index_to_remove]
            self.update_song_listbox()

if __name__ == "__main__":
    root = tk.Tk()
    app = MusicPlayerApp(root)
    root.mainloop()
