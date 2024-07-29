from flask import Flask, render_template, request, session, redirect
from flask_session import Session
import datetime

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["GET", "POST"])
def index():

    now = datetime.datetime.now()
    num_days = 0
    current_year = now.year
    current_month = now.month
    month_name = now.strftime("%B")
    current_day = now.day

    event_year = current_year
    event_month = current_month
    event_day = current_day
    
    event_date_obj = ""
    

   

    if "events" not in session:
        session["events"] = {}
    
    
    if request.method == "POST":
        
        event = request.form.get("event")

        event_date = request.form['event_date']
        event_date_obj = datetime.datetime.strptime(event_date, '%Y-%m-%d')
        
        event_year = event_date_obj.year
        event_month = event_date_obj.month
        event_day = event_date_obj.day

        str_event_day = str(event_day)
        
        
        

        if str_event_day in session["events"]:
            session["events"][str_event_day].append(event)
        else:
            session["events"][str_event_day] = [event]
            
            
        


    is_leap_year = (now.year % 4 == 0 and now.year % 100 != 0) or (now.year % 400 == 0)

    if now.month == 1 or now.month == 3 or now.month == 5 or now.month == 7 or now.month == 8 or now.month == 10 or now.month == 12:
        num_days = 31 
    elif now.month == 2 and is_leap_year:
        num_days = 29
    elif now.month == 2 and not is_leap_year:
        num_days = 28
    else:
        num_days = 30

    return render_template("index.html", events=session["events"], num_days=num_days, year=current_year, month=current_month, current_day=current_day, event_year=event_year, event_month=event_month, event_day=event_day, month_name=month_name, event_date_obj=event_date_obj)


@app.route("/clear", methods=["GET"])
def clear():
    session["events"] = {}
    return redirect("/")

