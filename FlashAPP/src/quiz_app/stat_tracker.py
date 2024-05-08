from typing import Dict, Tuple
import os
import matplotlib.pyplot as plt
import numpy as np

BP = os.path.realpath(os.path.join(os.path.realpath(__file__), "../../../.."))


class StatTracker:
    def __init__(self):
        self.categories = None
        self.n_flashcards = None
        self.seen_flashcards = None
        self.n_questions = None
        self.correct_questions = None

    def set_flashcards(self, categories: Dict[str, int], n_flashcards: int):
        self.categories = {k: [categories[k], 0] for k in categories.keys()}
        self.n_flashcards = n_flashcards
        self.seen_flashcards = 0

    def set_quiz(self, n_questions):
        self.n_questions = n_questions
        self.correct_questions = 0

    def inc_flashcards(self, category: str):
        self.categories[category][-1] += 1
        self.seen_flashcards += 1

    def inc_questions(self):
        self.correct_questions += 1

    @staticmethod
    def factorize(x: int) -> Tuple[int, int]:
        a, b, c = 1, 1, 0
        while True:
            if a * b >= x:
                return a, b
            else:
                if c % 2 == 0:
                    a += 1
                else:
                    b += 1
            c += 1

    def export_flashcards(self, exp_name: str):
        dir_path = f"{BP}/FlashAPP/data/{exp_name}"
        os.makedirs(dir_path, exist_ok=True)
        pie_chart_categories = ["bekannt", "unbekannt"]
        colors = ("cyan", "beige")
        wp = {'linewidth': 1, 'edgecolor': "green"}

        def func(pct, allvalues):
            absolute = int(pct / 100. * np.sum(allvalues))
            return "{:.1f}%\n({:d} g)".format(pct, absolute)

        nrows, ncols = self.factorize(len(list(self.categories.keys())) + 1)
        fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(15, 7))
        ax = ax.flatten()
        plt.subplots_adjust(hspace=0.4, wspace=0.2)

        for idx, category in enumerate(self.categories):
            plt.subplot(nrows, ncols, idx + 1)
            data = self.categories[category][1], self.categories[category][0] - self.categories[category][1]
            wedges, texts, autotexts = ax[idx].pie(data,
                                                     autopct=lambda pct: func(pct, data),
                                                     # explode=explode,
                                                     labels=pie_chart_categories,
                                                     shadow=True,
                                                     colors=colors,
                                                     startangle=90,
                                                     wedgeprops=wp,
                                                     textprops=dict(color="magenta"))

            ax[idx].legend(wedges, pie_chart_categories,
                             title="Fortschritt",
                             loc="center left",
                             bbox_to_anchor=(1, 0, 0.5, 1))

            plt.setp(autotexts, size=8, weight="bold")
            ax[idx].set_title(category)

        idx += 1
        plt.subplot(nrows, ncols, idx + 1)
        data = self.seen_flashcards, self.n_flashcards - self.seen_flashcards
        wedges, texts, autotexts = ax[idx].pie(data,
                                               autopct=lambda pct: func(pct, data),
                                               # explode=explode,
                                               labels=pie_chart_categories,
                                               shadow=True,
                                               colors=colors,
                                               startangle=90,
                                               wedgeprops=wp,
                                               textprops=dict(color="magenta"))

        ax[idx].legend(wedges, pie_chart_categories,
                       title="Fprtschritt",
                       loc="center left",
                       bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(autotexts, size=8, weight="bold")
        ax[idx].set_title("Total")
        for idx in range(idx + 1, ncols * nrows + 1):
            try:
                plt.subplot(nrows, ncols, idx + 1)
                ax[idx].axis('off')
            except:
                pass
        plt.tight_layout()
        plt.savefig(f"{dir_path}/learning_stats.png")
        plt.show()

    def export_quiz(self, exp_name: str):
        dir_path = f"{BP}/stats/data/{exp_name}"
        os.makedirs(dir_path, exist_ok=True)
        pie_chart_categories = ["richtig", "falsch"]
        colors = ("cyan", "brown")
        wp = {'linewidth': 1, 'edgecolor': "green"}

        def func(pct, allvalues):
            absolute = int(pct / 100. * np.sum(allvalues))
            return "{:.1f}%\n({:d} g)".format(pct, absolute)

        fig, ax = plt.subplots(figsize=(15, 7))
        plt.subplots_adjust(hspace=0.4, wspace=0.2)

        data = self.correct_questions, self.n_questions - self.correct_questions
        wedges, texts, autotexts = ax.pie(data,
                                               autopct=lambda pct: func(pct, data),
                                               # explode=explode,
                                               labels=pie_chart_categories,
                                               shadow=True,
                                               colors=colors,
                                               startangle=90,
                                               wedgeprops=wp,
                                               textprops=dict(color="magenta"))

        ax.legend(wedges, pie_chart_categories,
                       title="Score",
                       loc="center left",
                       bbox_to_anchor=(1, 0, 0.5, 1))

        plt.setp(autotexts, size=8, weight="bold")
        ax.set_title("Score")
        plt.tight_layout()
        plt.savefig(f"{dir_path}/score.png")
        plt.show()


if __name__ == "__main__":
    pass