from flask import render_template,redirect,request,session,url_for
from flask_app.models.user_model import User
from flask_app.models.review_model import Review
from flask_app import app

#HELPER functions for DISPLAY
def get_current_user():
    return User.retrieve_one_user(id=session['id'])

def get_current_review(id):
    return Review.get_one_review({'id':id})

def get_all_reviews():
    return Review.get_all_reviews()

#DISPLAY
@app.route('/new/review')
def new_review():
    user = get_current_user()
    return render_template("new_review.html", user=user)

@app.route('/user/account')
def user_account():
    user = get_current_user()
    reviews = get_all_reviews()
    return render_template('user_account.html', user=user, reviews=reviews)

@app.route('/edit/<int:id>')
def edit_review(id):
    user = get_current_user()
    review = get_current_review(id)
    return render_template('edit_review.html', user=user, review=review)

@app.route('/show/<int:id>')
def view_review(id):
    user = get_current_user()
    review = get_current_review(id)
    return render_template('view_one_review.html', user=user, review=review)





#HELPER functions for ACTIONS
#plants a new review record using request.form and session['id'] data
def create_new_review():
    data = {
        'restaurant_name': request.form['restaurant_name'],
        'thoughts': request.form['thoughts'],
        'recommend': request.form['recommend'],
        'review_date': request.form['review_date'],
        'location': request.form['location'],
        'user_id': session['id']
    }
    Review.create(data)

# update a review record using request.form data and id
def update_review(id):
    data = {
        'id':id,
        'restaurant_name': request.form['restaurant_name'],
        'thoughts': request.form['thoughts'],
        'recommend': request.form['recommend'],
        'review_date': request.form['review_date'],
        'location': request.form['location']
    }
    Review.update(data)

def delete_a_review(id):
    Review.delete({'id':id})

def vaild_review_data():
    return Review.validate_review(request.form)


#ACTIONS
@app.route('/review/create', methods = ['POST'])
def create_review():
    if not vaild_review_data():
        return redirect(url_for('new_review'))
    create_new_review()
    return redirect(url_for('user_account'))

@app.route('/review/update/<int:id>', methods=['POST'])
def update_review(id):
    if not vaild_review_data():
        return redirect(url_for('dashboard'))
    update_review(id)
    return redirect(url_for('user_account'))

@app.route('/delete_review/<int:id>')
def delete_review(id):
    delete_a_review(id)
    return redirect(url_for('user_account'))    