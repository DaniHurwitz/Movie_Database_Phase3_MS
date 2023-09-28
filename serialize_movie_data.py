def serialize_movie(movie_obj):
    '''takes a movie_obj parameter and returns a serialized HTML string for that movie object.'''
    output = ''
    for movie, details in movie_obj.items():
        # Get the movie variables
        poster_url = details.get('poster')
        year = details.get('year')
        rating = details.get('rating')

        # Add the movie-specific information to the 'output' string
        output += '<li>\n'
        output += '<div class="movie">\n'
        output += f'<img class="movie-poster" src="{poster_url}" title="{movie}" alt="{movie} movie poster"/>\n'
        output += f'<div class="movie-title">{movie}</div>\n'
        output += f'<div class="movie-year">{year}</div>\n'
        output += f'<div class="movie-rating">{rating}/10 </div>\n'
        output += '</div>\n'
        output += '</li>\n\n'

    return output

