from aiohttp import web
import aiohttp_jinja2
import jinja2
import pymongo


DATABASE_URI = "mongodb+srv://SpidySeries:SpidySeries@cluster0.xreosjj.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(DATABASE_URI)
db = client['series_database']
series_collection = db['series']
links_collection = db['series_links']

app = web.Application()
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

@aiohttp_jinja2.template('add_season.html')
async def add_season(request):
    if request.method == 'POST':
        data = request.post()
        series_key = data['series_key'].strip().lower().replace(' ', '')
        language = data['language'].strip().lower().replace(' ', '')
        season = data['season'].strip()
        quality = data['quality'].strip()
        link = data['link'].strip()

        season_key = f"{series_key}-{language}-{season.lower().replace(' ', '')}"

        # Adding the new season and link
        links = {quality: link}
        links_collection.update_one({"series_key": season_key}, {"$set": {"links": links}}, upsert=True)

        return web.HTTPFound('/add_season')
    return {}

@aiohttp_jinja2.template('add_quality.html')
async def add_quality(request):
    if request.method == 'POST':
        data = request.post()
        series_key = data['series_key'].strip().lower().replace(' ', '')
        language = data['language'].strip().lower().replace(' ', '')
        season = data['season'].strip().lower().replace(' ', '')
        quality = data['quality'].strip()
        link = data['link'].strip()

        season_key = f"{series_key}-{language}-{season}"
        links_collection.update_one({"series_key": season_key}, {"$set": {f"links.{quality}": link}}, upsert=True)

        return web.HTTPFound('/add_quality')
    return {}

app.router.add_get('/add_season', add_season)
app.router.add_post('/add_season', add_season)
app.router.add_get('/add_quality', add_quality)
app.router.add_post('/add_quality', add_quality)

if __name__ == '__main__':
    web.run_app(app, host='0.0.0.0', port=8000)
  
