from flask import Flask, render_template, request, redirect, url_for
import os
import json
import random

app = Flask(__name__)
database = {}
with open('foodlog.json') as fp:
    database = json.load(fp)


@app.route('/')
def home():
    return render_template('home.template.html')


@app.route('/', methods=['POST'])
def process_form():
    date = request.form.get('date')
    food_name = request.form.get('food_name')
    calories = request.form.get('calories')
    meal = request.form.get('meal')

    new_food = {
        "id": random.randint(1000, 9999),
        "date": date,
        "food_name": food_name,
        "calories": calories,
        "meal": meal
    }

    database.append(new_food)

    with open('foodlog.json', 'w') as fp:
        json.dump(database, fp)

    return redirect(url_for('show_records'))


@app.route('/records')
def show_records():
    return render_template('records.template.html', all_records=database)


@app.route('/records/<int:food_id>/edit')
def show_edit_records(food_id):
    record_to_edit = None
    for each_food in database:
        if each_food["id"] == food_id:
            record_to_edit = each_food
            break
    if record_to_edit:
        return render_template('edit_record.template.html',
                               record=record_to_edit)
    else:
        return f"The record of id {food_id} is NOT found!"


@app.route('/records/<int:food_id>/edit', methods=["POST"])
def process_edit_records(food_id):
    record_to_edit = None
    for each_food in database:
        if each_food["id"] == food_id:
            record_to_edit = each_food
            break
    if record_to_edit:
        record_to_edit["date"] = request.form.get("date")
        record_to_edit["food_name"] = request.form.get("food_name")
        record_to_edit["calories"] = request.form.get("calories")
        record_to_edit["meal"] = request.form.get("meal")

        with open('foodlog.json', 'w') as fp:
            json.dump(database, fp)
        return redirect(url_for("show_records"))

    else:
        return f"The record of id {food_id} is NOT found!"


# "magic code" -- boilerplate
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),  # or '0.0.0.0'
            port=int(os.environ.get('PORT')),  # or 8080
            debug=True)
