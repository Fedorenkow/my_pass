import pandas as pd
from flask import request, render_template, jsonify, url_for
from api.app import db, app
from api.models import it_college_type
from api.models.it_college import it_college
from api.models.it_college_type import it_college_type
from api.utils.utils import generate_unique_code, check_unique_code


@app.route('/')
def hello():
    return 'hello'


@app.route('/add', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        # Отримання даних з запиту POST
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        type_id = request.form.get('type_id')
        id = request.form.get('id')
        name = request.form.get('name')
        unique_code = str(generate_unique_code())

        # Перевірка чи всі дані присутні у запиті POST
        if not all([first_name, last_name, email, type_id]):
            return 'Please fill in all required fields.', 400

        # Перевірка чи введений email не зареєстрований вже в базі даних
        member = it_college.query.filter_by(email=email).first()
        if member:
            return 'Member with this email already exists.', 409

        # Перевірка чи унікальний код не зареєстрований
        unique = it_college.query.filter_by(unique_code=unique_code).first()
        while unique:
            unique_code = generate_unique_code()
            unique = it_college.query.filter_by(unique_code=unique_code).first()

        # Створення нового члену і додавання до бази даних
        new_member = it_college(first_name=first_name,
                                last_name=last_name,
                                email=email,
                                unique_code=unique_code,
                                type_id=type_id)
        new_member_type = it_college_type(id=id,
                                          name=name)
        db.session.add(new_member)
        db.session.add(new_member_type)
        db.session.commit()

        return render_template("insert_user.html", title="Register")

    else:
        return render_template("insert_user.html", title="Register")


@app.route('/id/<int:id>', methods=['GET'])
def get_member_id(id):
    member = it_college.query.get(id)
    if member:
        return jsonify({
            'Member ID': member.id,
            'First Name': member.first_name,
            'Last Name': member.last_name,
            'Email': member.email,
            'Unique Code': member.unique_code
        })
    else:
        return 'Member not found'


@app.route('/all', methods=['GET'])
def all_member():
    all_values = it_college.query.all()
    results = []

    for value in all_values:
        result = {
            'Member ID': value.id,
            'First Name': value.first_name,
            'Last Name': value.last_name,
            'Email': value.email,
            'Unique Code': value.unique_code
        }
        results.append(result)

    return jsonify(results)


@app.route('/delete/<int:id>', methods=['DELETE'])
def delete_member(id):
    member = it_college.query.get(id)

    # Видаляємо запис з таблиці it_college
    db.session.delete(member)

    # Видаляємо запис з таблиці it_college_type за відповідним type_id
    member_type = it_college_type.query.filter_by(id=member.type_id).first()
    db.session.delete(member_type)

    db.session.commit()

    return jsonify({"message": f"User id {id} deleted successfully"})


@app.route('/excel', methods=['GET', 'POST'])
def parser_excel():
    if request.method == 'POST':
        file = request.files['file']

        if file and file.filename.endswith('.xlsx'):
            try:

                df = pd.read_excel(file)

                for index, row in df.iterrows():
                    first_name = row['First Name']
                    last_name = row['Last Name']
                    email = row['Email']
                    name = row['Type_value']
                    type_id = row['Type_id']
                    id = row['Id']
                    unique_code = str(generate_unique_code())

                    # Перевірка чи унікальний код не зареєстрований у базі
                    unique = it_college.query.filter_by(unique_code=unique_code).first()
                    while unique:
                        unique_code = generate_unique_code()
                        unique = it_college.query.filter_by(unique_code=unique_code).first()

                    member = it_college(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        unique_code=unique_code,
                        type_id=type_id
                    )
                    member_type = it_college_type(
                        id=id,
                        name=name,
                    )

                    db.session.add(member)
                    db.session.add(member_type)

                db.session.commit()

                return 'Members added successfully'

            except Exception as e:
                return f'Error occurred: {str(e)}'

    else:
        return render_template("parser_excel.html", title="Parse")


@app.route('/check/<string:code>', methods=["GET"])
def check_code(code):
    result = check_unique_code(code)
    return jsonify(result)


@app.route('/home')
def home_page():
    return render_template("home_page.html", title="Home")
