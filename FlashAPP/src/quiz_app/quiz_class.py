import tkinter as tk
from tkinter import ttk
from typing import Optional, Dict, Any

from PIL import Image, ImageTk
import json
import os
from pygame import mixer
from .level_indicator import LevelIndicator
from .stat_tracker import StatTracker
BP = os.path.realpath(os.path.join(os.path.realpath(__file__), "../../../.."))


class QuizApp:
    def __init__(self, root: tk.Tk, stat_tracker: Optional[StatTracker] = None):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("900x500")  # Set the window size to 900x500
        self.root.configure(bg="#3ca094")
        self.current_question_index = 0
        self.score = 0
        self.levels = ["Level 0", "Level 1", "Level 2"]
        self.unlocked_levels = [0]

        # Load the quiz end image
        self.quiz_end_image_path = f'{BP}/FlashAPP/data/fertig.png'
        self.quiz_end_image = Image.open(self.quiz_end_image_path)
        self.quiz_end_image = ImageTk.PhotoImage(self.quiz_end_image)

        # Create Level Indicator
        self.level_indicator = LevelIndicator(root, levels=3)
        # Load questions from JSON file
        self.load_questions()
        self.stat_tracker = stat_tracker
        if stat_tracker is not None:

            self.stat_tracker.set_quiz(self.count_questions(self.questions))
        # Load user data (score and unlocked levels) from JSON file
        self.load_user_data()

        self.question_label = tk.Label(root, text="", font=("Helvetica", 12), bg= '#3ca094')
        self.question_label.pack(pady=30)

        #self.level_label = tk.Label(root, text="", font=("Helvetica", 12), bg= '#3ca094')
        #self.level_label.pack()

        self.radio_var = tk.StringVar()
        self.radio_var.set(-1)
        self.radio_buttons = []
        for i in range(4):
            radio_button = tk.Radiobutton(root, text="", variable=self.radio_var, value=i)
            radio_button.pack(anchor=tk.W, padx=200)  # Setze padx=250 für 250 Pixel Abstand vom linken Rand
            self.radio_buttons.append(radio_button)

        self.next_button = tk.Button(root, text="Next question", command=self.next_question)
        self.next_button.pack(pady=30)

        # create restart_button  reset_data_button
        self.create_buttons()

        #restart_button = tk.Button(root, text="Restart", command=self.restart_quiz)
        #restart_button.pack(side="left", padx=200,  pady=10)

        #reset_data_button = tk.Button(root, text="Reset Data", command=self.reset_data)
       # reset_data_button.pack(side="left",padx=10, pady=10)

        self.display_question()

        # Divider
        # self.create_divider(20)


        # Footer Section
        app_description = "Hinweis: Dies ist eine Quiz-App und das Spiel hat 3 vorgegebene Level mit unterschiedlichem Schwierigkeitsgrad. Die Fragen, mit denen Sie ein Level abschließen, öffnen das nächste Level. Viel Spaß beim Spielen!"
        contact_info = "Customer Service: alexbecker999@hotmail.com"
        self.create_footer(app_description, contact_info)

    @staticmethod
    def count_questions(dic: Dict[str, Any]) -> int:
        count = 0
        for lvl in dic:
            count += len(dic[lvl])
        return count

    def load_questions(self):
        try:
            with open(f'{BP}/FlashAPP/data/questions.json', 'r') as file:
                self.questions = json.load(file)
        except FileNotFoundError:
            print("The 'questions.json' file was not found.")
            self.questions = {}
        except json.JSONDecodeError:
            print("Error parsing JSON data from 'questions.json'. Make sure it is well-formatted.")
            self.questions = {}

    def load_user_data(self):
        try:
            with open(f'{BP}/FlashAPP/data/user_data.json', 'r') as file:
                user_data = json.load(file)
                self.score = user_data.get('score', 0)
                self.current_level = user_data.get('current_level', 0)
                self.unlocked_levels = user_data.get('unlocked_levels', [0])
        except FileNotFoundError:
            print("The 'user_data.json' file was not found.")
        except json.JSONDecodeError:
            print("Error parsing JSON data from 'user_data.json'. Make sure it is well-formatted.")

    def save_user_data(self):
        data = {
            "score": self.score,
            "current_level": self.current_level,
            "unlocked_levels": self.unlocked_levels
        }
        with open(f'{BP}/task1/data/user_data.json', 'w') as file:
            json.dump(data, file)

    def reset_user_data(self):
        data = {"score": 0, "current_level": 0, "unlocked_levels": [0]}
        with open(f'{BP}/FlashAPP/data/user_data.json', 'w') as file:
            json.dump(data, file)

    def display_question(self):
        if self.current_level < len(self.levels):
            level = self.levels[self.current_level]
            if self.current_question_index < len(self.questions.get(level, [])):
                question_data = self.questions[level][self.current_question_index]
                self.question_label.config(text=question_data["question"], bg='#3ca094')
                # self.level_label.config(text=f"Current Level: {level}", bg= '#3ca094')
                options = question_data["options"]
                for i in range(4):
                    self.radio_buttons[i].config(text=options[i], bg= '#3ca094')
                self.radio_var.set(-1)
            else:
                self.end_level()
        else:
            self.end_quiz()

    def next_question(self):
        if self.current_level < len(self.levels):
            if self.current_question_index < len(self.questions.get(self.levels[self.current_level], [])):
                selected_option = int(self.radio_var.get())
                if selected_option != -1:
                    question_data = self.questions[self.levels[self.current_level]][self.current_question_index]
                    if question_data["options"][selected_option] == question_data["answer"]:
                        self.score += 1
                        if self.stat_tracker is not None:
                            self.stat_tracker.inc_questions()
                    self.current_question_index += 1
                    self.display_question()
            else:
                self.end_level()
        else:
            self.end_quiz()
        self.update_user_data()
        self.level_indicator.set_level(self.current_level)

    def reset_data(self):
        self.reset_user_data()
        self.load_user_data()

    def restart_quiz(self):
        # Transition to the quiz
        self.root.destroy()
        del self.root
        self.reset_data()
        del self
        root = tk.Tk()
        QuizApp(root)
        root.mainloop()

    def end_level(self):
        self.current_question_index = 0
        if self.current_level < len(self.levels) - 1:
            self.current_level += 1
            self.unlocked_levels.append(self.current_level)
            self.display_question()
        else:
            self.end_quiz()  # All levels completed

    def end_quiz(self):
        total_questions = sum(len(questions) for questions in self.questions.values())
        
        # Play sound based on score
        mixer.init()
        if self.score < 5:
            mixer.music.load(os.path.join(BP, 'FlashAPP/data/badresult.mp3'))
            self.question_label.config(text="Leider haben Sie das Quiz nicht bestanden. Ihr Score ist {}/{}. Versuchen Sie es erneut!".format(self.score, total_questions), fg='red', font=("Helvetica", 14, 'bold'))
        else:
            mixer.music.load(os.path.join(BP, 'FlashAPP/data/goodresult.mp3'))
            self.question_label.config(text="Herzlichen Glückwunsch! Ihr Score ist {}/{}. Sie sind bereit für die Prüfung!".format(self.score, total_questions), fg='white', font=("Helvetica", 14, 'bold'))

        mixer.music.play()

        # Remove radio buttons
        for radio_button in self.radio_buttons:
            radio_button.destroy()

        # Remove the "Next question" button
        self.next_button.destroy()

        # Display quiz end image
        quiz_end_label = tk.Label(self.root, image=self.quiz_end_image, bg='#3ca094')
        quiz_end_label.place(relx=0.5, rely=0.5, anchor="center")

        self.radio_var.set(-1)
        self.save_user_data()


    def create_footer(self, app_description, contact_info):
        footer_frame = tk.Frame(self.root, bg="#3ca094")
        footer_frame.pack(side="bottom", pady=10)

        description_label = tk.Label(footer_frame, text=app_description, font=("Helvetica", 10), bg="#3ca094", wraplength=600)
        description_label.pack(anchor="w")

        contact_label = tk.Label(footer_frame, text=contact_info, font=("Helvetica", 10), bg="#3ca094")
        contact_label.pack()

    def create_buttons(self):
        button_frame = tk.Frame(self.root, bg='#3ca094')
        button_frame.place(relx=0.5, rely=0.75, anchor="s")  # Position at y-coordinate 400

        restart_button = tk.Button(button_frame, text="Restart", command=self.restart_quiz)
        restart_button.pack(side="left", padx=10, pady=10)

        reset_data_button = tk.Button(button_frame, text="Reset Data", command=self.reset_data)
        reset_data_button.pack(side="right", padx=10, pady=10)

        # Label to display the user's current level
        button_frame2 = tk.Frame(self.root, bg='#3ca094')
        button_frame2.place(relx=0.5, rely=0.80, anchor="s")  # Position at y-coordinate 400

        current_level_label = tk.Label(button_frame2, text="Level: 0", font=("Helvetica", 10), bg="#3ca094")
        current_level_label.pack(side="left", padx=10)

        # Label to display the user's score
        score_label = tk.Label(button_frame2, text="Score: 0", font=("Helvetica", 10), bg="#3ca094")
        score_label.pack(side="right", padx=10)

        self.current_level_label = current_level_label
        self.score_label = score_label

    def create_divider(self, height):
        separator = ttk.Separator(self.root, orient="horizontal")
        separator.pack(fill="x", pady=height)
        separator.pack(fill="x")

    # Update the current level and score labels
    def update_user_data(self):
        self.current_level_label.config(text=f"Level: {self.current_level}")
        self.score_label.config(text=f"Score: {self.score}")


if __name__ == "__main__":
    print(BP)
    r = tk.Tk()
    app = QuizApp(r)
    r.mainloop()