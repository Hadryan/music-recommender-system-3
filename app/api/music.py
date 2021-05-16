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

@bp.route('/music/getSinger/<string:singer>', methods=['GET'])
def get_singer(singer):
    url = 'http://127.0.0.1:7001/getSinger?singer=' + singer
    data = requests.get(url)
    data.encoding = 'utf-8'

    res_data = data.json()

    return res_data.get('data')

@bp.route('/music/getSong/<int:id>', methods=['GET'])
def get_song(id):
    url = 'http://127.0.0.1:7001/getSong?id=' + str(id)
    data = requests.get(url)
    data.encoding = 'utf-8'
    res_data = data.json()
    return res_data.get('data')

@bp.route('music/search/<string:s>', methods=['GET'])
def get_search(s):
    url = 'http://127.0.0.1:7001/search?s=' + s
    data = requests.get(url)
    data.encoding = 'utf-8'
    res_data = data.json()
    return res_data.get('data')
