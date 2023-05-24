from flask import jsonify
from api.app import app, db
from api.models.it_college_type import it_college_type


@app.route('/id_type/<int:id>', methods=['GET'])
def get_member_type_id(id):
    member = it_college_type.query.get(id)
    if member:
        return jsonify(f"Member ID: {member.id},member type: {member.name},registered: {member.registered}")
    else:
        return 'Member not found'
