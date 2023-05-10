from flask import request, render_template
from api.app import db, app
from api.models import it_college_type
from api.models.it_college import it_college


@app.route('/')
def hello():
    return 'hello'

@app.route('/add', methods = ["POST"])
def add_member():
    # Отримання даних з запиту POST
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    unique_code = request.form.get('unique_code')
    type_id = request.form.get('type_id')

    # Перевірка чи всі дані присутні у запиті POST
    if not all([first_name, last_name, email, unique_code, type_id]):
        return 'Please fill in all required fields.', 400

    # Перевірка чи введений email не зареєстрований вже в базі даних
    member = it_college.query.filter_by(email=email).first()
    if member:
        return 'Member with this email already exists.', 409

    # Перевірка чи введений unique_code не зареєстрований вже в базі даних
    member = it_college.query.filter_by(unique_code=unique_code).first()
    if member:
        return 'Member with this unique code already exists.', 409

    # Перевірка чи введений type_id існує в таблиці it_college_type
    member_type = it_college_type.query.filter_by(id=type_id).first()
    if not member_type:
        return 'Invalid member type.', 400

    # Створення нового члену і додавання до бази даних
    new_member = it_college(first_name=first_name,
                            last_name=last_name,
                            email=email,
                            unique_code=unique_code,
                            type_id=type_id)
    db.session.add(new_member)
    db.session.commit()

    return render_template("insert_user.html", title="Register")
