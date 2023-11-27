from flask import Flask
from flask import render_template
from flask import request
import csv
import random

# Todo:
# - 04_Wiedehopf.jpg aspect ratio


app = Flask(__name__)

birds = []
NUM_ANSWERS=3
NUM_ROUNDS=4

# Store bird questions in page, and guess number

def read_birds():
    with open('birds_all.csv',newline='', encoding="UTF8") as lst:
        return [b.strip() for b in lst.readlines()]

def read_quiz():
    quizlst=[]
    with open('birds_quiz.csv',newline='', encoding="UTF8") as birds:
        reader=csv.reader(birds)
        for row in reader:
            #print(f"""row[0]\trow[1]\trow[2]\trow[3] """)
            b={'num':row[0],'name':row[1],'url':row[2],'img':row[3]}
            quizlst.append(b)
    return quizlst

def pick_question_bird(quizlst,used):
    bird_num=-1
    while bird_num not in used:
        bird_num = random.randint(0, len(quizlst)-1)
        #print(f'new bird_num {bird_num}')
        #print(f'used: {used}')
        used.append(bird_num)
    return (quizlst[bird_num], used)

@app.route("/quiz")
def quiz():
    p={}
    p['birds']=birds
    p['quizlst']=quizlst
    #p['birds']=read_birds()
    #p['quizlst']=read_quiz()
    used=[]
    (p['bird'], used)=pick_question_bird(p['quizlst'],used)
    p['qcnt']=1
    p['q']=p['bird']['num']
    p['answers']=[]
    p['answers'].append(p['bird']['name'])
    while len(p['answers'])<NUM_ANSWERS:
        a_num = random.randint(0, len(p['birds'])-1)
        answer_name = p['birds'][a_num]
        if answer_name not in p['answers'] and answer_name != p['bird']['name']:
            p['answers'].append(p['birds'][a_num])
    random.shuffle(p['answers'])

    p['page_title']='Vogel-Quiz!'
    return render_template("quiz.html", p=p)

@app.route("/bird_list")
def bird_list():
    p={}
    p['birds']=read_birds_all()
    p['page_title']='List of birds'
    return render_template("bird_list.html", p=p)

@app.route("/")
def home():
    p={}
    p['page_title']='Home page!'
    return render_template("home.html", p=p)

birds=read_birds()
quizlst=read_quiz()