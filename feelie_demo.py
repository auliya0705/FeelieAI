import tkinter as tk
from tkinter import Canvas, Scrollbar
import threading, re, time

# Optional Text-to-Speech
try:
    import pyttsx3
    TTS_AVAILABLE = True
except:
    TTS_AVAILABLE = False


# ======================
#   BDI-like Emotion Logic
# ======================
class FeelieMind:
    def __init__(self):
        self.emotion_dict = {
            "angry": ["angry", "mad", "furious", "annoyed", "upset"],
            "sad": ["sad", "disappointed", "cry", "lonely", "hurt"],
            "happy": ["happy", "glad", "excited", "joy", "smile"],
            "afraid": ["scared", "afraid", "worried", "anxious"],
            "ashamed": ["shy", "ashamed", "embarrassed", "nervous"],
            "proud": ["proud", "great", "confident"],
            "calm": ["calm", "relaxed", "peaceful"],
            "neutral": []
        }

    def detect_emotion(self, text):
        text = text.lower()
        for emo, words in self.emotion_dict.items():
            if any(w in text for w in words):
                return emo
        return "neutral"

    def get_response(self, text, emotion):
        text = text.lower()

        if "friend" in text or "bimo" in text and emotion in ["angry", "sad"]:
            return (
                "Hmm, sounds like you feel really upset. You tried to take care of your ruler, "
                "but it got broken. I can understand why you're angry 😔"
            )

        if "broke" in text or "laugh" in text:
            return (
                "Oh, that must've made you even more upset. If I were you, I'd feel frustrated too. "
                "You want your friend to understand you're upset, but you don't want to start a fight, right?"
            )

        if "don't want to fight" in text or "want him to understand" in text:
            return (
                "That's amazing! You can think clearly even while you're mad 💛\n\n"
                "Maybe you can tell him something like:\n"
                "'I felt sad when you played with my stuff without asking. It made me upset.'\n\n"
                "That way, he knows you're upset, but you're also polite and honest."
            )

        if "okay" in text or "maybe" in text and "calm" not in text:
            return (
                "Great! You're being brave and kind 🌟\n"
                "That shows you're learning to manage your feelings.\n"
                "Now, let's take a deep breath together 🌬️\n"
                "In... two... three... and slowly out...\n"
                "How do you feel now? A bit calmer?"
            )

        if "calm" in text:
            return (
                "I'm glad you're feeling calmer 🩵\n"
                "Maybe later you can share this story with your mom — she'll be proud of you for learning from it!"
            )

        if "thank" in text:
            return (
                "You're welcome 😊 I'm always here to listen!\n"
                "You're kind and brave for talking about your feelings 💖\n"
                "Now, let's think of something fun — want to play an emotion guessing game or draw together?"
            )

        # default empathy
        if emotion == "angry":
            return "I can tell you're angry 😡. It's okay to feel that way when something bothers you."
        if emotion == "sad":
            return "You sound a little sad 😢. It's okay, I'm here to listen."
        if emotion == "happy":
            return "Yay! You sound happy today! 🌈"
        if emotion == "afraid":
            return "You feel scared... that's okay, everyone feels that sometimes 🤗"
        return "That's interesting! Tell me more about what happened 💬"


# ======================
#   Interactive Chat UI with Fun Design
# ======================
class FeelieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Feelie — Your Empathy Friend 🤖💙")
        self.root.geometry("900x750")
        self.root.configure(bg="#E8F8FF")

        self.mind = FeelieMind()

        if TTS_AVAILABLE:
            self.tts = pyttsx3.init()
            self.tts.setProperty("rate", 150)

        # Enhanced color schemes with gradients
        self.color_themes = {
            "angry": {
                "bg_start": "#FF6B6B",
                "bg_end": "#FFE66D",
                "user_bubble": "#FFE5E5",
                "bot_bubble": "#FFF4E6",
                "header": "#E63946"
            },
            "sad": {
                "bg_start": "#A8DADC",
                "bg_end": "#457B9D",
                "user_bubble": "#E3F2FD",
                "bot_bubble": "#BBDEFB",
                "header": "#1D3557"
            },
            "happy": {
                "bg_start": "#FFF77F",
                "bg_end": "#FFD166",
                "user_bubble": "#FFF9C4",
                "bot_bubble": "#FFECB3",
                "header": "#F77F00"
            },
            "afraid": {
                "bg_start": "#D4A5A5",
                "bg_end": "#9381FF",
                "user_bubble": "#E1D5E7",
                "bot_bubble": "#D4BEE4",
                "header": "#6A4C93"
            },
            "ashamed": {
                "bg_start": "#FFB3D9",
                "bg_end": "#FF6B9D",
                "user_bubble": "#FFE1EC",
                "bot_bubble": "#FFD6E8",
                "header": "#C9184A"
            },
            "proud": {
                "bg_start": "#B8F2E6",
                "bg_end": "#52B788",
                "user_bubble": "#D8F3DC",
                "bot_bubble": "#B7E4C7",
                "header": "#2D6A4F"
            },
            "calm": {
                "bg_start": "#CAF0F8",
                "bg_end": "#90E0EF",
                "user_bubble": "#E0F7FA",
                "bot_bubble": "#B2EBF2",
                "header": "#0077B6"
            },
            "neutral": {
                "bg_start": "#E8F8FF",
                "bg_end": "#C7ECFF",
                "user_bubble": "#E1F5FE",
                "bot_bubble": "#B3E5FC",
                "header": "#4A90E2"
            }
        }

        self.current_emotion = "neutral"
        self.build_ui()
        self.bot_message("Hi there! 👋 I'm Feelie, your friend who's always here to listen! 😊\n\nHow are you feeling today?")

    def build_ui(self):
        # Decorative header with gradient effect
        self.header = tk.Frame(self.root, bg="#4A90E2", height=100)
        self.header.pack(fill=tk.X)
        self.header.pack_propagate(False)

        # Feelie character (big emoji that changes)
        self.bot_character = tk.Label(
            self.header,
            text="🤖",
            bg="#4A90E2",
            fg="white",
            font=("Segoe UI Emoji", 45)
        )
        self.bot_character.pack(side=tk.LEFT, padx=25, pady=10)

        # Title area
        title_frame = tk.Frame(self.header, bg="#4A90E2")
        title_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.title_label = tk.Label(
            title_frame,
            text="Feelie",
            bg="#4A90E2",
            fg="white",
            font=("Comic Sans MS", 26, "bold")
        )
        self.title_label.pack(anchor="w", pady=(15, 0))

        self.subtitle_label = tk.Label(
            title_frame,
            text="Your Empathy Friend 💙",
            bg="#4A90E2",
            fg="#E8F8FF",
            font=("Comic Sans MS", 13)
        )
        self.subtitle_label.pack(anchor="w")

        # Current emotion indicator
        emotion_frame = tk.Frame(self.header, bg="#4A90E2")
        emotion_frame.pack(side=tk.RIGHT, padx=25)

        tk.Label(
            emotion_frame,
            text="You feel:",
            bg="#4A90E2",
            fg="white",
            font=("Comic Sans MS", 11)
        ).pack()

        self.emotion_display = tk.Label(
            emotion_frame,
            text="😊",
            bg="#4A90E2",
            fg="white",
            font=("Segoe UI Emoji", 35)
        )
        self.emotion_display.pack()

        # Decorative line
        separator = tk.Frame(self.root, bg="#87CEEB", height=3)
        separator.pack(fill=tk.X)

        # Scrollable chat area
        self.canvas_frame = tk.Frame(self.root, bg="#E8F8FF")
        self.canvas_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(15, 10))

        self.canvas = Canvas(
            self.canvas_frame,
            bg="#E8F8FF",
            highlightthickness=0,
            bd=0
        )
        
        self.scrollbar = Scrollbar(
            self.canvas_frame,
            orient="vertical",
            command=self.canvas.yview,
            width=15,
            bg="#B3E5FC",
            troughcolor="#E1F5FE",
            bd=0,
            highlightthickness=0
        )
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(fill=tk.BOTH, expand=True, side="left")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.chat_frame = tk.Frame(self.canvas, bg="#E8F8FF")
        self.canvas_window = self.canvas.create_window((0, 0), window=self.chat_frame, anchor="nw")

        self.chat_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Make canvas resize properly
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width)
        )

        # Input area with modern design
        input_container = tk.Frame(self.root, bg="#E8F8FF")
        input_container.pack(fill=tk.X, padx=20, pady=(0, 20))

        # Input wrapper for rounded effect
        input_wrapper = tk.Frame(input_container, bg="white", bd=2, relief=tk.SOLID)
        input_wrapper.pack(fill=tk.X, pady=5)

        self.input = tk.Text(
            input_wrapper,
            height=3,
            font=("Segoe UI", 12),
            wrap=tk.WORD,
            bd=0,
            highlightthickness=0,
            padx=10,
            pady=10
        )
        self.input.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.input.bind("<Return>", self.enter_pressed)

        # Styled send button
        self.send_btn = tk.Button(
            input_wrapper,
            text="Send 💬",
            bg="#4CAF50",
            fg="white",
            font=("Comic Sans MS", 12, "bold"),
            command=self.send_message,
            bd=0,
            padx=20,
            pady=10,
            cursor="hand2",
            activebackground="#45A049",
            activeforeground="white"
        )
        self.send_btn.pack(side=tk.RIGHT, padx=5, pady=5)

    def create_bubble(self, text, side="left", color="#FFFFFF", text_color="#000000"):
        """Create a chat bubble with rounded corners effect"""
        bubble_container = tk.Frame(self.chat_frame, bg=self.canvas["bg"])
        bubble_container.pack(
            anchor="w" if side == "left" else "e",
            pady=(5, 10),
            padx=15,
            fill="x"
        )

        # Icon/Avatar
        if side == "right":
            avatar = tk.Label(
                bubble_container,
                text="🤖",
                bg=self.canvas["bg"],
                font=("Segoe UI Emoji", 20)
            )
            avatar.pack(side=tk.RIGHT, padx=(10, 0))

        # Bubble frame with shadow effect
        shadow = tk.Frame(bubble_container, bg="#C0C0C0", bd=0)
        shadow.pack(
            side="left" if side == "left" else "right",
            padx=(0, 2) if side == "left" else (2, 0),
            pady=(2, 0)
        )

        bubble = tk.Frame(shadow, bg=color, bd=0)
        bubble.pack()

        # Message text
        msg_label = tk.Label(
            bubble,
            text=text,
            wraplength=500,
            justify="left",
            bg=color,
            fg=text_color,
            font=("Comic Sans MS", 11),
            padx=18,
            pady=12
        )
        msg_label.pack()

        if side == "left":
            avatar = tk.Label(
                bubble_container,
                text="👤",
                bg=self.canvas["bg"],
                font=("Segoe UI Emoji", 20)
            )
            avatar.pack(side=tk.LEFT, padx=(0, 10))

        # Animate bubble entrance
        self.animate_bubble(bubble_container)

        # Auto scroll to bottom
        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

    def animate_bubble(self, widget):
        """Simple fade-in animation"""
        # Start with slightly transparent-looking background
        original_bg = widget.cget("bg")
        
        def fade_in(step=0):
            if step < 5:
                widget.after(30, lambda: fade_in(step + 1))

        fade_in()

    def user_message(self, msg):
        theme = self.color_themes.get(self.current_emotion, self.color_themes["neutral"])
        self.create_bubble(msg, "left", theme["user_bubble"], "#000000")

    def bot_message(self, msg):
        theme = self.color_themes.get(self.current_emotion, self.color_themes["neutral"])
        self.create_bubble(msg, "right", theme["bot_bubble"], "#000000")
        
        if TTS_AVAILABLE:
            threading.Thread(target=self.speak, args=(msg,), daemon=True).start()

    def typing_indicator(self):
        """Show typing animation"""
        theme = self.color_themes.get(self.current_emotion, self.color_themes["neutral"])
        
        typing_frame = tk.Frame(self.chat_frame, bg=self.canvas["bg"])
        typing_frame.pack(anchor="e", pady=5, padx=15)

        typing_bubble = tk.Frame(typing_frame, bg=theme["bot_bubble"], bd=0)
        typing_bubble.pack(side=tk.RIGHT, padx=(2, 0))

        typing_label = tk.Label(
            typing_bubble,
            text="● ● ●",
            bg=theme["bot_bubble"],
            fg="#666666",
            font=("Comic Sans MS", 11),
            padx=18,
            pady=12
        )
        typing_label.pack()

        avatar = tk.Label(
            typing_frame,
            text="🤖",
            bg=self.canvas["bg"],
            font=("Segoe UI Emoji", 20)
        )
        avatar.pack(side=tk.RIGHT, padx=(10, 0))

        self.canvas.update_idletasks()
        self.canvas.yview_moveto(1.0)

        return typing_frame

    def speak(self, text):
        clean = re.sub(r"[^\w\s.,!?]", "", text)
        self.tts.say(clean)
        self.tts.runAndWait()

    def enter_pressed(self, e):
        if not (e.state & 0x1):
            self.send_message()
            return "break"

    def send_message(self):
        msg = self.input.get("1.0", tk.END).strip()
        if not msg:
            return
        self.input.delete("1.0", tk.END)
        self.user_message(msg)
        
        # Show typing indicator
        typing = self.typing_indicator()
        
        threading.Thread(
            target=self.process_response,
            args=(msg, typing),
            daemon=True
        ).start()

    def process_response(self, msg, typing_widget):
        # Simulate thinking time
        time.sleep(1.2)
        
        emotion = self.mind.detect_emotion(msg)
        response = self.mind.get_response(msg, emotion)

        # Update UI on main thread
        self.root.after(0, self._update_ui_with_response, emotion, response, typing_widget)

    def _update_ui_with_response(self, emotion, response, typing_widget):
        # Remove typing indicator
        typing_widget.destroy()
        
        # Change theme smoothly
        self.change_theme(emotion)
        
        # Show bot response
        self.bot_message(response)

    def change_theme(self, emotion):
        """Smoothly transition to new emotion theme"""
        if emotion == self.current_emotion:
            return
        
        self.current_emotion = emotion
        theme = self.color_themes.get(emotion, self.color_themes["neutral"])

        # Update colors
        new_bg = theme["bg_end"]
        self.root.configure(bg=new_bg)
        self.canvas.configure(bg=new_bg)
        self.chat_frame.configure(bg=new_bg)
        self.canvas_frame.configure(bg=new_bg)
        
        # Update header
        header_color = theme["header"]
        self.header.configure(bg=header_color)
        self.bot_character.configure(bg=header_color)
        self.title_label.configure(bg=header_color)
        self.subtitle_label.configure(bg=header_color)
        self.emotion_display.configure(bg=header_color)
        
        # Find emotion frame (parent of emotion_display)
        for child in self.header.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=header_color)
                for subchild in child.winfo_children():
                    if isinstance(subchild, tk.Label):
                        subchild.configure(bg=header_color)

        # Update emoji
        emoji = self.get_emoji(emotion)
        self.emotion_display.config(text=emoji)
        
        # Animate bot character
        self.animate_bot_character(emotion)

    def animate_bot_character(self, emotion):
        """Animate bot character based on emotion"""
        expressions = ["🤖", self.get_emoji(emotion), "🤖"]
        
        def animate(index=0):
            if index < len(expressions):
                self.bot_character.config(text=expressions[index])
                self.root.after(200, lambda: animate(index + 1))
        
        animate()

    def get_emoji(self, emo):
        emojis = {
            "angry": "😠",
            "sad": "😢",
            "happy": "😊",
            "afraid": "😨",
            "ashamed": "😳",
            "proud": "😎",
            "calm": "😌",
            "neutral": "🙂"
        }
        return emojis.get(emo, "🙂")


if __name__ == "__main__":
    root = tk.Tk()
    app = FeelieApp(root)
    root.mainloop()