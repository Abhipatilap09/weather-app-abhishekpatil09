from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class WeatherRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100))
    date = db.Column(db.String(50))
    temp = db.Column(db.Float)
    description = db.Column(db.String(100))
    icon = db.Column(db.String(10))

# Map weather conditions to CSS classes
def get_weather_class(weather_main):
    mapping = {
        'Clear': 'sunny',
        'Clouds': 'cloudy',
        'Rain': 'rainy',
        'Drizzle': 'rainy',
        'Thunderstorm': 'rainy',
        'Snow': 'snowy',
        'Mist': 'cloudy',
        'Fog': 'cloudy'
    }
    return mapping.get(weather_main, 'sunny')

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    forecast = None
    weather_class = ''
    records = WeatherRecord.query.all()
    api_key = '6d50389e627d2567d21e8820a19f91f1'  

    if request.method == 'POST':
        location = request.form['location']
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        try:
            # Current weather
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&units=metric&appid={api_key}"
            res = requests.get(url).json()
            if res.get('cod') != 200:
                weather = {'error': res.get('message', 'Error fetching weather')}
            else:
                weather = res
                weather_class = get_weather_class(weather['weather'][0]['main'])

                # Forecast
                f_url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&units=metric&appid={api_key}"
                f_res = requests.get(f_url).json()
                if f_res.get('cod') == "200":
                    # Filter by date range
                    forecast = []
                    for item in f_res['list']:
                        forecast_date = item['dt_txt'].split()[0]
                        if (not start_date or forecast_date >= start_date) and (not end_date or forecast_date <= end_date):
                            forecast.append(item)
                    forecast = forecast[:5]  # limit to 5 entries

                # Save to DB
                record = WeatherRecord(
                    location=weather['name'],
                    date=datetime.now().strftime('%Y-%m-%d %H:%M'),
                    temp=weather['main']['temp'],
                    description=weather['weather'][0]['description'],
                    icon=weather['weather'][0]['icon']
                )
                db.session.add(record)
                db.session.commit()
        except Exception as e:
            weather = {'error': str(e)}

    return render_template('index.html', weather=weather, forecast=forecast, records=records, weather_class=weather_class)

@app.route('/current')
def current_location():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    weather = None
    forecast = None
    weather_class = ''
    records = WeatherRecord.query.all()
    api_key = '6d50389e627d2567d21e8820a19f91f1'  
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
        res = requests.get(url).json()
        if res.get('cod') != 200:
            weather = {'error': res.get('message', 'Error fetching weather')}
        else:
            weather = res
            weather_class = get_weather_class(weather['weather'][0]['main'])

            f_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&units=metric&appid={api_key}"
            f_res = requests.get(f_url).json()
            if f_res.get('cod') == "200":
                forecast = f_res['list'][:5]

            record = WeatherRecord(
                location=weather['name'],
                date=datetime.now().strftime('%Y-%m-%d %H:%M'),
                temp=weather['main']['temp'],
                description=weather['weather'][0]['description'],
                icon=weather['weather'][0]['icon']
            )
            db.session.add(record)
            db.session.commit()
    except Exception as e:
        weather = {'error': str(e)}

    return render_template('index.html', weather=weather, forecast=forecast, records=records, weather_class=weather_class)

# CRUD Routes
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    record = WeatherRecord.query.get_or_404(id)
    record.temp = request.form['temp']
    record.description = request.form['description']
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    record = WeatherRecord.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return redirect(url_for('index'))

# Export Routes
@app.route('/export/json')
def export_json():
    records = WeatherRecord.query.all()
    data = []
    for r in records:
        data.append({
            'location': r.location,
            'date': r.date,
            'temp': r.temp,
            'description': r.description,
            'icon': r.icon
        })
    return jsonify(data)

@app.route('/export/csv')
def export_csv():
    records = WeatherRecord.query.all()
    filename = "weather_export.csv"
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Location','Date','Temperature','Description','Icon'])
        for r in records:
            writer.writerow([r.location, r.date, r.temp, r.description, r.icon])
    return f"CSV exported as {filename}"

# Run server
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
