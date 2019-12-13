import flask
from pypi_org.infrastructure.view_modifiers import response
from pypi_org.services import user_service

blueprint = flask.Blueprint('account', __name__, template_folder='templates')


@blueprint.route('/account')
@response(template_file='account/index.html')
def index():
    return {}


@blueprint.route('/account/register', methods=['GET'])
@response(template_file='account/register.html')
def register_get():
    return {}


@blueprint.route('/account/register', methods=['POST'])
@response(template_file='account/register.html')
def register_post():

    r = flask.request
    name = r.form.get('name')
    email = r.form.get('email', '').lower().strip()
    password = r.form.get('password', '').strip()

    if not name or not email or not password:
        return {
            'error': 'Some required fields are missing.',
            'name': name,
            'email': email,
            'password': password
        }

    user = user_service.create_user(name, email, password)
    if not user:
        return {
            'error': 'A user with that email address already exists.',
            'name': name,
            'email': email,
            'password': password
        }

    # TODO: log in browser as a session

    return flask.redirect('/account')


@blueprint.route('/account/login', methods=['GET'])
@response(template_file='account/login.html')
def login_get():
    return {}


@blueprint.route('/account/login', methods=['POST'])
@response(template_file='account/login.html')
def login_post():

    r = flask.request
    email = r.form.get('email', '').lower().strip()
    password = r.form.get('password', '').strip()

    if not email or not password:
        return {
            'error': 'Some required fields are missing.',
            'email': email,
            'password': password
        }

    # TODO: validate user
    user = user_service.login_user(email, password)
    if not user:
        return {
            'error': 'Account does not exist, or password is incorrect',
            'email': email,
            'password': password
        }

    # TODO: log in browser as a session

    return flask.redirect('/account')


@blueprint.route('/account/logout', methods=['POST'])
def logout():
    return {}
