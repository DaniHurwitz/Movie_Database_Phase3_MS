import statistics
import random
import sys
import requests
import os

import serialize_movie_data

MOVIE_API_KEY = 'a5f9b40'
MY_WEBSITE_TITLE = "Movies - Phase 3"


class MovieApp:
    def __init__(self, storage):
        self._storage = storage
        self.movies = self._storage.list_movies()

    def menu(self):
        # Prints Menu options to screen
        print('''
        Menu:
        0. Exit
        1. List movies
        2. Add movie
        3. Delete movie
        4. Update movie
        5. Stats
        6. Random movie
        7. Search movie
        8. Movies sorted by rating
        9. Generate website
        ''')


    def exit_program(self):
        print('Bye!')
        sys.exit()


    def _command_list_movies(self):
        '''
        Lists how many movies, all movie titles, with year and rating
        '''
        total_movies = len(self.movies)
        print(f"There are {total_movies} movies in total")

        for title, info in self.movies.items():
            print(f"{title}, {info['year']} - rating: {info['rating']}")


    def _command_add_movie(self):
        '''
        Asks the user to input a movie title, using an API to get correct title, year, rating, and poster URL
        [API used: OMDb API - The Open Movie Database]
        add_movie_storage() from the movie_storage module is called: adding & saving the updated list to JSON
        '''
        movie_input = input('Enter new movie name: ')
        # Replace spaces with '+'
        formatted_movie_input = movie_input.replace(' ', '+')

        try:
            response = requests.get(f"http://www.omdbapi.com/?apikey={MOVIE_API_KEY}&t={formatted_movie_input}")
            api_data = response.json()

            if 'Response' in api_data and api_data['Response'] == 'False':
                print("Error: Movie not found!")
            else:
                title = api_data['Title']
                # Check for duplicates:
                if title in self.movies:
                    print(f"Movie '{title}' already exists in the database!")
                    return

                year = api_data['Year']
                rating = api_data['imdbRating']
                float_rating = float(rating)
                poster_image_URL = api_data['Poster']

                self._storage.add_movie(title, year, float_rating, poster_image_URL)

                print(f"Movie '{title}' successfully added to the database!")

        except requests.exceptions.ConnectionError as e:
            # (e.g., no internet access, server unreachable)
            print("Connection Error:", e)
            print("Please check your internet connection and try again.")
        except requests.exceptions.RequestException as e:
            # request-related error (e.g., invalid URL, timeout, too many redirects)
            print("Request Exception:", e)
            print("There was an issue with the API request. Please try again later.")
        except Exception as e:
            # If any other unexpected error occurs
            print("Unexpected Error:", e)
            print("An unexpected error occurred.")


    def _command_delete_movie(self):
        '''
        Asks user which movie should be deleted, iterates over movie titles
        and removes user input movie if it exists in the list
        '''
        movie_to_delete = input("Enter movie name to delete: ")
        self._storage.delete_movie(movie_to_delete)


    def _command_update_movie(self):
        '''Updates the rating of a user-specified movie in the list with a user-specified rating.'''
        movie_to_update = input("Enter movie name: ")

        if movie_to_update in self.movies:
            new_movie_rating = float(input("Enter new movie rating (0-10): "))
            self._storage.update_movie(movie_to_update, new_movie_rating)
        else:
            print(f"The movie '{movie_to_update}' doesn't exist in the database!")


    def _command_stats(self):
        '''Prints average, median ratings, best & worst movies from provided movie list '''
        movie_ratings = []

        for movie, info in self.movies.items():
            movie_ratings.append(info["rating"])
        # Average
        average_rating = sum(movie_ratings) / len(movie_ratings)
        print(f"Average rating: {round(average_rating, 1)}")
        # Median
        median_rating = statistics.median(movie_ratings)
        print(f"Median rating: {round(median_rating, 1)}")
        # Best Movie
        max_rating = max(info["rating"] for movie, info in
                         self.movies.items()) #Find the maximum rating among all movies using max() on generator expr.
        best_movies = [movie for movie, info in self.movies.items() if
                       info['rating'] == max_rating]  # create a list of best movies
        best_movies_str = ", ".join(best_movies)
        print(f"Best movie(s): {best_movies_str} - {max_rating}")
        # Worst Movie
        min_rating = min(info["rating"] for movie, info in self.movies.items())
        worst_movies = [movie for movie, info in self.movies.items() if info['rating'] == min_rating]
        worst_movies_str = ", ".join(worst_movies)
        print(f"Worst movie(s): {worst_movies_str}, {min_rating}")


    def _command_random_movie(self):
        '''prints a random movie and its rating'''
        random_movie_title = random.choice(list(self.movies.keys()))
        random_movie_rating = self.movies[random_movie_title]["rating"]

        print(f"Your movie for tonight: {random_movie_title}, it is rated {random_movie_rating}")


    def _command_search_movie(self):
        '''
        Asks user to enter part of a movie, searches all movies in database and prints all movies matching the
        query, along with its rating
        '''
        user_search_input = input("Enter part of movie name: ").lower()
        matching_search_movies = []

        for movie, info in self.movies.items():
            if user_search_input in movie.lower():
                matching_search_movies.append((movie, info))

        if len(matching_search_movies) > 0:
            for matched_movie, info in matching_search_movies:
                print(f"{matched_movie}: {info['rating']}")
        else:
            print(f"Movie '{user_search_input}' not found :(")


    def _command_movies_sorted_by_rating(self):
        '''Prints the movies and ratings in descending order based on rating'''
        sorted_movies = sorted(self.movies.items(), key=lambda movie: movie[1]['rating'], reverse=True)

        for movie, info in sorted_movies:
            print(f"{movie}: {info['rating']}")


    def generate_website(self):
        '''
        Generates a website using functions from generate_website module to do templating on an
        HTML template file (+ accompanying CSS)
        '''
        output = serialize_movie_data.serialize_movie(self.movies)

        # File path to 'index_template.html' file in the '_static' folder for CODIO:
        template_file_path = os.path.join(os.path.dirname(__file__), '_static', 'index_template.html')

        # Replace place-holders on the HTML template file with serialized movie output from JSON file
        with open(template_file_path, "r") as movie_file:
            data = movie_file.read()
            data = data.replace("__TEMPLATE_MOVIE_GRID__", output)
            data = data.replace("__TEMPLATE_TITLE__", MY_WEBSITE_TITLE)

        # Create a new HTML doc with the desired movie content
        with open("movie_website.html", "w") as fileobj:
            fileobj.write(data)

        print('Website was successfully generated.')


    def run(self):
        while True:
            try:
                self.menu()
                user_option = int(input("Enter your choice (0 to 9): "))

                if user_option == 0:
                    self.exit_program()
                elif user_option == 1:
                    self._command_list_movies()
                    input("\nPress enter to continue.")
                elif user_option == 2:
                    self._command_add_movie()
                    input("\nPress enter to continue.")
                elif user_option == 3:
                    self._command_delete_movie()
                    input("\nPress enter to continue.")
                elif user_option == 4:
                    self._command_update_movie()
                    input("\nPress enter to continue.")
                elif user_option == 5:
                    self._command_stats()
                    input("\nPress enter to continue.")
                elif user_option == 6:
                    self._command_random_movie()
                    input("\nPress enter to continue.")
                elif user_option == 7:
                    self._command_search_movie()
                    input("\nPress enter to continue.")
                elif user_option == 8:
                    self._command_movies_sorted_by_rating()
                    input("\nPress enter to continue.")
                elif user_option == 9:
                    self.generate_website()
                    input("\nPress enter to continue.")
                else:
                    print("Invalid input.")
            except ValueError:
                print("Invalid input. Please enter a number.")
