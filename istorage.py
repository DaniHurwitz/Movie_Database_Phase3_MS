from abc import ABC, abstractmethod


class IStorage(ABC):
    @abstractmethod
    def list_movies(self):
        '''
        Abstract method for listing movies.
        This method should be implemented in subclasses to provide a list of movies.
        :return: Returns a dictionary of dictionaries that contains the movies information in the database.
        '''
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        '''
        Abstract method for adding movies to database.
        '''
        pass

    @abstractmethod
    def delete_movie(self, title):
        '''
        Abstract method to delete a movie from the movies database.
        '''
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        '''
        Abstract method to update the rating of a movie from the movies database.
        '''
        pass
