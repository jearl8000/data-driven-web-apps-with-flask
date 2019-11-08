import os

import flask
import pypi_org.services.package_service as package_service
from pypi_org.infrastructure.view_modifiers import response
import pypi_org.data.db_session as db_session

app = flask.Flask(__name__)


def main():
    register_blueprints()
    setup_db()
    app.run(debug=True)


def register_blueprints():
    from pypi_org.views import home_views, package_views, cms_views
    app.register_blueprint(home_views.blueprint)
    app.register_blueprint(package_views.blueprint)
    app.register_blueprint(cms_views.blueprint)


def setup_db():
    db_file = os.path.join(
        os.path.dirname(__file__),
        'db',
        'pypi.sqlite')

    db_session.global_init(db_file)


if __name__ == '__main__':
    main()
