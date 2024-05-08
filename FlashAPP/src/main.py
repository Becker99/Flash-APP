import tkinter as tk
from quiz_app import FlashcardApp, StatTracker


if __name__ == "__main__":
    player_name = "lelon"
    root = tk.Tk()
    s = StatTracker()
    app = FlashcardApp(root, s)
    root.mainloop()

    # learn-stats
    s.export_flashcards(player_name)
    s.export_quiz(player_name)

