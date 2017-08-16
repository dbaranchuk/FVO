from app import lm
from app.models import User
from flask_login import current_user

@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def user_role(user_id=None):
	user = current_user if user_id is None else User.query.get(user_id)
	if not isinstance(user.is_authenticated, bool) and user.is_authenticated():
		return user.role
	else:
		return -1