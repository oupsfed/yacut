import random
import string

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import URLMapForm
from .models import URLMap


def get_unique_short_id():
    text = f'{string.ascii_letters}0123456789'
    char_number = 6
    short = ''.join(random.choice(text) for x in range(char_number))
    if URLMap.query.filter_by(short=short).first():
        return get_unique_short_id()
    return short


@app.route('/', methods=['GET', 'POST'])
def index_view():
    maps = URLMap.query.all()
    print(*maps)
    form = URLMapForm()
    if form.validate_on_submit():
        short = form.custom_id.data
        if URLMap.query.filter_by(short=short).first():
            flash(f'Имя {short} уже занято!')
            return render_template('index.html', form=form)
        if not short:
            short = get_unique_short_id()
        urlmap = URLMap(
            original=form.original_link.data,
            short=short,
        )
        db.session.add(urlmap)
        db.session.commit()
        flash('Ваша новая ссылка готова:')
        flash(url_for('url_map_view', short=short, _external=True,), category='url')
        return render_template('index.html', form=form)

    return render_template('index.html', form=form)


@app.route('/<short>')
def url_map_view(short):
    url_map = URLMap.query.filter_by(short=short).first()
    if url_map is None:
        abort(404)
    return redirect(url_map.original)
