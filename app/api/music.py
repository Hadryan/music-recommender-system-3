from flask import request, jsonify, url_for
import requests
from app.api import bp

def basic_get(id):
    url = 'https://music.163.com/api/playlist/detail?id=' + str(id)
    data = requests.get(url)
    data.encoding = 'utf-8'
    return data.text

@bp.route('/music/rising', methods=['GET'])
def get_rising_music():
    data = basic_get(3778678)
    return data

@bp.route('/music/newSong', methods=['GET'])
def get_new_music():
    data = basic_get(3779629)
    return data

@bp.route('/music/popular', methods=['GET'])
def get_popular_music():
    data = basic_get(3778678)
    return data