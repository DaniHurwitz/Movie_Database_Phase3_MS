from istorage import IStorage
import os
import json


class StorageJson(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path
        self.movies = {}  # Initialize an empty dict to store movie data

        # Check if the JSON file exists
        if os.path.exists(file_path):
            try:
                # If it exists, load its contents into the movies list
                with open(file_path, 'r') as file:
                    self.movies = json.load(file)
            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except json.JSONDecodeError as json_error: #file does exist but contains invalid JSON data
                print(f"Error decoding JSON in {file_path}: {json_error}")
        else:
            print(f"File not found: {file_path}")


    def list_movies(self):
        '''
        Returns a dictionary of dictionaries that
        contains the movies information in the database.
        '''
        return self.movies


    def add_movie(self, title, year, rating, poster_image_URL):
        '''
        Adds a movie to the movies database.
        :param title: movie title
        :param year: year released
        :param rating: movie scored rating
        :param poster_image_URL: link to poster
        '''
        self.movies[title] = {
            "rating": rating,
            "year": year,
            "poster": poster_image_URL,
        }
        self.save_movies_to_JSON()


    def delete_movie(self, title):
        '''
        Deletes a movie from the movies database.
        :param title: Movie title, given by user input
        '''
        if title in self.movies:
            del self.movies[title]
            print(f"The movie '{title}' has been successfully deleted.")
            self.save_movies_to_JSON()
        else:
            print(f"The movie '{title}' doesn't exist!")


    def update_movie(self, title, rating):
        '''
        Updates a movie's rating in the movies database.
        :param title: Movie title specified by user input
        :param rating: New (updated) movie rating from user input
        '''
        if title in self.movies:
            self.movies[title]['rating'] = rating
            self.save_movies_to_JSON()
            print(f"The movie '{title}' was successfully updated.")
        else:
            print(f"The movie '{title}' doesn't exist!")


    def save_movies_to_JSON(self):
        '''
        Saves the movie data to the JSON file.
        '''
        with open(self.file_path, "w") as file:
            json.dump(self.movies, file, indent=4)


tester = StorageJson('films.json')
tester.list_movies()