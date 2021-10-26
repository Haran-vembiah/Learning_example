from sqlalchemy import create_engine
# from sqlalchemy import select

engine = create_engine("postgresql+psycopg2://postgres:54321@localhost/postgres",
                       echo=True, pool_size=6, max_overflow=10, encoding='latin1')
engine.connect()

print(engine)

