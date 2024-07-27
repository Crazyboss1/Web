from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)

DATABASE_URI = "mongodb+srv://SpidySeries:SpidySeries@cluster0.xreosjj.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(DATABASE_URI)
db = client['series_database']
series_collection = db['series']

@app.route('/add_edit_series/<series_key>', methods=['GET', 'POST'])
def add_edit_series(series_key=None):
    if request.method == 'POST':
        series_data = {
            'title': request.form['title'],
            'released_on': request.form.get('released_on', "N/A"),
            'genre': request.form.get('genre', "N/A"),
            'rating': request.form.get('rating', "N/A"),
            'languages': [lang.strip() for lang in request.form.get('languages', "").split(",")],
            'seasons': {}
        }

        # Add or update series data
        series_collection.update_one(
            {'key': series_key},
            {'$set': series_data},
            upsert=True
        )
        return redirect(url_for('view_series', series_name=series_data['title']))

    else:
        # Fetch existing series data for editing
        series = series_collection.find_one({'key': series_key}) if series_key else {}
        return render_template('add_edit_series.html', series=series)

@app.route('/add_season/<series_key>', methods=['POST'])
def add_season(series_key):
    season_name = request.form['season_name']
    language = request.form['language'].lower().replace(' ', '')
    links_str = request.form.get('links', "")
    links = dict(link.split('=') for link in links_str.split(","))

    season_key = f"{series_key}-{language}-{season_name.lower().replace(' ', '')}"

    series_collection.update_one(
        {"key": series_key},
        {"$set": {f"seasons.{season_name}": {"links": links}}},
        upsert=True
    )

    return redirect(url_for('view_series', series_name=series_key))

@app.route('/view_series/<series_name>')
def view_series(series_name):
    series = series_collection.find_one({"title": series_name})
    return render_template('view_series.html', series=series)

if __name__ == '__main__':
    app.run(debug=True)
