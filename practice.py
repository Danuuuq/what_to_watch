from random import randint

from flask import Flask, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SECRET_KEY'] = 'AIJUIsb6a%^$d43cv'
db = SQLAlchemy(app)


class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, nullable=False)


class StoryForm(FlaskForm):
    # Опишите поля формы:
    title = StringField(
        'Укажите название истории',
        validators=[DataRequired(message='Обязательное поле'),
                    Length(1, 128)]
    )
    text = TextAreaField(
        'Напишите текст истории',
        validators=[DataRequired()]
    )
    submit = SubmitField('Опубликовать')


@app.route('/')
def index_view():
    stories = Story.query.all()
    return render_template('stories.html', stories=stories)


@app.route('/add', methods=['GET', 'POST'])
def add_view():
    form = StoryForm()
    if form.validate_on_submit():
        story = Story(
            title=form.title.data,
            text=form.text.data
        )
        db.session.add(story)
        db.session.commit()
        return redirect(url_for('index_view'))
    return render_template('add.html', form=form)


@app.route('/story')
def random_story_view():
    stories_count = Story.query.count()
    random_story = Story.query.get_or_404(
        randint(1, stories_count)
    )
    return render_template('random.html', story=random_story)