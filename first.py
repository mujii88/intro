import tkinter as tk
import random
import os
import json

# List of jokes
JOKES = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the math book look sad? Because it had too many problems.",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "Why don't programmers like nature? It has too many bugs.",
    "Why do we tell actors to 'break a leg?' Because every play has a cast!",
    "Parallel lines have so much in common. It’s a shame they’ll never meet.",
    "Why did the computer go to the doctor? Because it had a virus!",
    "Why was the math lecture so long? The professor kept going off on a tangent.",
    "Why did the bicycle fall over? Because it was two-tired!",
    "Why did the tomato turn red? Because it saw the salad dressing!"
]

# File to store shown jokes
JOKE_STATE_FILE = os.path.expanduser("~/.joke_gui_state.json")

def get_unseen_jokes():
    if os.path.exists(JOKE_STATE_FILE):
        try:
            with open(JOKE_STATE_FILE, 'r') as f:
                state = json.load(f)
            shown = set(state.get('shown', []))
        except Exception:
            shown = set()
    else:
        shown = set()
    unseen = [j for j in JOKES if j not in shown]
    return unseen, shown

def mark_joke_as_shown(joke):
    if os.path.exists(JOKE_STATE_FILE):
        try:
            with open(JOKE_STATE_FILE, 'r') as f:
                state = json.load(f)
            shown = set(state.get('shown', []))
        except Exception:
            shown = set()
    else:
        shown = set()
    shown.add(joke)
    with open(JOKE_STATE_FILE, 'w') as f:
        json.dump({'shown': list(shown)}, f)

def reset_joke_state():
    if os.path.exists(JOKE_STATE_FILE):
        os.remove(JOKE_STATE_FILE)

class JokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Joke of the Day!")
        self.root.geometry("500x300")
        self.root.configure(bg="#f0f4f8")
        self.joke_label = tk.Label(
            root, text="", wraplength=440, font=("Arial", 16, "bold"),
            bg="#f0f4f8", fg="#2d3a4b", justify=tk.CENTER, pady=30
        )
        self.joke_label.pack(expand=True)
        self.next_btn = tk.Button(
            root, text="Next Joke", command=self.show_joke,
            bg="#4f8cff", fg="white", font=("Arial", 12, "bold"),
            activebackground="#357ae8", relief=tk.RAISED, bd=3, cursor="hand2"
        )
        self.next_btn.pack(pady=10)
        self.show_joke()

    def show_joke(self):
        unseen, shown = get_unseen_jokes()
        if not unseen:
            reset_joke_state()
            unseen, shown = get_unseen_jokes()
            msg = "You've seen all the jokes! Starting over..."
            self.joke_label.config(text=msg)
            self.root.after(1500, self.show_joke)
            return
        joke = random.choice(unseen)
        self.joke_label.config(text=joke)
        mark_joke_as_shown(joke)

if __name__ == "__main__":
    root = tk.Tk()
    app = JokeApp(root)
    root.mainloop()