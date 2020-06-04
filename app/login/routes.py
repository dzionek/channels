from flask import Blueprint, request, render_template
from .utils import log_in, is_logged, set_up_app

login = Blueprint('login', __name__)

@login.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        return log_in(request.form)
    else:
        if is_logged():
            return set_up_app()
        else:
            return render_template('login.html')