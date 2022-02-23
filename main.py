import csv
from csv import writer

from forms import NameSearchForm, CpSearchForm, AddForm
from flask import Flask, render_template, jsonify, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)
# ---------------------------------------------------------------------------







# Rutas Flask
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = AddForm()
    return render_template('add.html', form=form)

@app.route('/cp_search')
def cp_search():
    form = CpSearchForm()
    return render_template('cp_search.html', form=form)


@app.route('/name_search')
def name_search():
    form = NameSearchForm()
    return render_template('name_search.html', form=form)


@app.route('/colonia_results')
def colonia_results():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        print(list_of_rows)
        print(list_of_rows[1:])
    return render_template('resultados.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
