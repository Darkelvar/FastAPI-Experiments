from sqlmodel import create_engine, SQLModel, Session

# URL structure: postgresql://username:password@localhost:port/DB_NAME
# If the Postgres is not hosted locally replace localhost with the actual address
postgre_url = ""
engine = create_engine(postgre_url, echo=True)


def create_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
