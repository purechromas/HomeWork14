from flask import Flask, jsonify
from utils import get_one, get_all

app = Flask(__name__)


@app.get('/movie/<title>')
def get_title(title: str):
    query = f"""
    SELECT * FROM netflix
    WHERE title = '{title}'
    ORDER BY date_added 
    """

    query_result = get_one(query)

    if query_result is None:
        return jsonify(status=404)

    movie = {
        'title': query_result['title'],
        'country': query_result['country'],
        'release_year': query_result['release_year'],
        'genre': query_result['listed_in'],
        'description': query_result['description']
    }

    return jsonify(movie)


@app.get('/movie/<year1>/to/<year2>')
def year_to_year(year1, year2):
    query = f"""
    SELECT * FROM netflix
    WHERE release_year BETWEEN {year1} AND {year2}
    ORDER BY release_year DESC 
    LIMIT 100
    """

    result = []

    for item in get_all(query):
        result.append(
            {
                'title': item['title'],
                'release_year': item['release_year'],
            }
        )

    return jsonify(result)


@app.get('/movie/rating/<value>')
def rating(value: str):
    query = """
    SELECT * FROM netflix
    """

    if value.lower() == 'children':
        query += 'WHERE rating = "G" ORDER BY release_year DESC LIMIT 100'
    elif value.lower() == 'family':
        query += 'WHERE rating = "G" OR rating = "PG" OR rating = "PG-13" ORDER BY release_year DESC LIMIT 100'
    elif value.lower() == 'adult':
        query += 'WHERE rating = "R" OR rating = "NC-17" ORDER BY ORDER BY release_year DESC LIMIT 100'
    else:
        return jsonify(status=404)

    result = []

    for movie in get_all(query):
        result.append(
            {
                'title': movie['title'],
                'rating': movie['rating'],
                'description': movie['description']
            }
        )

    return result


@app.get('/genre/<value>')
def genre(value):
    query = f"""
    SELECT * FROM netflix
    WHERE listed_in LIKE '%{value}%'
    ORDER BY date_added DESC
    LIMIT 15
    """

    result = []

    for movie in get_all(query):
        result.append(
            {
                'title': movie['title'],
                'description': movie['description'],
                'ganre': movie['listed_in']
            }
        )

    return result


if '__main__' == __name__:
    app.run(debug=True)
