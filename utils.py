import sqlite3


def get_one(query):
    with sqlite3.connect('netflix.db') as connection:
        connection.row_factory = sqlite3.Row
        result = connection.execute(query).fetchone()

        if result is None:
            return None
        else:
            return dict(result)


def get_all(query):
    with sqlite3.connect('netflix.db') as connection:
        connection.row_factory = sqlite3.Row
        result = connection.execute(query).fetchall()

        movies = []

        for item in result:
            movies.append(dict(item))

        return movies


def get_actor(actor1, actor2):
    query = f"""
    SELECT * FROM netflix
    WHERE netflix.cast LIKE '%{actor1}%' AND netflix.cast LIKE '%{actor2}%'
    """

    cast = []
    set_cast = set()
    result = get_all(query)

    for movie in result:
        for actor in movie['cast'].split(', '):
            cast.append(actor)

    for actor in cast:
        if cast.count(actor) > 2:
            set_cast.add(actor)

    return set_cast

# print(get_actor('Jack Black', 'Dustin Hoffman'))


def get_movie(type_movie, release_year, listed_in):
    query = f"""
    SELECT * FROM netflix
    WHERE netflix.type = '{type_movie}'
    AND release_year = {release_year}
    AND listed_in LIKE '%{listed_in}%'
    """

    result = []

    for movie in get_all(query):
        result.append(
            {
                'title': movie['title'],
                'description': movie['description']
            }
        )

    return result

