import tkinter as tk

class LevelStyleController:
    def __init__(self, root, level_style):
        self.root = root
        self.level_style = level_style

    def apply_level_style(self):
        self.root.configure(bg=self.level_style.get("root", "#3ca094"))
        self.apply_style_to_children(self.root)

    def apply_style_to_children(self, parent):
        for child in parent.winfo_children():
            if isinstance(child, tk.Frame):
                child.configure(bg=self.level_style.get("root", "#3ca094"))
                self.apply_style_to_children(child)
            elif isinstance(child, tk.Label):
                child.configure(bg=self.level_style.get("Label", "#3ca094"))
            elif isinstance(child, tk.Button):
                child.configure(bg=self.level_style.get("button", "#3ca094"))
            elif isinstance(child, tk.Radiobutton):
                child.configure(bg=self.level_style.get("button", "#3ca094"))
