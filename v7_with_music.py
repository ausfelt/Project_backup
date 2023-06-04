from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QTextEdit, QHBoxLayout, QSpacerItem, QSizePolicy, QGraphicsDropShadowEffect, QMessageBox
from PyQt5.QtGui import QFont, QPainter, QBrush, QImage, QPalette, QColor
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import json
import sys
import os


# Check if JSON file exists and can be read
filename = 'rooms.json'
if not os.path.isfile(filename):
    print(f"Error: File '{filename}' does not exist.")
    exit()

# Check if JSON file is correctly formatted
try:
    with open(filename, encoding='utf-8') as f:
        room_data = json.load(f)
except ValueError as e:
    print(f"Error: The file '{filename}' contains invalid JSON data.")
    print(f"Exception: {e}")
    exit()

# Check if required keys exist in JSON data
required_keys = ['text', 'options']
for room, room_info in room_data.items():
    for key in required_keys:
        if key not in room_info:
            print(f"Error: Missing key '{key}' in room '{room}'.")
            exit()

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
        image = QImage("C:/Users/ausli/Desktop/space2.jpg")  # Update with your image path
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
        self.health_value.setFont(QFont('Arial', 14))

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

        self.start_button = QPushButton("Start")
        self.start_button.setFont(QFont('Arial', 36, QFont.Bold))
        self.start_button.setStyleSheet("background-color: black; color: pink; border-style: outset; border-width: 3px; border-radius: 10px; border-color: orange")
        self.start_button.clicked.connect(self.start_game)

        self.start_layout = QVBoxLayout()
        self.start_layout.addItem(QSpacerItem(40, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.start_layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        self.start_layout.addItem(QSpacerItem(40, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.layout.addLayout(self.start_layout)

        self.buttons = []

        # Resize the window
        self.resize(1024, 576)

        # Background music
        self.background_music = QMediaPlayer(self)
        self.background_music.setMedia(QMediaContent(QUrl.fromLocalFile("C:/Users/ausli/Desktop/04_Underworld.mp3")))  # Update with the path to your music file
        self.background_music.setVolume(50)
        self.background_music.stateChanged.connect(self.check_music_state)

    def check_music_state(self, state):
        # Check the state of the background music
        if state == QMediaPlayer.StoppedState:
            # If the music has stopped, play it again
            self.background_music.play()

    def start_game(self):
        # Start the game by removing the start button and updating the room
        self.layout.removeItem(self.start_layout)
        self.start_button.deleteLater()
        self.start_button = None
        self.update_room()
        self.play_background_music()

    def update_room(self):
        # Update the current room's text, options, and health bar
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
            button.setStyleSheet("background-color: black; color: pink; border-style: outset; border-width: 3px; border-radius: 10px; border-color: orange;")
            button.clicked.connect(lambda checked, option=option: self.choose_option(option))
            self.layout.addWidget(button)
            self.buttons.append(button)

        if state['current_room'] == 'end':
            self.show_end_message()

    def update_health_bar(self):
        # Update the health bar based on the current HP value
        current_hp = state['hp']
        if current_hp >= 101:
            health_color = QColor(Qt.green)
        elif current_hp == 100:
            health_color = QColor(Qt.blue)
        else:
            health_color = QColor(Qt.red)

        # Change the HP bar text to white
        self.health_value.setStyleSheet("color: white")
        self.health_value.setText(f"HP: {current_hp}")
        self.health_bar.setText("")
        self.health_bar.setStyleSheet(f"background-color: {health_color.name()}")

        if current_hp <= 0:
            self.show_end_message()

    def choose_option(self, option):
        # Handle the player's choice of an option
        _, next_room, hp_delta = option
        state['current_room'] = next_room
        state['hp'] += hp_delta
        if state['hp'] <= 0:
            state['hp'] = 0
        self.update_room()
        message = ""
        if hp_delta < 0:
            message = "\nOOOF! That was not a wise choice."
        elif hp_delta > 0:
            message = "\nYay! You feel replenished."
        else:
            message = "\nYou feel indifferent."
        self.text.append(message)
        QTimer.singleShot(3000, lambda: self.remove_text(message))  # Message will be removed after 3 seconds

        sender = self.sender()
        sender.setCursor(Qt.ArrowCursor)

    def remove_text(self, message):
        # Remove a specific message from the text area
        current_text = self.text.toPlainText()
        self.text.setPlainText(current_text.replace(message, ''))

    def handle_end_message(self, button):
        # Handle the button click in the end message box
        if button.text() == "OK":
            self.centered_message_box.close()
            self.stop_background_music()
            QApplication.quit()

    def show_end_message(self):
        # Show the end message when the game ends
        if state['hp'] <= 0:
            message = "YOU DIED"
            color = "red"
        else:
            message = "D̶͈̰̙̠̘̜͈̒͊O̷̧̲̙̱̖̻̥̳̿͌͛̓̐̅̆̏͝ ̴̟̰͉͉̣̤͔͙̠͚̮̦͙͊̒̈̕͘͜ͅN̶̪̞̖͎̜̰͛̃O̵̢͔͂̄͐̈̒͐͝T̶͍̖͙̜͉̝͉͖͙͍͈̖̪͍̘̃̉̊̇͘̕ ̵̯̈́̓͜F̸̡͓̳̳̲̘̼͍͚̬̮̌̓̈́̌̀̈́̒̓͗̉̈͝͝Ǫ̷̰̙̂͊̀́͑̅̊͠͝͝Ļ̷̧̢̻̰̱̖̲̮̟̈́̀̈́̾͋͐̓̈̍̅L̸̨̠̠̱̻̫͉̝̥̮̜̅̃͑͝Ǫ̶̪̪̺̘̝̗͚̂̀͑͜Ẃ̴̨͔͎̪̥̬͍͓̮̤͔̬̱͌̿̇̚͝͠ ̴̙̜͓̝͍̘͈̩̖̖̝͍̝͕͊͂͑ͅṰ̷̡͔͉͍̂̈́̿̆̓̔͗̽͛͝H̷̢̤̠͈͍̬̹̖̬̻̜̭̬̟̾̃̍̐̿͌͌̈́̅͜͠Ȩ̴̡̨̛̭̙̗̤͚̤̼̞̾̌̇͗͑̈̂̾̎̃̐̿̀ͅM̴̡̠̺͎̘͍͕̭̜̪͔̥̹͈̣̾̌͌͋̅̊̍̂͌̓̚"
            color = "purple"

        self.centered_message_box = QMessageBox()
        self.centered_message_box.setWindowTitle("Game Over" if state['hp'] <= 0 else "D̶͈̰̙̠̘̜͈̒͊O̷̧̲̙̱̖̻̥̳̿͌͛̓̐̅̆̏͝ ̴̟̰͉͉̣̤͔͙̠͚̮̦͙͊̒̈̕͘͜ͅN̶̪̞̖͎̜̰͛̃O̵̢͔͂̄͐̈̒͐͝T̶͍̖͙̜͉̝͉͖͙͍͈̖̪͍̘̃̉̊̇͘̕ ̵̯̈́̓͜F̸̡͓̳̳̲̘̼͍͚̬̮̌̓̈́̌̀̈́̒̓͗̉̈͝͝Ǫ̷̰̙̂͊̀́͑̅̊͠͝͝Ļ̷̧̢̻̰̱̖̲̮̟̈́̀̈́̾͋͐̓̈̍̅L̸̨̠̠̱̻̫͉̝̥̮̜̅̃͑͝Ǫ̶̪̪̺̘̝̗͚̂̀͑͜Ẃ̴̨͔͎̪̥̬͍͓̮̤͔̬̱͌̿̇̚͝͠ ̴̙̜͓̝͍̘͈̩̖̖̝͍̝͕͊͂͑ͅṰ̷̡͔͉͍̂̈́̿̆̓̔͗̽͛͝H̷̢̤̠͈͍̬̹̖̬̻̜̭̬̟̾̃̍̐̿͌͌̈́̅͜͠Ȩ̴̡̨̛̭̙̗̤͚̤̼̞̾̌̇͗͑̈̂̾̎̃̐̿̀ͅM̴̡̠̺͎̘͍͕̭̜̪͔̥̹͈̣̾̌͌͋̅̊̍̂͌̓̚")
        self.centered_message_box.setText(message)
        self.centered_message_box.setStyleSheet(f"background-color: {color}; color: white; font-size: 24px;")

        screen_geometry = QApplication.desktop().availableGeometry()
        message_box_geometry = self.centered_message_box.frameGeometry()
        x = (screen_geometry.width() - message_box_geometry.width()) // 2
        y = (screen_geometry.height() - message_box_geometry.height()) // 2
        self.centered_message_box.move(x, y)

        self.centered_message_box.setStandardButtons(QMessageBox.Ok)
        self.centered_message_box.buttonClicked.connect(self.handle_end_message)
        self.centered_message_box.exec_()

        # Stop the background music when the game ends
        self.stop_background_music()

    def play_background_music(self):
        # Play the background music
        self.background_music.play()

    def stop_background_music(self):
        # Stop the background music and reset the position to the beginning
        self.background_music.stop()
        self.background_music.setPosition(0)  # Reset the position to the beginning

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    window.play_background_music()  # Start playing the background music
    sys.exit(app.exec_())