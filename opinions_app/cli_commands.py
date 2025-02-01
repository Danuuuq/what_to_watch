import csv

import click

from .models import Opinion
from . import db, app


@app.cli.command('load_opinions')
def load_opinion_command():
    """Функция загрузки мнений в базу данных."""
    with open('opinions.csv', encoding='UTF-8') as f:
        reader = csv.DictReader(f)
        counter = 0
        for row in reader:
            opinion = Opinion(**row)
            db.session.add(opinion)
            db.session.commit()
            counter += 1
    click.echo(f'Загружено мнений: {counter}')
