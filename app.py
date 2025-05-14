from flask import Flask, render_template, request, redirect, url_for, session
import json

app = Flask(__name__)
app.secret_key = 'supersecret'

# Load questions
with open('questions_cleaned.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

@app.route('/')
def index():
    return render_template('index.html', questions=questions)

@app.route('/question/<int:id>', methods=['GET', 'POST'])
def question(id):
    if 'answers' not in session:
        session['answers'] = {}

    if request.method == 'POST':
        answer = request.form.get('answer')
        if answer:
            session['answers'][str(id)] = int(answer)
        session.modified = True
        next_id = id + 1 if id < len(questions) else 'result'
        return redirect(url_for('question', id=next_id))

    return render_template('question.html', q=questions[id - 1], id=id)

@app.route('/result')
def result():
    score = 0
    for q in questions:
        user_ans = session.get('answers', {}).get(str(q['id']))
        if user_ans == q['correct_answer']:
            score += 1
    return render_template('result.html', score=score, total=len(questions))

if __name__ == '__main__':
    app.run(debug=True)
