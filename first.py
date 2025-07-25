import tkinter as tk
import requests
import threading
import random

# Vibrant color palette
BG_COLORS = ["#f0f4f8", "#ffe066", "#f38181", "#95e1d3", "#fce38a", "#eaffd0", "#a8d8ea", "#f7cac9", "#b5ead7", "#ffb347"]
JOKE_EMOJIS = ["😂", "🤣", "😹", "😆", "😜", "😎", "🤪", "😺", "😹", "😻", "😹"]

JOKE_API_URLS = [
    # Official Joke API
    "https://official-joke-api.appspot.com/jokes/random",
    # JokeAPI (safe mode)
    "https://v2.jokeapi.dev/joke/Any?type=single&safe-mode",
    # Chuck Norris
    "https://api.chucknorris.io/jokes/random"
]

class JokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("😂 Funniest Joke Machine 😂")
        self.bg_color = random.choice(BG_COLORS)
        self.root.configure(bg=self.bg_color)
        self.root.geometry("600x350")
        self.root.minsize(400, 250)
        self.root.resizable(False, False)

        # Header
        self.header = tk.Label(
            root, text="Joke of the Moment!", font=("Comic Sans MS", 24, "bold"),
            bg=self.bg_color, fg="#2d3a4b", pady=10
        )
        self.header.pack(pady=(20, 0))

        # Emoji
        self.emoji_label = tk.Label(
            root, text=random.choice(JOKE_EMOJIS), font=("Arial", 40),
            bg=self.bg_color
        )
        self.emoji_label.pack(pady=(0, 10))

        # Joke text
        self.joke_var = tk.StringVar()
        self.joke_label = tk.Label(
            root, textvariable=self.joke_var, wraplength=520,
            font=("Segoe UI", 16, "bold"), bg=self.bg_color, fg="#333",
            justify=tk.CENTER, padx=20, pady=20, relief=tk.RIDGE, bd=3
        )
        self.joke_label.pack(expand=True, fill=tk.BOTH, padx=30, pady=(0, 10))

        # Next joke button
        self.next_btn = tk.Button(
            root, text="🤣 Next Joke! ", command=self.get_joke,
            bg="#4f8cff", fg="white", font=("Arial", 14, "bold"),
            activebackground="#357ae8", activeforeground="#fff",
            relief=tk.RAISED, bd=4, cursor="hand2", padx=18, pady=8,
            highlightthickness=0
        )
        self.next_btn.pack(pady=(0, 20))

        # Status
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(
            root, textvariable=self.status_var, font=("Arial", 10),
            bg=self.bg_color, fg="#888"
        )
        self.status_label.pack()

        self.get_joke()

    def get_joke(self):
        self.joke_var.set("Fetching a hilarious joke... Please wait!")
        self.emoji_label.config(text=random.choice(JOKE_EMOJIS))
        self.status_var.set("")
        threading.Thread(target=self._fetch_joke, daemon=True).start()

    def _fetch_joke(self):
        for _ in range(3):  # Try up to 3 times
            api_url = random.choice(JOKE_API_URLS)
            try:
                resp = requests.get(api_url, timeout=5)
                if resp.status_code == 200:
                    joke = self.parse_joke(api_url, resp.json())
                    if joke:
                        self.show_joke(joke)
                        return
            except Exception as e:
                continue
        self.show_joke("😢 Sorry, couldn't fetch a joke right now. Check your internet connection!")
        self.status_var.set("Network error. Try again later.")

    def parse_joke(self, api_url, data):
        if "official-joke-api" in api_url:
            return f"{data.get('setup', '')}\n{data.get('punchline', '')}".strip()
        elif "jokeapi" in api_url:
            return data.get('joke')
        elif "chucknorris" in api_url:
            return data.get('value')
        return None

    def show_joke(self, joke):
        self.joke_var.set(joke)
        self.emoji_label.config(text=random.choice(JOKE_EMOJIS))

if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        import sys
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
        import requests
    root = tk.Tk()
    app = JokeApp(root)
    root.mainloop()