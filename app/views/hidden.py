from app import lm
from app.models import User
from flask_login import current_user

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def user_role():
    if not isinstance(current_user.is_authenticated, bool) and current_user.is_authenticated():
        return current_user.role
    else:
        return -1