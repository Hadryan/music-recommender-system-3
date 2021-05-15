from flask import request, jsonify, url_for
import requests
from app.api import bp
from app.api.errors import bad_request

def basic_get(id):
    url = 'https://music.163.com/api/playlist/detail?id=' + str(id)
    data = requests.get(url)
    data.encoding = 'utf-8'
    return data.text

@bp.route('/music/rising', methods=['GET'])
def get_rising_music():
    data = basic_get(19723756)
    return data

@bp.route('/music/newSong', methods=['GET'])
def get_new_music():
    data = basic_get(3779629)
    return data

@bp.route('/music/popular', methods=['GET'])
def get_popular_music():
    data = basic_get(3778678)
    return data

@bp.route('/music/search', methods=['POST'])
def get_search():
    data = request.get_json()
    if not data:
        return bad_request('You must post JSON data')
    message = {}
    if 'type' not in data or not data.get('type', None):
        message['type'] = 'Please provide type'
    if 's' not in data or not data.get('s', None):
        message['s'] = 'Please provide search string'
    if message:
        return bad_request(message)

    s = data.get('s')
    type = data.get('type')
    url = 'http://music.163.com/api/search/get/web?csrf_token=hlpretag=&hlposttag=&s=' + s +'&type=' + type +'&offset=0&total=true&limit=20'
    data = requests.get(url)
    data.encoding = 'utf-8'
    return data.text

@bp.route('/music/getSinger/<string:singer>', methods=['GET'])
def get_singer(singer):
    url = 'http://127.0.0.1:7001/getSinger?singer=' + singer
    data = requests.get(url)
    data.encoding = 'utf-8'

    res_data = data.json()

    return res_data.get('data')

