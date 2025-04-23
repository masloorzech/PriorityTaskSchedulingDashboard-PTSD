import os

import requests
from flask import Blueprint, request, jsonify, Response
from bson import ObjectId, json_util
from flask_cors import CORS


API_KEY = os.environ.get('OPENWEATHER_API_KEY')

API_URL = 'http://api.openweathermap.org/data/2.5/weather'

weather_bp = Blueprint("weather", __name__)
CORS(weather_bp)

@weather_bp.route('/<city>', methods=['GET'])
def get_weather(city):
    if not API_KEY:
        return jsonify({'error': 'API key not set in environment'}), 500
    params = {
        'q': city,
        'appid': API_KEY,
        'units': 'metric'
    }
    response = requests.get(API_URL, params=params)
    data = response.json()
    if response.status_code != 200:
        return jsonify({'error': data.get('message', 'Unknown error')}), response.status_code
    weather = {
        'city': city,
        'temperature': data['main']['temp'],
        'humidity': data['main']['humidity'],
        'description': data['weather'][0]['description']
    }
    return jsonify(weather), 200

@weather_bp.route('/coords', methods=['GET'])
def get_weather_by_coords():
    if not API_KEY:
        return jsonify({'error': 'API key not set in environment'}), 500
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    if not lat or not lon:
        return jsonify({'error': 'Missing latitude or longitude'}), 400
    params = {
        'lat': lat,
        'lon': lon,
        'appid': API_KEY,
        'units': 'metric'
    }
    try:
        response = requests.get(API_URL, params=params, timeout=5)
        data = response.json()
    except requests.RequestException:
        return jsonify({'error': 'Weather service unreachable'}), 503
    if response.status_code != 200:
        return jsonify({'error': data.get('message', 'Unknown error')}), response.status_code
    weather = {
        'location': {
            'lat': lat,
            'lon': lon
        },
        'city': data.get('name', 'Unknown'),
        'temperature': data['main']['temp'],
        'humidity': data['main']['humidity'],
        'description': data['weather'][0]['description']
    }
    return jsonify(weather), 200
