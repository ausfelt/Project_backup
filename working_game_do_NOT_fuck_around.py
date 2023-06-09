import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Game state
state = {
    'current_room': 'start',
    'hp': 100
}

rooms = {
    "start": {
        "text": "You stand in your great grandfather's house...",
        "options": [
            ("Search for clues", "start", 0),
            ("Fight the dragon", "start", -10),
            ("Chill with the ghost", "start", -10),
            ("Open his old rum", "room1", 0),
            ("Leave for the next room", "start", -10),
        ],
    },
    "room1": {
        "text": "You're in the library, the first room, and there are books covered with dust...",
        "options": [
            ("Read a book", "room1", -10),
            ("Search for secret doors", "room2", 0),
            ("Rest for a while", "room1", +10),
            ("Go back", "start", 0),
            ("Speak with Kel'Thuzad", "room1", -10),
        ],
    },
    "room2": {
        "text": "You made it to the next room, a cavernous room with a chest in the center...",
        "options": [
            ("Open the chest", "room2", 0),
            ("Inspect the room for traps", "room2", 0),
            ("Eat a snack", "room2", -10),
            ("Go back", "room1", -10),
            ("Investigate the papers on the table", "room3", 0),

        ],
    },
    "room3": {
        "text": "You're now in the bathroom, the third room, and it has NOT been cleaned for a while...",
        "options": [
            ("Clean the bathroom", "room3", +10),
            ("Go for a number two", "room3", 0),
            ("Kill the enormous spider", "room3", 0),
            ("Go back", "room2", -10),
            ("Read the vintage porno magazine hidden in the cabinet", "room4", +10),
        ],
    },
    "room4": {
        "text": "After a good read you find yourself in a giant hallway, with stairs to the second floor. Should i \n"
                "go for it...?",
        "options": [
            ("Eat an old pizza crust from the floor", "room4", -10),
            ("Examine the paintings on the wall", "room4", 0),
            ("Sprint to the stairs before the ghost eats your kidneys", "room5", +10),
            ("Fall asleep", "room4", 0),
            ("Smoke some of the sweet dank great grandpa left under a floorboard", "room4", +10),
        ],
    },
    "room5": {
        "text": "You are now on the second floor. It smells of death, but also chicken...",
        "options": [
            ("Find the source of the chicken smell", "room5", -10),
            ("Search for more dank", "room5", 0),
            ("Go to the bedroom", "room6", +10),
            ("Try to remember why you are here", "room5", 0),
            ("What is life anyway? You contemplate and time flies", "room5", -10),
        ],
    },
    "room6": {
        "text": "You are now in the bedroom. You now know where the smell come from. Apparently he had a chicken farm \n"
                "in his bedroom? All of them are dead, except one. It seems demonic and you try to communicate with it...",
        "options": [
            ("Why are you still alive??!", "room6", 0),
            ("What happened here?", "room6", 0),
            ("For whom do you speak?", "room6", 0),
            ("Kill the demon chicken! Maybe i will get his powers?", "room7", +10),
            ("Clean up the room", "room6", 0),
        ],
    },
    "room7": {
        "text": "You feel stronger after killing the demon chicken but eating it raw was probably not the best choice...",
        "options": [
            ("Throw up", "room7", -10),
            ("Embrace the extreme nausea", "room7", -10),
            ("Rest for a while", "room7", +10),
            ("Climb the ladder to the attic", "room8", 0),
            ("Bring the papers you found to read later. They're written in a strange language, almost alien...", "room7", +10),
        ],
    },
    "room8": {
        "text": "You are now in the attic and the asbestos is everywhere. Luckily you ate the chicken and is unharmed.\n"
                "Maybe i should eat more raw demon chicken? Or was it the last one in existence? Now one knows, for now...",
        "options": [
            ("Use the strange translation device you find in the corner of the room", "room9", 0),
            ("Eat all the asbestos just because you can", "room8", 0),
            ("Look for more demon chicken", "room8", 0),
            ("Go through some boxes. It says 'classified' on them and 'Area 51 property...'", "room8", 0),
            ("Jump out of the window because you are scared", "end", -210),
        ],
    },
    "room9": {
        "text": "You use the translation device and the language is in face alien. From a species of alien living in \n"
                "Area 51 that has inhabited the earth for centuries. They come from the Andromeda Galaxy and they \n"
                "teach humans how to advance in technology. But the weirdest part is that your name is mentioned \n"
                "several times. Almost like are of some importance you don't understand yet. You hear a load bang \n"
                "outside and you think 'This is it'",
        "options": [
            ("Defend yourself against whatever comes at you", "room9", -10),
            ("Say a silent prayer and accept your fate", "room9", 0),
            ("Go and check what is the cause of the bang", "room10", +10),
            ("Hide in the corner", "room9", -10),
            ("Is it the dank from before that is playing with my mind?", "room9", 0),
        ],
    },
    "room10": {
        "text": "You are outside and you see a bright light. it fills you with warmth. You see 5 large figures, pale \n"
                "in skin tone and a large frame. They speak but you don't understand...",
        "options": [
            ("Try to fight them", "end", -200),
            ("Use the translation device. Maybe it can translate speech as well", "room11", +20),
            ("Faint and shit yourself", "room10", -10),
            ("Stand there paralyzed. like an idiot, and just stare", "room10", 0),
            ("Scream at the top of your lungs, thinking it will scare them for some reason", "room10", 0),
        ],
    },
    "room11": {
        "text": "'We are the Annunaki. We come in peace. You have a curious mind, just like your great grandfather. \n"
                "If you are ready, we have the truth you have been looking for your whole life. Are you ready \n"
                "to hear it, Sebastian?'",
        "options": [
            ("How do they know my name? You faint again", "room11", -10),
            ("Holy shit they are HUGE", "room11", 0),
            ("'Please, tell me truth'", "room12", +10),
            ("Try to run for your life, but your feet can't move", "room11", 0),
            ("'Am i becoming psychotic?", "room11", 0),
        ],
    },
    "room12": {
        "text": "'We can only tell you the truth if you are really prepared to hear it. You might think you are but \n"
                "in reality you might not be. You can ask us questions first, but only ask us questions you are \n"
                "ready to accept the truth. We are not responsible for what your mind is capable of comprehending...'",
        "options": [
            ("Why are you here?", "room12", -10),
            ("Who was my great grandfather, really?", "room13", +10),
            ("Do you have a recepie for space pizza?", "room12", 0),
            ("Thinking for yourself, 'The truth really was out there the whole time'", "room12", 0),
            ("Take your gun and end it. 'This is to much, i can't handle it'", "end", -300),
        ],
    },
    "room13": {
        "text": "'You are asking a great question. Your great grandfather was actually a descendant from us. Do you \n"
                "understand what that means to you?'",
        "options": [
            ("I don't even know you are real. I smoked a fat one before", "room13", 0),
            ("I understand that i am scared", "room13", 0),
            ("Do you have any space weed?", "room13", +10),
            ("How can he be an alien and I am human?", "room14", +10),
            ("I need to think...", "room13", +10),
        ],
    },
    "room14": {
        "text": "What says that you are human? You have always felt out of place, been much taller and stronger than \n"
                "your peers. You have had almost an obsession with space your whole life. You have been drawn to the \n"
                "Annunaki lore and 'myths' since you went to middle school. I'm surprised you have not been able to \n"
                "connect the dots yet. But then again, your whole family kept it a secret from you your whole life. \n"
                "Only your great grandfather, Ninhursag, who you called Jeff thought you had the right to know. And \n"
                "for that we are grateful and that is also why we are here now. You have to make a choice. A choice \n"
                "that will change your life.",
        "options": [
            ("Hold on, what? I'm an alien?", "room14", 0),
            ("Why did my family thought this was something to hide?", "room14", 0),
            ("What is the choice i have to make?", "room15", +10),
            ("'I can't believe this. An alien? What else have they been keeping from me?", "room14", 0),
            ("You start crying, don't know what to feel. Is it happiness? Sadness? Both? Neither?", "room14", +10),
        ],
    },
    "room15": {
        "text": "You have to choose if you want to come with us to our home planet, Planet X that you have been told \n"
                "is a wild conspiracy. We have wanted to keep it that way so the rest of earths population can live \n"
                "in peace. They would not be able to handle a truth like that. The planet is a part of our solar system \n"
                "but its trajectory is a very wide oval and it only passes close to earth every 15000 years. Now is \n"
                "the time that Planet X is close to earth but it will only stay close for 3 more days and then the \n"
                "window closes. Do you want to join us and explore the universe, or do you wish to live a human life, \n"
                "devoid of all you have ever dreamt of.",
        "options": [
            ("Holy shit, are you guys serious?", "room15", -10),
            ("'But if i leave, i have to leave my family behind. I am not ready to do that'", "room15", 0),
            ("You are awestruck since everything you have read about this subject is TRUE. You stand \n"
            "there in silence", "room15", 0),
            ("Get a heart attack", "end", -300),
            ("Please tell me more. I want to join, but i also have family here. I can't just leave them", "room16", +10),
        ],
    },
    "room16": {
        "text": "Your whole family, as we said before, are the same species as us. It was them who alerted us that you \n"
                "were going to investigate Jeffs house. And we knew you would find the truth. If you choose to leave \n"
                "earth behind, your family will follow.",
        "options": [
            ("This is all i have dreamt of, and my family will join me. Of course i will join you", "room17", +10),
            ("I'm still a little sceptic. I need a breather since i feel a panic attack is coming \nmy way", "room16",
             -10),
            ("Stand in silence. How can you trust them? You have only spoken to them for about \n30 minutes", "room16",
             0),
            (
            "I feel they are being sincere, and who would make such an elaborate prank? I will join them", "room17", 0),
            (
            "No way, José. 'I'd rather die than to follow you liars. I have heard about aliens \nand the butt stuff. I'm not into that.'",
            "room16", -50),
        ],
    },
    "room17": {
        "text": "You have made the right choice. Please join us to the ship and will leave for Planet X, also \n"
                "known as Nibiru. You will finally come home.",
        "options": [
            ("I march straight to the ship", "room18", 0),
            ("Well this is not what expected when i woke up this morning", "room17", 0),
            ("This is too good to be true. Am i still tripping?", "room17", -10),
            (
            "You pinch yourself in the arm, thinking it's all a dream but it is not. I join my \nbrothers in a voyage to explore the cosmos",
            "room18", +10),
            ("I just need to go back and get a, uuuh, important magazine", "room18", +10),
        ],
    },
    "room18": {
        "text": "You are in the spaceship now. It's so much bigger on the inside than you could have imagined from \n"
                "when you saw it from the outside. But i don't complain. This is me. This is my destiny",
        "options": [
            ("You feel a feeling you have never felt before. Is this real joy?", "room18", 0),
            ("You explore the ship and push some buttons", "end", -300),
            ("So, where are we going after we have been to Nibiru?", "room19", +10),
            ("You eat something you find on the floor, again. And now you have alien food poisoning", "room18", -30),
            ("Read the vintage porno magazine, again. This is the only pictures you have of humans \n"
             "that you will carry with you around the universe. You keep it so you never forget what \n"
             "other humans than your family looks like. Even if it is a bit explicit", "room18", +10),
        ],
    },
    "room19": {
        "text": "My great grandfather comes to visit me. He says: 'This was the only way I could get you to \n"
                "investigate. I did not have the courage to tell you myself; I did not want you to believe \n"
                "I was crazy, so I faked my death so you could find the truth by yourself. I hope you can forgive me. \n"
                "The rest of my family gathers as well and life feels good. It feels right for the first time in \n"
                "my life. It's all come together. I feel joy. I feel happiness. I am home.'",
        "options": [
            ("Give him a big hug", "end", 0),
            ("I throw up because of the alien food poisoning", "end", 0),
            ("I wonder what's next. I feel like this is only the beginning of my journey", "end", 0),
            ("We land on Nibiru and in all my excitement I run out without any protective gear and \n"
             "I die immediately. My body was still programmed to be on Earth and they hadn't \n"
             "calibrated me yet", "end", -500),
            ("Take a big inhale of the space weed. Life is good", "end", 0)
        ]
    },

    "end": {
        "text": "You have found the truth... or have you?",
        "options": [],
    },
}

# Function to update the GUI to reflect the current room
def update_room():
    room = rooms[state['current_room']]
    text.delete(1.0, tk.END)
    text.insert(tk.END, room['text'] + "\n\n")
    for button in option_buttons:
        button.pack_forget()
    for i, option in enumerate(room['options']):
        button_text, _, _ = option
        command = lambda option=option: choose_option(option)
        button = tk.Button(frame, text=button_text, command=command, bg='teal', fg='black', font=('Arial', 12))  # Set button color
        button.pack(side=tk.TOP, fill=tk.X)
        option_buttons.append(button)

# Function to update game state
def choose_option(option):
    global state
    _, state['current_room'], hp_delta = option
    state['hp'] += hp_delta
    hp_label.config(text="HP: " + str(state['hp']))
    hp_progress['value'] = state['hp']  # Update progress bar
    if state['hp'] <= 0:
        messagebox.showinfo("Game Over", "You have died.")
        root.quit()
    else:
        update_room()
        if hp_delta < 0:
            text.insert(tk.END, "\nOuch! OOF that was dumb.")
        elif hp_delta > 0:
            text.insert(tk.END, "\nYay! You feel replenished.")
        else:
            text.insert(tk.END, "\nGood choice! You chose wisely.")

# Create the GUI
root = tk.Tk()
root.configure(bg='teal')  # Set background color
frame = tk.Frame(root, bg='teal')  # Set frame color
frame.pack()
text = tk.Text(frame, wrap=tk.WORD, bg='black', fg='white', font=('Arial', 18))  # Set text background and font color
text.pack()
hp_label = tk.Label(root, text="HP: 100", bg='black', fg='white', font=('Arial', 18))  # Set HP label background and font color
hp_label.pack()
hp_progress = ttk.Progressbar(root, length=100, mode='determinate')  # Create progress bar
hp_progress.pack()
hp_progress['value'] = 100  # Initial HP value
option_buttons = []
update_room()
root.mainloop()