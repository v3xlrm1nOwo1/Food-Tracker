from flask import request, redirect, render_template, url_for
from datetime import datetime
from sqlalchemy import text
from app import app
from app.models import *

@app.route('/', methods=['GET', 'POST'])
def home():    
    if request.method == 'POST':
        
        date = request.form['new-day']
        datetime_object = datetime.strptime(date, '%Y-%m-%d')
        datetime_database = datetime.strftime(datetime_object, '%Y%m%d')
                
        new_date = Log_date(date=datetime.strptime(date, '%Y-%m-%d'))
        
        try:
            db.session.add(new_date)
            db.session.commit()
            return redirect(url_for('home'))
        except:
            return "There was an issue adding your date ):"
    
    elif request.method == 'GET':
        foods_day = []
        
        sql = f'''SELECT Log_date.id, Log_date.date, SUM(Food.protein), SUM(Food.carbohydrates), SUM(Food.fat), SUM(Food.calories)
                  FROM Log_date
                  LEFT JOIN Food_date ON Food_date.log_date_id = log_date.id 
                  LEFT JOIN Food ON Food.id = Food_date.Food_id 
                  GROUP BY Log_date.id 
                  ORDER BY Log_date.date DESC'''
                  
        with db.engine.begin() as conn:
            for food_detils in conn.execute(text(sql)):
                foods_day.append({'log_date_id': int(food_detils[0]), 'log_date': datetime.strftime(datetime.strptime(food_detils[1], '%Y-%m-%d'), '%B %d, %Y'), 'protein': food_detils[2], 'carbohydrates': food_detils[3], 'fat': food_detils[4], 'calories': food_detils[5]})
            
        return render_template('home.html', foods_day=foods_day)


@app.route('/view/<int:id>', methods=['GET', 'POST'])
def day(id):
    if request.method == 'POST':
        food_id = request.form['food-name']

        food_day = Food_date(food_id=food_id, log_date_id=id)
        
        try:
            db.session.add(food_day)
            db.session.commit()
            return redirect(url_for('day', id=id))
        except:
            return "There was an issue adding your date ):"
    
    elif request.method == 'GET':
        date = Log_date.query.get_or_404(id)
        foods = Food.query.order_by(Food.id).all()        
        
        foods_day = []
        total = {'protein': 0, 'carbohydrates': 0, 'fat': 0, 'calories': 0}
        
        sql = f'''SELECT Food.name, Food.protein, Food.carbohydrates, Food.fat, Food.calories 
                  FROM Log_date 
                  JOIN Food_date ON Food_date.log_date_id = log_date.id 
                  JOIN Food ON Food.id = Food_date.Food_id 
                  WHERE Log_date.id = {id}'''
                  
        with db.engine.begin() as conn:
            for food_detils in conn.execute(text(sql)):
                foods_day.append({'food': {'name': food_detils[0], 'protein': food_detils[1], 'carbohydrates': food_detils[2], 'fat': food_detils[3], 'calories': food_detils[4]}})
                total['protein'] = total['protein'] + food_detils[1]
                total['carbohydrates'] = total['carbohydrates'] + food_detils[2]
                total['fat'] = total['fat'] + food_detils[3]
                total['calories'] = total['calories'] + food_detils[4]

        return render_template('day.html', date_id=date.id, date=datetime.strftime(date.date, '%B %d, %Y'), foods=foods, foods_day=foods_day, total=total)


@app.route('/food', methods=['GET', 'POST'])
def food():
    if request.method == 'POST':
        name = request.form['food-name']
        protein = int(request.form['protein'])
        carbohydrates = int(request.form['carbohydrates'])
        fat = int(request.form['fat'])
        calories = protein * 4 + carbohydrates * 4 + fat * 9
        print(calories)
        
        new_food = Food(name=name, protein=protein, carbohydrates=carbohydrates, fat=fat, calories=calories)
        
        try:
            db.session.add(new_food)
            db.session.commit()
            return redirect(url_for('food'))
        except:
            return "There was an issue adding your food ):"
    
    elif request.method == 'GET':
        foods = Food.query.order_by(Food.id).all()
        return render_template('add_food.html', foods=foods)