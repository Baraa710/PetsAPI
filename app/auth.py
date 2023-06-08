
from app import login_manager
import re

login_manager.login_view = "login"

def is_valid_email_address(email_address):
   match = re.match(r"^[\w\-\.]+@([\w\-]+\.)+[\w\-]{2,4}$", email_address)
  
   return bool(match)
