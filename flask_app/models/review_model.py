
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user_model  import User 
from flask_app import DB
from flask import flash


class Review: #match to workbench table
    def __init__(self,data):
        self.id = data['id']
        self.restaurant_name = data['restaurant_name']
        self.thoughts = data['thoughts']
        self.recommend = data['recommend']
        self.review_date = data['review_date']
        self.location = data['location'] #map api
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

#CREATE
    @classmethod
    def create(cls,data):
        query = "INSERT INTO reviews (restaurant_name, thoughts, recommend, review_date, location, user_id) VALUES(%(restaurant_name)s, %(thoughts)s, %(recommend)s, %(review_date)s, %(location)s, %(user_id)s);"
        return connectToMySQL(DB).query_db(query, data)

#RETRIEVE
    @classmethod
    def get_all_reviews(cls):
        query = "SELECT * FROM reviews ORDER BY created_at DESC"
        results= connectToMySQL(DB).query_db(query)
        all_reviews = []
        for row in results:
            all_reviews.append(cls(row))
        return all_reviews

    @classmethod
    def get_one_review(cls,data):
        query= "SELECT * FROM reviews WHERE id=%(id)s;"
        results= connectToMySQL(DB).query_db(query, data)
        if results:
            review = cls(results[0])
            return review

#UPDATE
    @classmethod
    def update(cls,data):
        query = "UPDATE reviews SET restaurant_name=%(restaurant_name)s, thoughts=%(thoughts)s, recommend=%(recommend)s, review_date=%(review_date)s, location=%(location)s WHERE id=%(id)s;"
        return connectToMySQL(DB).query_db(query, data)

#DELETE
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM reviews WHERE id=%(id)s;"
        return connectToMySQL(DB).query_db(query, data)

#VALIDATE
    @staticmethod
    def validate_review(data):
        errors = {}
        if len(data['restaurant_name']) <2:
            errors['restaurant_name']= "Restaurant Name must be at least 5 characters"
        if len(data['thoughts']) > 400:
            errors['thoughts']= "Review must be less than 400 characters"
        if len(data['recommend']) < 1:
            errors['recommend']= "Recommendation  is required"
        if len(data['review_date']) <2:
            errors['review_date']= "Review date is required"
        if len(data['location']) <2:
            errors['location']= "Restaurant location must be at least 5 characters"
        
        for category,msg in errors.items():
            flash(msg,category)
        
        return len(errors)==0