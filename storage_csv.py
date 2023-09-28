from istorage import IStorage
import os
import csv


class StorageCsv(IStorage):
    def __init__(self, file_path):
        self.file_path = file_path
        self.movies = {}

        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as file:
                    csv_reader = csv.DictReader(file) #Convert CSV to dictionary
                    for row in csv_reader:
                        title = row['title']
                        rating = float(row['rating'])
                        year = row['year']
                        poster = row['poster']

                        # Create a dictionary for each movie
                        movie_info = {
                            "rating": rating,
                            "year": year,
                            "poster": poster
                        }

                        self.movies[title] = movie_info

            except FileNotFoundError:
                print(f"File not found: {file_path}")
            except csv.Error as csv_error:
                print(f"CSV Error in {file_path}: {csv_error}")
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
        if title in self.movies:
            print(f"A movie with the title '{title}' already exists in the database.")
            return

        self.movies[title] = {
            "rating": rating,
            "year": int(year),
            "poster": poster_image_URL,
        }
        self.save_movies_to_CSV()


    def delete_movie(self, title):
        '''
        Deletes a movie from the movies database.
        :param title: Movie title, given by user input
        '''
        if title in self.movies:
            del self.movies[title]
            self.save_movies_to_CSV()
            print(f"The movie '{title}' has been successfully deleted.")
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
            self.save_movies_to_CSV()
            print(f"The movie '{title}' was successfully updated.")
        else:
            print(f"The movie '{title}' doesn't exist!")


    def save_movies_to_CSV(self):
        '''
        Saves the movie data to the CSV file.
        '''
        with open(self.file_path, "w", newline='') as file:
            fieldnames = ["title", "year", "rating", "poster"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Check if the file is empty (no header)
            if file.tell() == 0:
                writer.writeheader()

            for title, movie_data in self.movies.items():
                row = {"title": title, **movie_data}
                writer.writerow(row)
