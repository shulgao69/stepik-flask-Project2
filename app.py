from flask import Flask, render_template, redirect, url_for
import json
from flask_wtf import FlaskForm
from wtforms import StringField,  RadioField
from wtforms.validators import InputRequired


app = Flask(__name__)
app.secret_key = "randomstring"


with open("days.json", "r", encoding="utf-8") as fff:
   days = fff.read()
   days = json.loads(days)


with open("goals.json", "r", encoding="utf-8") as f:
   goals = f.read()
   goals = json.loads(goals)


with open("teachers.json", "r", encoding="utf-8") as ff:
   teach = ff.read()
   teachers = json.loads(teach)


class UserForm(FlaskForm):
    name = StringField('Вас зовут', [InputRequired()])
    phone = StringField('Ваш телефон', [InputRequired()])
    clientWeekday = StringField()
    clientTime = StringField()
    clientTeacher = StringField()


class MyRequest(FlaskForm):
    goal_request = RadioField ("Какая цель занятий?", choices = goals.items())
    time_request = RadioField("Сколько времени есть?", choices = [("1-2 часа в неделю", "1-2 часа в неделю"),("3-5 часов в неделю","3-5 часов в неделю"), ("5-7 часов в неделю","5-7 часов в неделю"), ("7-10 часов в неделю","7-10 часов в неделю")])
    name_request = StringField("Вас зовут", [InputRequired()])
    phone_request = StringField("Ваш телефон", [InputRequired()])


@app.route('/')
def render_index():
    return render_template("index.html",
                           teachers = teachers,
                           goals = goals
                           )


@app.route('/goals/<goal>/')
def render_goal(goal):
    teach = []
    if goal not in goals:
        teach = teachers
    else:
        for teacher in teachers:
            for yuorgoals in teacher["goals"]:
                if yuorgoals == goal:
                    teach.append(teacher)

    return render_template("goal.html",
                           goal = goal,
                           teachers = teach,
                           goals = goals
                           )


@app.route('/profile/<int:id>/')
def render_profile(id):
    return render_template("profile.html",
                           teachers = teachers,
                           goals = goals,
                           id = id,
                           days = days
                           )


@app.route('/booking/<int:id>/<day>/<time>/')
def render_booking(id, day, time):
    form = UserForm()
    clientWeekday = day
    clientTime = time
    clientTeacher = id
    return render_template("booking.html",
                           teachers = teachers,
                           goals = goals,
                           days = days,
                           id = id,
                           day = day,
                           time = time,
                           clientWeekday = clientWeekday,
                           clientTime = clientTime,
                           clientTeacher = clientTeacher,
                           form = form
                           )


@app.route('/booking_done/', methods=['POST'])
def render_booking_done():
    form = UserForm()
    name = form.name.data
    phone = form.phone.data
    clientWeekday = form.clientWeekday.data
    clientTime = form.clientTime.data
    clientTeacher = form.clientTeacher.data

    teachers[int(clientTeacher)]["free"][clientWeekday][clientTime] = False
    with open("teachers.json", "w", encoding="utf-8") as f:
        json.dump(teachers, f, ensure_ascii=False)

    contents =str({"Имя педагога": teachers[int(clientTeacher)]["name"], "Имя ученика": name, "Телефон": phone, "День недели": clientWeekday, "Время": clientTime }) + ','
    with open("booking.json", "a", encoding="utf-8") as userform:
        userform.write(contents)

    return render_template("booking_done.html",
                           teachers = teachers,
                           goals = goals,
                           days = days,
                           clientWeekday = clientWeekday,
                           clientTime = clientTime,
                           clientTeacher = clientTeacher,
                           name = name,
                           phone = phone
                           )


@app.route('/request/')
def render_request():
    form = MyRequest()

    return render_template("request.html",
                           teachers = teachers,
                           goals = goals,
                           form = form
                           )


@app.route('/request_done/', methods=['POST'])
def render_request_done():
    form = MyRequest()
    goal_request = form.goal_request.data
    time_request = form.time_request.data
    name_request = form.name_request.data
    phone_request = form.phone_request.data
    time = {"1-2 часа в неделю", "3-5 часов в неделю", "5-7 часов в неделю", "7-10 часов в неделю"}

    if goal_request not in goals:
        return redirect((url_for('render_request')))
    elif time_request not in time:
        return redirect((url_for('render_request')))
    else:
        request_contents =str({"Цель занятий": goals[goal_request], "Времени есть": time_request, "Имя": name_request, "Телефон": phone_request }) + ', '
        with open("request.json", "a", encoding="utf-8") as requestform:
            requestform.write(request_contents)

    return render_template("request_done.html",
                           teachers = teachers,
                           goals = goals,
                           goal_request = goal_request,
                           time_request = time_request,
                           name_request = name_request,
                           phone_request = phone_request
                           )


if __name__ == '__main__':
    app.run()