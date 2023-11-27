from flask import Flask
from flask import render_template
from flask import request
from flask import session
from flask import abort, redirect, url_for
import csv
import random

app = Flask(__name__)
app.secret_key = b'foobar'
app.debug=True

birds = []
NUM_ANSWERS=3
NUM_ROUNDS=4

# todo: keep list of used birds
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

@app.route("/quiz_results")
def quiz_results():
    p={}
    p['results']=session['results']
    session['results']=[]
    p['page_title']='Vogel-Quiz Antworten!'
    return render_template("quiz_results.html", p=p)

@app.route("/quiz/<answer>")
@app.route("/quiz")
def quiz(answer=None):
    p={}

    if 'question_number' in session:
        session['question_number'] += 1
    else:
        session['question_number']=1
        session['correct_count]'] = 0
        session['results]'] = {} 

    if 'bird' in session:
        # check session['bird']=p['bird']['name']
        if session['bird']==answer:
            p['last_correct']=f"Die letzte Antwort: Richtig! Es war ein {session['bird']} "
        else:
            p['last_correct']=f"Die letzte Antwort: Schade, es war ein {session['bird']}, kein {answer}"

        rslt={'bird':session['bird'], 'img':session['img'], 'answer':answer}
        session['results'].append(rslt)
    else:
        session['results']=[]

    #if 'show_answer' in session:
        #if session['show_answer']==False:
            #session['show_answer']=True
            #p['show_answer']=True
            #return render_template("quiz.html", p=p)
        #else:
            #session['show_answer']=False
    #else:
        #session['show_answer']=False

    # are we done?
    if session['question_number'] > NUM_ROUNDS:
        #session['question_number']=1
        #session['last_correct']=''
        #session['bird]'] = ''
        p['results']=session['results']
        p['page_title']='Vogel-Quiz Antworten!'
        #session['results]'] = [] 
        session.clear()
        return render_template("quiz_results.html", p=p)


    if not answer:
        answer=''
    p['last_answer'] = answer
    p['question_number']=session['question_number']
    p['birds']=birds
    p['quizlst']=quizlst
    #p['birds']=read_birds()
    #p['quizlst']=read_quiz()
    used=[]
    (p['bird'], used)=pick_question_bird(p['quizlst'],used)
    session['bird']=p['bird']['name']
    session['img']=p['bird']['img']
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
    p['birds']=birds
    p['birds'].sort()

    p['page_title']='List of possible birbs'
    return render_template("bird_list.html", p=p)

@app.route("/")
def home():
    p={}
    p['page_title']='Home page!'
    return render_template("home.html", p=p)

birds=read_birds()
quizlst=read_quiz()