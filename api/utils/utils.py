import random

from api.models.it_college import it_college


def generate_unique_code():
    return random.randint(1000000000, 9999999999)


def check_unique_code(code):
    check = it_college.query.filter_by(unique_code=str(code)).first()
    if check:
        return True
    else:
        return False
