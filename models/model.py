from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session

DB_URI = "mysql+pymysql://root:1307ak@localhost:3306/playlist_service_db"
engine = create_engine(DB_URI)


SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)
Base = declarative_base()