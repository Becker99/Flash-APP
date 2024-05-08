import json
import tkinter as tk
import random
from typing import Optional

from PIL import Image, ImageTk
from .quiz_class import QuizApp
from .level_indicator import LevelIndicator
from .stat_tracker import StatTracker
import os
from pygame import mixer

BP = os.path.realpath(os.path.join(os.path.realpath(__file__), "../../../.."))


class FlashcardApp:
    def __init__(self, root, stat_tracker: Optional[StatTracker] = None):
        self.root = root
        self.root.title("Flashcard Part")
        self.root.geometry("800x600")
        self.root.configure(bg="#3ca094")

        with open(f'{BP}/FlashAPP/data/deck.json', 'r') as f:
            self.deck = []
            self.category_mapping = {}
            self.categories = {}
            temp = json.load(f)["deck"]
            for inst in temp:
                self.deck.append(inst[:2])
                self.category_mapping[inst[0]] = inst[2]
                if inst[2] in self.categories:
                    self.categories[inst[2]] += 1
                else:
                    self.categories[inst[2]] = 1
        print(self.category_mapping)
        print(self.categories)
        self.count = len(self.deck)
        self.current_question_index = 0
        if stat_tracker is not None:
            self.stat_tracker = stat_tracker
            self.stat_tracker.set_flashcards(categories=self.categories, n_flashcards=self.count)

        # Labels
        self.question_label = tk.Label(root, text="", font=("Helvetica", 25), bg="#3ca094", wraplength=700)
        self.question_label.place(relx=0.5, rely=0.1, anchor="n")


        self.answer_label = tk.Label(root, text="", font=("Helvetica", 15), bg="#3ca094")
        self.answer_label.place(relx=0.5, rely=0.5, anchor='center')

        # Create Buttons
        self.button_frame = tk.Frame(root, bg="#3ca094")
        self.button_frame.place(relx=0.5, rely=0.85, anchor='s')  # Adjust the rely option as needed

        self.show_button = tk.Button(self.button_frame, text="Show", command=self.show_flashcard)
        self.show_button.grid(row=0, column=0, padx=20)

        self.next_button = tk.Button(self.button_frame, text="Next", command=self.next_flashcard)
        self.next_button.grid(row=0, column=1, padx=20)

        # Finish Button to move to the next Level
        self.finish_button = tk.Button(self.button_frame, text="Finish", command=self.finish_flashcard)
        self.finish_button.grid(row=0, column=2, padx=20)

        # Footer Section
        app_description = "Hinweis: Dies ist eine Quiz-App und das Spiel hat 3 vorgegebene Level mit unterschiedlichem Schwierigkeitsgrad. Die Fragen, mit denen Sie ein Level abschließen, öffnen das nächste Level. Viel Spaß beim Spielen!"
        contact_info = "Customer Service: alexbecker999@hotmail.com"
        self.create_footer(app_description, contact_info)

        # Run next function when the program starts
        self.next_flashcard()

        self.root.mainloop()

    def next_flashcard(self):
        # Clear Screen
        self.answer_label.config(text="")
        # Create random selection
        if self.current_question_index < self.count:
            self.question_label.config(text=self.deck[self.current_question_index][0])
            self.current_question_index += 1
        else:
            # When all questions have been run through, shuffle the order again and reset the index
            random.shuffle(self.deck)
            self.current_question_index = 0
            self.next_flashcard()

    def show_flashcard(self):
        # Play sound
        mixer.init()
        mixer.music.load(os.path.join(BP, 'FlashAPP/data/show_sound.mp3'))
        mixer.music.play()
        self.answer_label.config(text=self.deck[self.current_question_index - 1][1])
        if self.stat_tracker is not None:
            self.stat_tracker.inc_flashcards(self.category_mapping[self.deck[self.current_question_index - 1][0]])

    def finish_flashcard(self):
        # Transition to the quiz
        self.root.destroy()  # Close the current window
        self.open_quiz_app()

    def open_quiz_app(self):
        quiz_root = tk.Tk()  # Create a new window for the quiz
        quiz_app = QuizApp(quiz_root, self.stat_tracker)  # Pass the level_indicator instance to QuizApp

    def create_footer(self, app_description, contact_info):
        footer_frame = tk.Frame(self.root, bg="#3ca094")
        footer_frame.pack(side="bottom", pady=10)

        description_label = tk.Label(footer_frame, text=app_description, font=("Helvetica", 10), bg="#3ca094", wraplength=600)
        description_label.pack(anchor="w")

        contact_label = tk.Label(footer_frame, text=contact_info, font=("Helvetica", 10), bg="#3ca094")
        contact_label.pack()


if __name__ == "__main__":
    print(BP)
    r = tk.Tk()
    s = StatTracker()
    app = FlashcardApp(r, s)
    r.mainloop()
    print(s.seen_flashcards)
