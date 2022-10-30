from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()
DB_URI = "mysql+pymysql://root:your_password@localhost:3306/playlist_service_db"
engine = create_engine(DB_URI)

Session = sessionmaker(bind=engine)
