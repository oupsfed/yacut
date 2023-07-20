import re

from flask import jsonify, request, url_for

from . import app, db
from .error_handlers import InvalidAPIUsage
from .models import URLMap
from .views import get_unique_short_id


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_urlmap(short_id):
    url_map = URLMap.query.filter_by(short=short_id).first()
    if url_map is None:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    return jsonify({'url': url_map.to_dict()['original']}), 200


@app.route('/api/id/', methods=['POST'])
def add_urlmap():
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса', 400)
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!', 400)
    if 'custom_id' not in data or data['custom_id'] in ['', None]:
        data['custom_id'] = get_unique_short_id()
    if URLMap.query.filter_by(short=data['custom_id']).first() is not None:
        raise InvalidAPIUsage(f'Имя "{data["custom_id"]}" уже занято.')
    if (len(data['custom_id']) > 16 or
            not re.search('^[a-zA-Z0-9]{2,16}$', data['custom_id'])):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    url_map = URLMap()
    data['original'] = data['url']
    data['short'] = data['custom_id']
    url_map.from_dict(data)
    db.session.add(url_map)
    db.session.commit()
    return jsonify({
        'url': url_map.to_dict()['original'],
        'short_link': url_for('url_map_view',
                              short=data['short'],
                              _external=True)

    }), 201
