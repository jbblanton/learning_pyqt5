from PyQt5 import QtCore
from PyQt5.QtGui import QCursor, QPixmap
from PyQt5.QtWidgets import QLabel, QPushButton, QGridLayout

import json
import pandas as pd
import random
import requests


# Initialize the layout
grid = QGridLayout()


# Fetch the list of questions
r = requests.get("https://opentdb.com/api.php?amount=20&category=18&difficulty=medium&type=multiple")

data = r.text
data = json.loads(data)['results']  # list of objects


def get_index():
    # If there are more questions, keep going!
    if len(data) > 0:
        index = random.randint(0, len(data))
        print(index)
        return index
    # If not, check the score for winning or losing scores
    elif parameters['score'][-1] >= 80:
        win_game()
    else:
        lose_game()
        #return None


def load_question_data(i):
    '''Grab a question object from the list and parse out the elements'''

    print(i)
    if i == None:
        lose_game()

    question = data[i]['question']
    correct = data[i]['correct_answer'] 
    wrong = data[i]['incorrect_answers']

    # Remove that question object to prevent repeats
    data.pop(i)

    # Fix characters with bad formatting
    formatting = [
                  ("#039;", "'"),
                  ("&'", "'"),
                  ("&quot;", '"'),
                  ("&lt;", "<"),
                  ("&gt;", ">")
                  ]

    # Replace bad characters in strings
    for tuple in formatting:
        question = question.replace(tuple[0], tuple[1])
        correct = correct.replace(tuple[0], tuple[1])
    # Replace bad characters in lists
    for tuple in formatting:
        wrong = [char.replace(tuple[0], tuple[1]) for char in wrong]

    # Add the new question & answers to the parameters for display
    q_and_a['question'] = question
    q_and_a['correct'] = correct

    all_answers = wrong + [correct]
    random.shuffle(all_answers)

    for idx, answer in enumerate(all_answers):
        q_and_a[f'answer{idx + 1}'] = answer

    frame2()


# Global data storage for state management
q_and_a = {  
          "question": '',
          "answer1": '',
          "answer2": '',
          "answer3": '',
          "answer4": '',
          "correct": '',
          }

parameters = {
              "score": [0],
              "index": [get_index()]
            }

widgets = {
          "logo": [],
          "start_button": [],
          "score": [],
          "question": [], 
          "answer1": [],
          "answer2": [],
          "answer3": [],
          "answer4": [],
          "win_msg": [],
          "fail_msg": [],
          "exit": [],
          "new_game_btn": []
        }


def start_game():
    clear_widgets()
    load_question_data(get_index())
    frame2()


def exit_game():
    clear_widgets()
    frame1()

def win_game():
    clear_widgets()
    winning_frame()

def lose_game():
    clear_widgets()
    losing_frame()


def clear_widgets():
    '''Move between frames'''
    print('clearing widgets')
    for widget in widgets:
        if widgets[widget] != []:
          widgets[widget][-1].hide()

        for i in range(0, len(widgets[widget])):
          widgets[widget].pop()


def create_buttons(answer):
    '''Generate the 4 matching answer options'''

    btn = QPushButton(answer)
    btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    btn.setFixedWidth(485)

    btn.setStyleSheet('*{border: 4px solid "#BC006C";' +
                    'color: white;' + 
                    'font-family: Shanti;' +
                    'font-size: 16px;' +
                    'border-radius: 25px;' +
                    'padding: 15px 0;' +
                    'margin: 10px 10px;}' +
                    '*:hover{background: "#BC006C"}'
                    )

    btn.clicked.connect(lambda x: is_correct(answer))

    return btn


def new_question():
    parameters['index'].pop()
    parameters['index'].append(get_index())
    load_question_data(parameters['index'][-1])

    widgets['score'][-1].setText(str(parameters['score'][-1]))
    widgets['question'][0].setText(q_and_a['question'])


def is_correct(answer):
    '''Check answer and increment score
        +10 for correct
        -5 for incorrect ''' 

    new_q = True

    print('Answer: ', answer)
    if str(answer) == q_and_a['correct']:
        print('CORRECT')
        temp_score = parameters['score'][-1]
        parameters['score'].pop()
        print(temp_score + 10)
        parameters['score'].append(temp_score + 10)
        
        if (parameters['score'][-1] + 10) >= 100:
            new_q = False
            win_game()

    else:
        print("WRONG")
        temp_score = parameters['score'][-1]
        parameters['score'].pop()
        print(temp_score - 5)
        parameters['score'].append(temp_score - 5)

        if (temp_score - 5) < 0:
            print('inside the loser')
            new_q = False
            lose_game()

    if new_q:
        new_question()


def frame1():
    '''Welcome screen for the game'''

    clear_widgets()
    parameters['score'][-1] = 0 

    # Display logo at top center
    image = QPixmap('./images/game_logo.png')
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignHCenter)
    logo.setStyleSheet('margin-top: 50px;')

    widgets['logo'].append(logo)

    # Play button widget
    btn = QPushButton('PLAY!')
    btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    btn.setStyleSheet('*{border: 4px solid "#BC006C";' +
                    'border-radius: 15px;' +
                    'font-size: 35px;' +
                    'color: white;' +
                    'margin: 100px 50px;' +
                    'padding: 25px 0;}' +
                    '*:hover{background: "#BC006C";}'
                    )
    btn.clicked.connect(start_game)

    widgets['start_button'].append(btn)

    # Add both elements to the grid layout;
    #   Take up 1 row, 2 columns of space
    grid.addWidget(widgets['logo'][-1], 0, 0, 1, 2)
    grid.addWidget(widgets['start_button'][-1], 1, 0, 1, 2)


def frame2():
    '''Displays Question, 4 answer options, and score'''

    clear_widgets()

    score = QLabel(str(parameters['score'][-1]))
    score.setAlignment(QtCore.Qt.AlignRight)
    score.setStyleSheet('font-size: 35px;' +
                      'color: white;' +
                      'padding: 10px 10px 10px 10px;' +
                      'margin: 20px 200px;' +
                      'background: "#64a314";' +
                      'border: 1px solid "#64a314";' +
                      'border-radius: 25px;'
                      )
    widgets['score'].append(score)

    question = QLabel(q_and_a['question'])
    question.setAlignment(QtCore.Qt.AlignCenter)
    question.setMinimumHeight(220)
    question.setWordWrap(True)
    question.setStyleSheet('font-family: Shanti;' +
                          'font-size: 25px;' +
                          'color: white;' +
                          'padding: 75px;'
                          )
    widgets['question'].append(question)

    button1 = create_buttons(q_and_a['answer1'])
    button2 = create_buttons(q_and_a['answer2'])
    button3 = create_buttons(q_and_a['answer3'])
    button4 = create_buttons(q_and_a['answer4'])

    widgets['answer1'].append(button1)
    widgets['answer2'].append(button2)
    widgets['answer3'].append(button3)
    widgets['answer4'].append(button4)

    exit_btn = QPushButton('Quit Game')
    exit_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    exit_btn.setStyleSheet('*{font-size: 12px;' +
                        'color: white;' +
                        'margin: 25px 25px;' +
                        'padding: 5px;' +
                        'border: 1px solid "#BC006C";' +
                        'border-radius: 25px;}' +
                        '*:hover{background: "#BC006C";}'
                        )
    exit_btn.clicked.connect(exit_game)

    widgets['exit'].append(exit_btn)

    # Display bottom logo
    image = QPixmap('./images/logo_bottom.png')
    logo = QLabel()
    logo.setPixmap(image)
    logo.setAlignment(QtCore.Qt.AlignHCenter)
    logo.setStyleSheet('margin-top: 75px; margin-bottom: 30px;')
    widgets['logo'].append(logo)

    grid.addWidget(widgets['score'][-1], 0, 1)
    grid.addWidget(widgets['question'][-1], 1, 0, 1, 2) # Includes row and column span info
    grid.addWidget(widgets['answer1'][-1], 2, 0)
    grid.addWidget(widgets['answer2'][-1], 2, 1)
    grid.addWidget(widgets['answer3'][-1], 3, 0)
    grid.addWidget(widgets['answer4'][-1], 3, 1)
    grid.addWidget(widgets['logo'][-1], 4, 0, 1, 2)
    grid.addWidget(widgets['exit'][-1], 0, 0, 1, 1)


def winning_frame():
    '''Shown when score is 100
        or when out of Questions and score is greater than 80 '''

    clear_widgets()
    print('winner')

    win_message = QLabel("Congratulations! You won!\n Your score is:")
    win_message.setAlignment(QtCore.Qt.AlignRight)
    win_message.setStyleSheet('font-family: Shanti;' +
                               'font-size: 25px;' +
                               'color: white;' +
                               'margin: 100px 0px;'
                              )
    widgets["win_msg"].append(win_message)

    # Score widget
    score = QLabel("100")
    score.setStyleSheet('font-size: 100px;' +
                        'color: #8FC740;' +
                        'margin: 0 75px 0px 75px;'
                        )
    widgets["score"].append(score)

    # #go back to work widget
    # message2 = QLabel("OK. Now go back to WORK.")
    # message2.setAlignment(QtCore.Qt.AlignCenter)
    # message2.setStyleSheet(
    #     "font-family: 'Shanti'; font-size: 30px; color: 'white'; margin-top:0px; margin-bottom:75px;"
    #     )
    # widgets["message2"].append(message2)

    # Try Again button widget
    redo_btn = QPushButton('TRY AGAIN')
    redo_btn.setStyleSheet('*{padding: 25px 0px;' +
                        'background: "#BC006C";' +
                        'color: white;' +
                        'font-family: Arial;' +
                        'font-size: 35px;' +
                        'border-radius: 40px;' +
                        'margin: 10px 200px;}' +
                        '*:hover {background: "#ff1b9e";}'
                        )
    redo_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    redo_btn.clicked.connect(frame1)

    widgets["new_game_btn"].append(redo_btn)

    # Logo widget
    pixmap = QPixmap('logo_bottom.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet('padding: 10px;' + 
                        'margin-top: 75px;'
                        )
    widgets["logo"].append(logo)

    # Place widgets on the grid
    grid.addWidget(widgets["win_msg"][-1], 2, 0)
    grid.addWidget(widgets["score"][-1], 2, 1)
    #grid.addWidget(widgets["message2"][-1], 3, 0, 1, 2)
    grid.addWidget(widgets["new_game_btn"][-1], 3, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 4, 0, 2, 2)


def losing_frame():
    clear_widgets()
    print('loser')

    # Losing message
    message = QLabel("Sorry, you lost.\n Your score is:")
    message.setAlignment(QtCore.Qt.AlignRight)
    message.setStyleSheet('font-family: Shanti;' +
                          'font-size: 35px;' +
                          'color: white;' +
                          'margin: 75px 5px;' + 
                          'padding: 20px;'
                          )
    widgets["fail_msg"].append(message)

    # Score widget
    score = QLabel(str(parameters["score"][-1]))
    score.setStyleSheet('font-size: 100px;' + 
                        'color: white;' + 
                        'margin: 0 75px 0px 75px;'
                        )
    widgets["score"].append(score)

    # Try Again button widget
    redo_btn = QPushButton('TRY AGAIN')
    redo_btn.setStyleSheet('*{padding: 25px 0px;' +
                        'background: "#BC006C";' +
                        'color: white;' +
                        'font-family: Arial;' +
                        'font-size: 35px;' +
                        'border-radius: 40px;' +
                        'margin: 10px 200px;}' +
                        '*:hover {background: "#ff1b9e";}'
                        )
    redo_btn.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
    redo_btn.clicked.connect(frame1)

    widgets["new_game_btn"].append(redo_btn)

    # Logo widget
    pixmap = QPixmap('logo_bottom.png')
    logo = QLabel()
    logo.setPixmap(pixmap)
    logo.setAlignment(QtCore.Qt.AlignCenter)
    logo.setStyleSheet('padding: 10px;' + 
                        'margin-top: 75px;'
                        )
    widgets["logo"].append(logo)

    # Place widgets on the grid
    grid.addWidget(widgets["fail_msg"][-1], 1, 0)
    grid.addWidget(widgets["score"][-1], 1, 1)
    grid.addWidget(widgets["new_game_btn"][-1], 2, 0, 1, 2)
    grid.addWidget(widgets["logo"][-1], 3, 0, 1, 2)