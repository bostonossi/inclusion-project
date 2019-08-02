import json
import pandas as pd
import requests
from sqlalchemy import *
from enum import Enum
from bossdi_db import *
from sqlalchemy.orm import sessionmaker
from github import Github


import json

with open('ossdi.config.json') as config_file:
    confidg_data = json.load(config_file)

class OSSDI_Collector:
    """
    a class for getting metrics from the GitHub API
    """
    def __init__(self, api_key):
        """
        Creates a new GitHub instance
        
        : param api_key: GitHub API key
        """
        self.GITHUB_API_KEY = confidg_data['GitHub']['apikey']
        self.api = Github(api_key)
        self.bossdi_db = Bossdi(user = confidg_data['Ossdi']['user'], 
                                password = confidg_data['Ossdi']['pass'],
                                host = confidg_data['Ossdi']['host'], 
                                port = confidg_data['Ossdi']['port'], 
                                dbname = confidg_data['Ossdi']['name'])
        engine = self.bossdi_db.get_db()
        Base.metadata.create_all(engine)
        Session = sessionmaker()
        Session.configure(bind=engine)
        self.conn = engine.connect()
        self.session = Session()

        
class COC_Statuses(Enum):
    """
    This class enumerates the various potential states of a repository's
    code of conduct.
    """
    GITHUB_DET_NONE = 1
    GITHUB_DET_YES = 2
    IN_README = 3
    IN_SEPARATE_FILES = 4
      
        
class COC_Collector(OSSDI_Collector):
    """
    This class collects data on the state of a given repository's code of conduct
    file, and populate the corresponding table in the Bossdi database.
    """
    def __init__(self, api_key):
        super().__init__(api_key)

        exists = self.session.query(self.session.query(COC_State).filter_by\
                                  (state='GitHub_det_None').exists()).scalar()
        if not exists:
            self.session.add(COC_State(state = 'GitHub_det_None'))
            self.session.add(COC_State(state = 'GitHub_det_Yes'))
            self.session.add(COC_State(state = 'in_ReadMe'))
            self.session.add(COC_State(state = 'in_separate_files'))
            self.session.commit()
        

    def code_of_conduct(self, owner, repo):
        """
        Determines whether a given repository has a code of conduct file
        and record the result in the Bossdi database.

        :param owner: The name of the Project owner.
        :param repo: The name of the repo
        :return: DataFrame with the result
        """
        url = "http://api.github.com/repos/{}/{}/community/code_of_conduct".format\
              (owner, repo)
        header = {'Accept': 'application/vnd.github.scarlet-witch-preview+json'}
        json = requests.get(url, auth=('user', self.GITHUB_API_KEY), headers=header).json()

        exists = self.session.query(self.session.query(Projects).filter_by\
                                  (repo_name = repo).exists()).scalar()
        if json['body'] != None:
            if not exists:
                self.session.add(Projects(repo_owner = owner, repo_name = repo, code_of_conduct_state = 2))
                self.session.commit()
            else:
                repo_object = self.session.query(Projects).filter_by(repo_name = repo).first()
                repo_object.code_of_conduct_state = 2
                self.session.commit()
        else:
            if not exists:
                self.session.add(Projects(repo_owner = owner, repo_name = repo, code_of_conduct_state = 1))
                self.session.commit()
            else:
                repo_object = self.session.query(Projects).filter_by(repo_name = repo).first()
                repo_object.code_of_conduct_state = 1
                self.session.commit()
