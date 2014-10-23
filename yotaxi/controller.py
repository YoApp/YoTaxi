from yotaxi import app
from flask import request, render_template
from API_KEY import api_token
import requests

YO_API = "https://api.justyo.co/yo/"


def get_stand_ref(lat, lon):
    """Get taxi stand's reference within 20 miles"""
    url_places = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={0},{1}&radius=20000&types=%7Ctaxi_stand&sensor=false&key=AIzaSyCej3iRHphjKOGUxNq0j2bk129bym0sAHY".format(
        lat, lon)
    r = requests.get(url_places)
    try:
        for i in r.json()['results']:
            stand_open = i['opening_hours']['open_now']
            if stand_open:
                return i['reference']
                break
    except KeyError:
        return r.json()['results'][0]['reference']


def get_phone_number(ref):
    """Get a taxi stands number from reference"""
    url_num = "https://maps.googleapis.com/maps/api/place/details/json?key=AIzaSyCej3iRHphjKOGUxNq0j2bk129bym0sAHY&sensor=false&reference={0}".format(
        ref)
    r = requests.get(url_num)
    try:
        return r.json()['result']['formatted_phone_number']
    except KeyError:
        return None


def get_stand_name(ref):
    """Get stands name"""
    url_num = "https://maps.googleapis.com/maps/api/place/details/json?key=AIzaSyCej3iRHphjKOGUxNq0j2bk129bym0sAHY&sensor=false&reference={0}".format(
        ref)
    r = requests.get(url_num)
    try:
        return r.json()['result']['name']
    except KeyError:
        return None


def send_yo(username, link):
    """Yo a username"""
    requests.post(
        YO_API,
        data={'api_token': api_token, 'username': username, 'link': link})


@app.route('/')
def main():
    """Index Controller"""
    return render_template('index.html')


@app.errorhandler(404)
def handle_error(e):
    return render_template('404.html')


@app.route('/noresult')
def noresult():
    return render_template('noresult.html')


@app.route('/response')
def response():
    taxi_number = request.args.get('msg')
    stand_name = request.args.get('name')
    return render_template('response.html',
                           phone_number=taxi_number,
                           stand_name=stand_name)


@app.route('/yo')
def yo():
    """Handle callback request"""
    username = request.args.get('username')
    location = request.args.get('location')
    splitted = location.split(';')
    latitude = splitted[0]
    longitude = splitted[1]
    stand_ref = get_stand_ref(latitude, longitude)
    stand_name = get_stand_name(stand_ref)
    num = get_phone_number(stand_ref)
    if num is None:
        send_yo(username, 'http://yo-taxi.herokuapp.com/noresult')
    else:
        link = "http://yo-taxi.herokuapp.com/response?msg={0}&name={1}".format(
            num, stand_name)
        send_yo(username, link)
    return 'OK'
