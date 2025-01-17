import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

from pypi_org.data.modelbase import SqlAlchemyBase

__factory = None
# we could work with the session factory directly, but by making it 'private'
# and adding a 'create_session' function, the IDE can give type hints for the Session class


def global_init(db_file: str):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("You must specify a db file.")

    conn_str = 'sqlite:///' + db_file.strip()
    # print(conn_str)

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    # noinspection PyUnresolvedReferences
    import pypi_org.data.__all_models
    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory

    session: Session = __factory()
    session.expire_on_commit = False

    return session

