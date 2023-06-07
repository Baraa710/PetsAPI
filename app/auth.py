from flask_login import login_required, login_remembered, login_user
from app import login_manager, User

login_manager.login_view = "login"

