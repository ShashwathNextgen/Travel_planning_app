import psycopg2
from psycopg2 import sql
from werkzeug.security import generate_password_hash, check_password_hash
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseConnection:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.connection = None

    def __enter__(self):
        self.connection = psycopg2.connect(
            host=self.host,
            database=self.database,
            user=self.user,
            password=self.password
        )
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()
        if exc_type is not None:
            logger.error("Exception occurred: %s", exc_value)
        print("Database connection closed.")

class PlaceDetails:
    def __init__(self, place_id, name,location,description):
        self.id = place_id
        self.name = name
        self.location = location
        self.description = description


    def __str__(self):
        return (f"place_id: {self.id}, Name: {self.name}, Description: {self.desc[:60]}..., "
                f"Location: {self.location}")


class Places:
    def __init__(self, host, database, user, password):
        self.db_params = (host, database, user, password)

    def fetch_places(self, search_term=None):
        with DatabaseConnection(*self.db_params) as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM place"
            if search_term:
                query += " WHERE name ILIKE %s"
                cursor.execute(query, (f'%{search_term}%',))
            else:
                cursor.execute(query)
            places_data = cursor.fetchall()
            cursor.close()
        places = [PlaceDetails(*place_data) for place_data in places_data]
        return places

