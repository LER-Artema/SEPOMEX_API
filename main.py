import csv
from csv import writer

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)

# Base de datos

class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), URL()])
    open = StringField('Open e.g. 8AM', validators=[DataRequired()])
    close = StringField('Close e.g. 8PM', validators=[DataRequired()])
    coffee = StringField('Coffee rating', default='☕️', validators=[DataRequired()])
    wifi = StringField('WiFi strengthens rating', default='💪', validators=[DataRequired()])
    power = StringField('Power strengthens rating', default='🔌', validators=[DataRequired()])

    submit = SubmitField('Submit')
# ---------------------------------------------------------------------------

# Rutas Flask
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        elements = [
            form.cafe.data,
            form.location.data,
            form.open.data,
            form.close.data,
            form.coffee.data,
            form.wifi.data,
            form.power.data,
        ]
        with open('cafe-data.csv', 'a', newline='') as csv_file:
            obj = writer(csv_file)
            obj.writerow(elements)
            csv_file.close()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        print(list_of_rows)
        print(list_of_rows[1:])
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
