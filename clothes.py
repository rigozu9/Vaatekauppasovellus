# method to get clotehs for database

from db import db
from models import Clothes  # Import Clothes model from models module

def get_clothes():
    # Fetch all clothing items from the clothes table
    result = Clothes.query.all()
    return result
