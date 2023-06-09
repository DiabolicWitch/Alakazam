import sys
import openai
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTextEdit, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

def read_api_key_from_file():
    with open("key.txt", "r") as file:
        api_key = file.read().strip()
        return api_key

api_key = read_api_key_from_file()
openai.api_key = api_key

def read_prompt():
    with open("prompt.txt", "r") as file:
        content = file.read()
        messages = [{"role": "system", "content": content}]
        return messages

messages = read_prompt()

class Alakazam(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alakazam GPT")
        self.setGeometry(100, 100, 400, 400)

        self.layout = QVBoxLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        #Adiciona ícone ao programa
        icon = QIcon("Alakazam.ico")
        self.setWindowIcon(icon)


        self.answer_label = QLabel("Alakazam respondeu:")
        self.answer_label.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.answer_label)

        self.answer_textedit = QTextEdit()
        self.answer_textedit.setStyleSheet("font-size: 13px; background-color: #FFFFFF; border: 3px groove #8C5C0F")
        self.answer_textedit.setReadOnly(True)
        self.layout.addWidget(self.answer_textedit, stretch=5)

        self.question_label = QLabel("Pergunte ao Alakazam:")
        self.question_label.setStyleSheet("font-size: 14px;")
        self.layout.addWidget(self.question_label)

        self.question_textedit = QTextEdit()
        self.question_textedit.setStyleSheet("font-size: 13px; background-color: #F0F0F0; border: 3px groove #8C5C0F")
        self.layout.addWidget(self.question_textedit, stretch=1)

        self.submit_button = QPushButton("Enviar")
        self.submit_button.setStyleSheet("background-color: #E9CE82; border: 2px solid #8C5C0F")
        self.layout.addWidget(self.submit_button)

        self.setCentralWidget(self.widget)

        self.submit_button.clicked.connect(self.submit_question)

    def Custom(self, user_input):
        messages.append({"role": "user", "content": user_input})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        ChatGPT_reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": ChatGPT_reply})
        return ChatGPT_reply

    def submit_question(self):
        question = self.question_textedit.toPlainText()
        answer = self.Custom(question)
        self.answer_textedit.setPlainText(answer)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            self.submit_question()
        else:
            super().keyPressEvent(event)

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("QMainWindow { background-color: #EEEAAA; }")  # Substitua pelo caminho da sua imagem
    window = Alakazam()
    window.show()
    sys.exit(app.exec_())

main()