# Flash-APP

Dies ist eine interaktive Python-Lernanwendung, die entwickelt wurde, um Python-Grundlagen und -Fortgeschrittenenkenntnisse auf spielerische Weise zu vermitteln. Die Anwendung enthält zwei Hauptmodule: ein Flashcard-Lernspiel und ein Quiz.

# Flashcard-Lernspiel
Das Flashcard-Lernspiel ermöglicht es den Benutzern, Python-Grundlagen durch das Durchgehen von Fragen und Antworten zu lernen. Die Fragen werden in Form von Karteikarten präsentiert, wobei der Benutzer die Antwort anzeigen und dann überprüfen kann, ob sie richtig ist. Das Spiel enthält verschiedene Kategorien von Fragen und bietet eine angenehme Lernerfahrung durch spielerische Effekte wie Sounds und Grafiken.

# Quiz
Das Quiz-Modul bietet eine weitere Möglichkeit, das Python-Wissen zu testen. Es enthält eine Reihe von Fragen mit mehreren Antwortoptionen. Der Benutzer kann die Fragen beantworten und erhält am Ende des Quiz eine Punktzahl basierend auf der Anzahl der korrekten Antworten.

# Dateistruktur
flashcard_class.py: Enthält die Hauptklasse für das Flashcard-Lernspiel.
quiz_class.py: Enthält die Hauptklasse für das Quiz.
level_indicator.py: Implementiert eine Klasse zur Anzeige des aktuellen Spiel- oder Quiz-Levels.
stat_tracker.py: Implementiert eine Klasse zur Verfolgung von Spielerstatistiken, wie z.B. die Anzahl der gesehenen Karten oder die Anzahl der korrekten Quiz-Antworten.
main.py: Startet die Anwendung und initialisiert die benötigten Klassen.
user_data.json: Speichert die Benutzerdaten, einschließlich des aktuellen Punktestands und der freigeschalteten Spiel- oder Quiz-Levels.
questions.json: Enthält die Fragen und Antworten für das Quiz in JSON-Format.
deck.json: Enthält die Fragen und Antworten für das Flashcard-Lernspiel in JSON-Format.
