from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_mail import Mail, Message
from datetime import datetime, timedelta
from dateutil import rrule
from models import Event, JSONEncoder
from config import Config
from bson import ObjectId
import json
import os
from analytics import TimeAnalytics, ChartGenerator
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

app = Flask(__name__)
app.config.from_object(Config)
app.json_encoder = JSONEncoder

# Initialize MongoDB
from flask_pymongo import PyMongo
mongo = PyMongo(app)

# Initialize Flask-Mail
mail = Mail(app)

# Make timedelta available in templates
@app.context_processor
def utility_processor():
    return dict(timedelta=timedelta, datetime=datetime)

# Routes
@app.route('/')
def index():
    # Get upcoming events for the home page
    now = datetime.now()
    future_events = list(mongo.db.events.find({
        'start_time': {'$gte': now},
        'user_id': 'current_user'  # In a real app, you'd use session/user auth
    }).sort('start_time', 1).limit(5))
    
    # Convert to Event objects
    events = [Event.from_dict(event) for event in future_events]
    
    return render_template('index.html', events=events)

@app.route('/daily')
def daily_view():
    date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    selected_date = datetime.strptime(date_str, '%Y-%m-%d')
    
    start_of_day = datetime.combine(selected_date, datetime.min.time())
    end_of_day = datetime.combine(selected_date, datetime.max.time())
    
    events = list(mongo.db.events.find({
        'start_time': {'$gte': start_of_day, '$lte': end_of_day},
        'user_id': 'current_user'
    }).sort('start_time', 1))
    
    events = [Event.from_dict(event) for event in events]
    return render_template('daily.html', events=events, selected_date=selected_date)

@app.route('/weekly')
def weekly_view():
    date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    selected_date = datetime.strptime(date_str, '%Y-%m-%d')
    
    start_of_week = selected_date - timedelta(days=selected_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    events = list(mongo.db.events.find({
        'start_time': {'$gte': start_of_week, '$lte': end_of_week},
        'user_id': 'current_user'
    }).sort('start_time', 1))
    
    events = [Event.from_dict(event) for event in events]
    
    # Group events by day
    days = []
    for i in range(7):
        day = start_of_week + timedelta(days=i)
        day_events = [e for e in events if e.start_time.date() == day.date()]
        days.append((day, day_events))
    
    return render_template('weekly.html', days=days, selected_date=selected_date)

@app.route('/monthly')
def monthly_view():
    date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    selected_date = datetime.strptime(date_str, '%Y-%m-%d')
    
    year, month = selected_date.year, selected_date.month
    start_of_month = datetime(year, month, 1)
    
    if month == 12:
        end_of_month = datetime(year+1, 1, 1) - timedelta(days=1)
    else:
        end_of_month = datetime(year, month+1, 1) - timedelta(days=1)
    
    events = list(mongo.db.events.find({
        'start_time': {'$gte': start_of_month, '$lte': end_of_month},
        'user_id': 'current_user'
    }).sort('start_time', 1))
    
    events = [Event.from_dict(event) for event in events]
    
    # Create calendar grid
    first_weekday = start_of_month.weekday()
    days_in_month = (end_of_month - start_of_month).days + 1
    
    calendar = []
    week = [None] * first_weekday
    
    for day in range(1, days_in_month + 1):
        current_date = datetime(year, month, day)
        day_events = [e for e in events if e.start_time.date() == current_date.date()]
        week.append((current_date, day_events))
        
        if len(week) == 7:
            calendar.append(week)
            week = []
    
    if week:
        week.extend([None] * (7 - len(week)))
        calendar.append(week)
    
    return render_template('monthly.html', calendar=calendar, selected_date=selected_date)

@app.route('/yearly')
def yearly_view():
    date_str = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    selected_date = datetime.strptime(date_str, '%Y-%m-%d')
    year = selected_date.year
    
    events = list(mongo.db.events.find({
        'start_time': {'$gte': datetime(year, 1, 1), '$lte': datetime(year, 12, 31, 23, 59, 59)},
        'user_id': 'current_user'
    }).sort('start_time', 1))
    
    events = [Event.from_dict(event) for event in events]
    
    # Group events by month
    months = []
    for month in range(1, 13):
        month_events = [e for e in events if e.start_time.month == month]
        months.append((month, month_events))
    
    return render_template('yearly.html', months=months, year=year, selected_date=selected_date)

@app.route('/event/new', methods=['GET', 'POST'])
def new_event():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        start_time = datetime.fromisoformat(request.form.get('start_time'))
        end_time = datetime.fromisoformat(request.form.get('end_time'))
        event_type = request.form.get('event_type')
        repeat = request.form.get('repeat')
        
        event = Event(title, description, start_time, end_time, event_type, repeat, 'current_user')
        mongo.db.events.insert_one(event.to_dict())
        
        # Send email notification if enabled
        if request.form.get('send_email') == 'on':
            send_event_notification(event, 'created')
        
        return redirect(url_for('index'))
    
    return render_template('event_form.html', event=None)

@app.route('/event/<event_id>/edit', methods=['GET', 'POST'])
def edit_event(event_id):
    event_data = mongo.db.events.find_one({'_id': ObjectId(event_id)})
    if not event_data:
        return "Event not found", 404
    
    event = Event.from_dict(event_data)
    
    if request.method == 'POST':
        event.title = request.form.get('title')
        event.description = request.form.get('description')
        event.start_time = datetime.fromisoformat(request.form.get('start_time'))
        event.end_time = datetime.fromisoformat(request.form.get('end_time'))
        event.event_type = request.form.get('event_type')
        event.repeat = request.form.get('repeat')
        
        mongo.db.events.update_one({'_id': ObjectId(event_id)}, {'$set': event.to_dict()})
        
        # Send email notification if enabled
        if request.form.get('send_email') == 'on':
            send_event_notification(event, 'updated')
        
        return redirect(url_for('index'))
    
    return render_template('event_form.html', event=event)

@app.route('/event/<event_id>/delete', methods=['POST'])
def delete_event(event_id):
    event_data = mongo.db.events.find_one({'_id': ObjectId(event_id)})
    if event_data:
        event = Event.from_dict(event_data)
        mongo.db.events.delete_one({'_id': ObjectId(event_id)})
        
        # Send email notification if enabled
        if request.form.get('send_email') == 'on':
            send_event_notification(event, 'deleted')
    
    return redirect(url_for('index'))

@app.route('/email-settings', methods=['GET', 'POST'])
def email_settings():
    if request.method == 'POST':
        # Save email settings (in a real app, you'd store these in database)
        app.config['MAIL_SERVER'] = request.form.get('mail_server')
        app.config['MAIL_PORT'] = int(request.form.get('mail_port'))
        app.config['MAIL_USE_TLS'] = request.form.get('mail_use_tls') == 'true'
        app.config['MAIL_USERNAME'] = request.form.get('mail_username')
        app.config['MAIL_PASSWORD'] = request.form.get('mail_password')
        app.config['MAIL_DEFAULT_SENDER'] = request.form.get('mail_default_sender')
        
        return redirect(url_for('index'))
    
    # Pass the current email configuration to the template
    email_config = {
        'MAIL_SERVER': app.config.get('MAIL_SERVER', ''),
        'MAIL_PORT': app.config.get('MAIL_PORT', ''),
        'MAIL_USE_TLS': app.config.get('MAIL_USE_TLS', ''),
        'MAIL_USERNAME': app.config.get('MAIL_USERNAME', ''),
        'MAIL_PASSWORD': app.config.get('MAIL_PASSWORD', ''),
        'MAIL_DEFAULT_SENDER': app.config.get('MAIL_DEFAULT_SENDER', '')
    }
    
    return render_template('email_settings.html', email_config=email_config)

@app.route('/analytics/dashboard')
def analytics_dashboard():
    time_analytics = TimeAnalytics(mongo)
    chart_gen = ChartGenerator()
    
    user_id = 'current_user'  # In real app, use session/user auth
    
    # Get analytics data
    time_distribution = time_analytics.get_time_distribution(user_id)
    productivity_trends = time_analytics.get_productivity_trends(user_id)
    peak_hours = time_analytics.get_peak_hours(user_id)
    category_efficiency = time_analytics.get_category_efficiency(user_id)
    
    # Generate charts
    distribution_chart = chart_gen.create_time_distribution_chart(time_distribution)
    trends_chart = chart_gen.create_productivity_trend_chart(productivity_trends)
    peak_hours_chart = chart_gen.create_peak_hours_chart(peak_hours)
    
    return render_template('analytics/dashboard.html',
                         time_distribution=time_distribution,
                         productivity_trends=productivity_trends,
                         peak_hours=peak_hours,
                         category_efficiency=category_efficiency,
                         distribution_chart=distribution_chart,
                         trends_chart=trends_chart,
                         peak_hours_chart=peak_hours_chart)

@app.route('/analytics/time-distribution')
def time_distribution():
    time_analytics = TimeAnalytics(mongo)
    user_id = 'current_user'
    
    time_distribution = time_analytics.get_time_distribution(user_id)
    chart_data = ChartGenerator.create_time_distribution_chart(time_distribution)
    
    return render_template('analytics/time_distribution.html',
                         time_distribution=time_distribution,
                         chart_data=chart_data)

@app.route('/analytics/productivity-trends')
def productivity_trends():
    time_analytics = TimeAnalytics(mongo)
    user_id = 'current_user'
    
    trends = time_analytics.get_productivity_trends(user_id)
    chart_data = ChartGenerator.create_productivity_trend_chart(trends)
    
    return render_template('analytics/productivity_trends.html',
                         trends=trends,
                         chart_data=chart_data)

def send_event_notification(event, action):
    try:
        subject = f"Event {action.capitalize()}: {event.title}"
        
        # Generate a calendar image URL based on the event date
        event_month = event.start_time.strftime('%B')
        event_day = event.start_time.strftime('%d')
        calendar_image_url = f"https://via.placeholder.com/600x200/f3f4f6/6366f1?text={event_month}+{event_day}+Calendar"
        
        # Create HTML email content
        html_body = render_template(
            'email_template.html', 
            event=event, 
            action=action,
            app_name="TimeFlow Scheduler",
            timetable_image=calendar_image_url
        )
        
        msg = Message(
            subject=subject,
            recipients=[app.config['MAIL_DEFAULT_SENDER']],
            html=html_body
        )
        
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False

if __name__ == '__main__':
    app.run(debug=True)