import tkinter as tk
from tkinter import messagebox

# Quiz data
quiz_questions = [
    {"question": "What is the capital of France?", "options": ["Berlin", "Madrid", "Paris", "Rome"], "answer": 2},
    {"question": "Which planet is known as the Red Planet?", "options": ["Earth", "Mars", "Jupiter", "Venus"], "answer": 1},
    {"question": "Who wrote 'Hamlet'?", "options": ["Charles Dickens", "William Shakespeare", "Mark Twain", "Leo Tolstoy"], "answer": 1},
    {"question": "What is the largest ocean?", "options": ["Atlantic", "Indian", "Arctic", "Pacific"], "answer": 3},
    {"question": "What is the powerhouse of the cell?", "options": ["Nucleus", "Mitochondria", "Ribosome", "Chloroplast"], "answer": 1},
    {"question": "Which country invented pizza?", "options": ["France", "Italy", "Greece", "Spain"], "answer": 1},
    {"question": "Who painted the Mona Lisa?", "options": ["Van Gogh", "Picasso", "Leonardo da Vinci", "Michelangelo"], "answer": 2},
    {"question": "How many continents are there?", "options": ["5", "6", "7", "8"], "answer": 2},
    {"question": "Which gas do plants absorb?", "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"], "answer": 2},
    {"question": "Which element has the symbol 'O'?", "options": ["Oxygen", "Gold", "Osmium", "Oganesson"], "answer": 0}
]

# Quiz Class
class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz App")
        self.root.geometry("500x400")

        self.question_index = 0
        self.score = 0
        self.user_answer = tk.IntVar()

        self.create_widgets()
        self.display_question()

    def create_widgets(self):
        self.label_question = tk.Label(self.root, text="", font=("Arial", 14), wraplength=400, justify="center")
        self.label_question.pack(pady=20)

        self.radio_buttons = []
        for i in range(4):
            rb = tk.Radiobutton(self.root, text="", variable=self.user_answer, value=i, font=("Arial", 12))
            self.radio_buttons.append(rb)
            rb.pack(anchor="w")

        self.button_next = tk.Button(self.root, text="Next", command=self.next_question, font=("Arial", 12))
        self.button_next.pack(pady=20)

    def display_question(self):
        question_data = quiz_questions[self.question_index]
        self.label_question.config(text=f"Q{self.question_index + 1}: {question_data['question']}")

        for i, option in enumerate(question_data["options"]):
            self.radio_buttons[i].config(text=option)

    def next_question(self):
        if self.user_answer.get() == quiz_questions[self.question_index]["answer"]:
            self.score += 1

        self.question_index += 1

        if self.question_index < len(quiz_questions):
            self.display_question()
        else:
            self.show_results()

    def show_results(self):
        messagebox.showinfo("Quiz Completed", f"Your score: {self.score}/{len(quiz_questions)}")
        self.root.quit()

# Running the GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
