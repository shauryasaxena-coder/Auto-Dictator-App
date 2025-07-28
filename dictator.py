import customtkinter as ctk
from gtts import gTTS
import pygame
import random
import tempfile

def load_words(file_path):
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

class SpellingApp:
    def __init__(self, master):
        self.master = master
        self.words = load_words("words.txt")
        self.used_words = []
        self.current_word = None
        self.current_audio_file = None

        pygame.mixer.init()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Heading
        self.label = ctk.CTkLabel(
            master, 
            text="Click a button to start", 
            font=("Arial", 32, "bold")
        )
        self.label.pack(pady=20)

        # Word label (hidden until Show is pressed)
        self.word_label = ctk.CTkLabel(
            master,
            text="",
            font=("Arial", 36, "bold"),
            text_color="#1a73e8"   # default color for revealed words
        )
        self.word_label.pack(pady=20)

        # ▶ Hear new word
        self.button_play = ctk.CTkButton(
            master,
            text="▶ Hear",
            font=("Arial", 26, "bold"),
            corner_radius=30,
            height=60,
            width=300,
            fg_color="#1a73e8",
            hover_color="#1557b0",
            command=self.play_new_word
        )
        self.button_play.pack(pady=10)

        # 🔁 Replay same word
        self.button_replay = ctk.CTkButton(
            master,
            text="🔁 Replay",
            font=("Arial", 26, "bold"),
            corner_radius=30,
            height=60,
            width=300,
            fg_color="#fbbc05",
            hover_color="#c69303",
            command=self.replay_word
        )
        self.button_replay.pack(pady=10)

        # 👁 Show the word
        self.button_show = ctk.CTkButton(
            master,
            text="👁 Show",
            font=("Arial", 26, "bold"),
            corner_radius=30,
            height=60,
            width=300,
            fg_color="#3cba54",
            hover_color="#2d8f41",
            command=self.show_word
        )
        self.button_show.pack(pady=10)

    def get_next_word(self):
        if not self.words:
            self.label.configure(text="All text used. Restarting...")
            self.words = self.used_words
            self.used_words = []
            return None

        self.current_word = random.choice(self.words)
        self.words.remove(self.current_word)
        self.used_words.append(self.current_word)
        return self.current_word

    def play_audio(self, word):
        try:
            tts = gTTS(text=word, lang='en')
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.save(fp.name)
                self.current_audio_file = fp.name
                pygame.mixer.music.load(self.current_audio_file)
                pygame.mixer.music.play()
        except Exception as e:
            self.label.configure(text=f"Error: {e}")

    def play_new_word(self):
        word = self.get_next_word()
        if word is None:
            return
        self.word_label.configure(text="")  # hide the word
        self.label.configure(text="Listen…")
        self.play_audio(word)

    def replay_word(self):
        if self.current_audio_file:
            pygame.mixer.music.load(self.current_audio_file)
            pygame.mixer.music.play()

    def show_word(self):
        if self.current_word:
            self.word_label.configure(
                text=self.current_word,
                text_color="#4349fc"  # you can change reveal color here
            )
            self.label.configure(text="This word is:")

# ---------- GUI ----------
root = ctk.CTk()
root.title("English Spelling App")
root.geometry("600x500")

app = SpellingApp(root)
root.mainloop()