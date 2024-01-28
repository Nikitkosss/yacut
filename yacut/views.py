from random import choice
from string import ascii_lowercase, ascii_uppercase, digits

from flask import abort, flash, redirect, render_template

from yacut import app, db
from yacut.forms import URLMapForm
from yacut.models import URLMap


def get_unique_short_id():
    short = ''.join(
        choice(ascii_uppercase + ascii_lowercase + digits)
        for _ in range(6)
    )
    while URLMap.query.filter_by(short=short).first():
        short = ''.join(
            choice(ascii_uppercase + ascii_lowercase + digits)
            for _ in range(6)
        )
    return short


@app.route('/', methods=['GET', 'POST'])
def generate_short_id_view():
    form = URLMapForm()

    if form.validate_on_submit():
        short = form.custom_id.data
        original = form.original_link.data

        if not short:
            short = get_unique_short_id()
        elif URLMap.query.filter_by(short=short).first():
            flash('Предложенный вариант короткой ссылки уже существует.')
            return render_template('index.html', form=form)

        url_map = URLMap(
            original=original,
            short=short
        )

        db.session.add(url_map)
        db.session.commit()

        context = {'url_map': url_map, 'form': form}
        return render_template('index.html', **context)

    return render_template('index.html', form=form)


@app.route('/<string:short>')
def short_id_view(short):
    url_map = URLMap.query.filter_by(short=short).first()

    if url_map:
        return redirect(url_map.original)
    else:
        abort(404)
