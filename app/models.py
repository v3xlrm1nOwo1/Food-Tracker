from app import app
from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///food_tracker.db"
db = SQLAlchemy(app)
    
class Log_date(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=True)
    
    def __repr__(self):
        return '<ID %r>' % self.id


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=True)
    protein = db.Column(db.Integer, nullable=True)    
    carbohydrates = db.Column(db.Integer, nullable=True)
    fat = db.Column(db.Integer, nullable=True)
    calories = db.Column(db.Integer, nullable=True)
    
    def __repr__(self):
        return '<ID %r>' % self.id
    

class Food_date(db.Model):
    food_id = db.Column(db.Integer, primary_key=True)
    log_date_id = db.Column(db.Integer, primary_key=True)
    
    def __repr__(self):
        return '<ID %r>' % self.log_date_id
    