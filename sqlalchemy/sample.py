# from sqlalchemy import select
import sqlalchemy as db

engine = db.create_engine("postgresql+psycopg2://postgres:54321@localhost/postgres",
                          echo=True, pool_size=6, max_overflow=10, encoding='latin1')
connection = engine.connect()
metadata = db.MetaData()

census = db.Table(mgt.flights, metadata, autoload=True, autoload_with=engine)
# Print the column names
print(census.columns.keys())
print(engine)
print(dir(engine))
print(dir(type(engine.table_names)))
