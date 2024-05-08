import tkinter as tk
import os

BP = os.path.realpath(os.path.join(os.path.realpath(__file__), "../../../.."))

class LevelIndicator(tk.Frame):
    def __init__(self, master=None, levels=3):
        super().__init__(master)
        self.levels = levels
        self.configure(bg="#3ca094")
        self.current_level = 0
        self.indicators = []


        # Load image for the indicator
        self.image_on = tk.PhotoImage(file=f"{BP}/FlashAPP/data/indicator_on.png")
        self.image_off = tk.PhotoImage(file=f"{BP}/FlashAPP/data/indicator_off.png")

        # Add labels for each level
        for i in range(levels):
            level_label = tk.Label(self, text=f"Level {i}", font=("Helvetica", 12), bg= '#3ca094')
            level_label.grid(row=0, column=i, pady=5)

            indicator = tk.Label(self, image=self.image_off, relief=tk.FLAT, bg= '#3ca094')
            indicator.grid(row=1, column=i, padx=5, pady=5)
            self.indicators.append(indicator)

        self.pack()

    def set_level(self, level):
        if 0 <= level < self.levels:
            self.current_level = level
            for i, indicator in enumerate(self.indicators):
                if i == level:
                    indicator.config(image=self.image_on)
                else:
                    indicator.config(image=self.image_off)


if __name__ == "__main__":
    root = tk.Tk()
    level_indicator = LevelIndicator(root, levels=3)
    level_indicator.set_level(1)
    level_indicator.pack()
    root.mainloop()