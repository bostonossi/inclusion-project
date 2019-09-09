from sqlalchemy import *
import sqlalchemy as s


from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Bossdi(object):
    """Queries BOSSDI database"""

    def __init__(self, user, password, host, port, dbname, projects=None):
        """
        Connect to the database

        :param dbstr: The [database string](http://docs.sqlalchemy.org/en/latest/core/engines.html) to connect to the GHTorrent database
        """
        self.DB_STR = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(
            user, password, host, port, dbname
        )
        self.db = s.create_engine(self.DB_STR, poolclass=s.pool.NullPool)
        self.projects = projects

    def get_db(self):
        return self.db


class COC_State(Base):
    __tablename__ = 'CODE_CONDUCT_STATE'
    
    id = Column(Integer, primary_key=True)
    shortName = Column(String(50), nullable=False)
    prettyName = Column(String(50), nullable=False)

class Readme_State(Base):
    __tablename__ = 'README_STATE'

    id = Column(Integer, primary_key=True)
    shortName = Column(String(50), nullable=False)
    prettyName = Column(String(50), nullable=False)

class Projects(Base):
    __tablename__ = 'PROJECTS'

    id = Column(Integer, primary_key=True)
    repo_owner = Column(String(30), nullable=False)
    repo_name = Column(String(30), nullable=False)
    code_of_conduct_state = Column(Integer, \
                                      ForeignKey('CODE_CONDUCT_STATE.id'), \
                                      nullable=True)
    readme_state = Column(Integer, ForeignKey('README_STATE.id'),\
                             nullable=True)
    GHTorrent_Id = Column(Integer, nullable=True)



    
    


