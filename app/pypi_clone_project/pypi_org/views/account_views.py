import flask

from pypi_org.infrastructure import cookie_auth, request_dict
from pypi_org.infrastructure.view_modifiers import response
from pypi_org.services import user_service
from pypi_org.viewmodels.account.index_viewmodel import IndexViewModel
from pypi_org.viewmodels.account.register_viewmodel import RegisterViewModel

blueprint = flask.Blueprint('account', __name__, template_folder='templates')


@blueprint.route('/account')
@response(template_file='account/index.html')
def index():
    vm = IndexViewModel()
    if not vm.user:
        return flask.redirect('/account/login')

    return vm.to_dict()


@blueprint.route('/account/register', methods=['GET'])
@response(template_file='account/register.html')
def register_get():
    vm = RegisterViewModel()
    return vm.to_dict()


@blueprint.route('/account/register', methods=['POST'])
@response(template_file='account/register.html')
def register_post():
    vm = RegisterViewModel()

    vm.validate()
    if vm.error:
        return vm.to_dict()

    user = user_service.create_user(vm.name, vm.email, vm.password)
    if not user:
        vm.error = 'The account could not be created.'
        return vm.to_dict()

    resp = flask.redirect('/account')
    cookie_auth.set_auth(resp, user.id)

    return resp


@blueprint.route('/account/login', methods=['GET'])
@response(template_file='account/login.html')
def login_get():
    return {
        'user_id': cookie_auth.get_user_id_via_auth_cookie(flask.request),
    }


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

    user = user_service.login_user(email, password)
    if not user:
        return {
            'error': 'Account does not exist, or password is incorrect',
            'email': email,
            'password': password
        }

    resp = flask.redirect('/account')
    cookie_auth.set_auth(resp, user.id)

    return resp


@blueprint.route('/account/logout')
def logout():
    resp = flask.redirect('/')
    cookie_auth.logout(resp)

    return resp
