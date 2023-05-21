from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QHBoxLayout, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont, QPainter, QBrush, QImage, QPalette, QColor
from PyQt5.QtCore import Qt, QTimer
import json


# Load room data from JSON file
with open('rooms.json') as f:
    room_data = json.load(f)

# Convert room names to valid JSON keys
rooms = {name.replace(" ", "_"): info for name, info in room_data.items()}

state = {
    'current_room': 'start',
    'hp': 100
}


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Set image as background
        palette = QPalette()
        image = QImage("C:/Users/ausli/Desktop/space.jpg")  # Update with your image path
        palette.setBrush(QPalette.Background, QBrush(image))
        self.setPalette(palette)

        self.text = QTextEdit(self)
        self.text.setFont(QFont('Arial', 18))
        self.text.setReadOnly(True)
        # Set the text edit to transparent and text color to black
        self.text.setStyleSheet("background: transparent; color: black; border: none")
        # Add a drop shadow effect to make the black text more readable
        shadow = QGraphicsDropShadowEffect(self.text)
        shadow.setBlurRadius(5)
        shadow.setXOffset(1)
        shadow.setYOffset(1)
        shadow.setColor(Qt.white)
        self.text.setGraphicsEffect(shadow)

        self.health_bar = QLabel(self)
        self.health_bar.setFixedSize(100, 20)
        self.health_value = QLabel(self)
        self.health_value.setFont(QFont('Arial', 12))

        # Create a layout for the health bar and center it
        self.health_layout = QHBoxLayout()
        self.health_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.health_layout.addWidget(self.health_value)
        self.health_layout.addWidget(self.health_bar)
        self.health_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addLayout(self.health_layout)
        self.setLayout(self.layout)

        self.buttons = []

        self.update_room()

        # Resize the window
        self.resize(1024, 768)

    def update_room(self):
        room = rooms[state['current_room']]
        self.text.clear()
        self.text.append(room['text'] + "\n\n")
        self.update_health_bar()
        for button in self.buttons:
            self.layout.removeWidget(button)
            button.deleteLater()
        self.buttons.clear()
        for i, option in enumerate(room['options']):
            button_text, _, _ = option
            button = QPushButton(button_text)
            button.setFont(QFont('Arial', 12))
            button.setStyleSheet("background-color: black; color: pink; border-style: outset; border-width: 2px; border-radius: 10px; border-color: beige;")
            button.clicked.connect(lambda checked, option=option: self.choose_option(option))
            self.layout.addWidget(button)
            self.buttons.append(button)

    def update_health_bar(self):
        current_hp = state['hp']
        if current_hp >= 101:
            health_color = QColor(Qt.green)
        elif current_hp <= 99:
            health_color = QColor(Qt.red)
        else:
            health_color = QColor(Qt.blue)

        # Change the HP bar text to white
        self.health_value.setStyleSheet("color: white")
        self.health_value.setText(f"HP: {current_hp}")
        self.health_bar.setText("")
        self.health_bar.setStyleSheet(f"background-color: {health_color.name()}")

    def choose_option(self, option):
        _, next_room, hp_delta = option
        state['current_room'] = next_room
        state['hp'] += hp_delta
        self.update_room()
        message = ""
        if hp_delta < 0:
            message = "\nOOOF! That was not a wise choice."
        elif hp_delta > 0:
            message = "\nYay! You feel replenished."
        else:
            message = "\nGood choice! You chose wisely."
        self.text.append(message)
        QTimer.singleShot(3000, lambda: self.remove_text(message))  # Message will be removed after 3 seconds

    def remove_text(self, message):
        current_text = self.text.toPlainText()
        self.text.setPlainText(current_text.replace(message, ''))


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
