# Weather App - AI Engineer Intern Technical Assessment

**Author:** Abhishek Patil  
**Role:** AI/ML/Gen AI Application Intern

This weather app allows users to get **current weather** and **5-day forecasts** for any location. Users can also store, update, delete, and export weather data. The app uses **OpenWeatherMap API**, **Flask**, and **SQLite**.

---

## **Features**

### 1. Current Weather & Forecast

- Enter a location (City, ZIP, or Postal Code) to get weather.
- Optional start and end dates for filtering forecasts.
- Dynamic **weather icons** and **backgrounds**.
- 5-day forecast displayed in cards with icons.

### 2. Geolocation

- Get weather for your current location with the "Use Current Location" button.

### 3. CRUD Operations

- **Create:** Save weather data in database automatically on search.
- **Read:** View previous weather searches.
- **Update:** Update temperature and description for any record.
- **Delete:** Delete any record from the database.

### 4. Export Data

- Export weather records to **JSON** or **CSV** formats.

### 5. Extra Features

- **Info button:** Links to [Product Manager Accelerator LinkedIn page](https://www.linkedin.com/company/product-manager-accelerator).
- **YouTube & Google Maps links** for each location.

---

## **Technologies Used**

- **Backend:** Python, Flask, Flask_SQLAlchemy
- **Frontend:** HTML, CSS, JavaScript
- **Database:** SQLite
- **API:** [OpenWeatherMap](https://openweathermap.org/api)

---

## **Setup Instructions**

1. Clone the repository:

```bash
# clone
git clone https://github.com/Abhipatilap09/weather-app-abhishekpatil09.git
cd weather-app-abhishekpatil09

# create venv (Linux/macOS)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# set env (example)
export OWM_API_KEY="your_openweathermap_key"
export FLASK_APP=app.py
flask run
# then open http://127.0.0.1:5000

```
