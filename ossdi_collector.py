import json
from github import Github
from sqlalchemy import *
from bossdi_db import *
from sqlalchemy.orm import sessionmaker

with open('ossdi.config.json') as config_file:
    config_data = json.load(config_file)

class OSSDI_Collector:
    """
    skeleton class for establishing connection with the OSSDI database 
    """
    def __init__(self, api_key):
        """
        reads the ossdi.config.json file and creates sqlalchemy connection
        
        : param api_key: GitHub API key
        """
        self.GITHUB_API_KEY = config_data['GitHub']['apikey']
        self.api = Github(api_key)
        self.bossdi_db = Bossdi(user = config_data['Ossdi']['user'], 
                                password = config_data['Ossdi']['pass'],
                                host = config_data['Ossdi']['host'], 
                                port = config_data['Ossdi']['port'], 
                                dbname = config_data['Ossdi']['name'])
        engine = self.bossdi_db.get_db()
        Base.metadata.create_all(engine)
        Session = sessionmaker()
        Session.configure(bind=engine)
        self.conn = engine.connect()
        self.session = Session()

    def get_data(self, owner, repo):

        url = "http://api.github.com/repos/{}/{}/readme".format\
              (owner, repo)
        
        header = {'Accept': 'application/vnd.github.scarlet-witch-preview+json'}
        
        json = requests.get(url, auth=('user', self.GITHUB_API_KEY)).json()

        return json 

