import json
import requests
from sqlalchemy import *
from enum import Enum
from ossdi_collector import *
from bossdi_db import COC_State

  
class COC_Statuses(Enum):
    """
    This class enumerates the various potential states of a repository's
    code of conduct.
    """
    GH_DETERMINED_NONE = 1
    GH_DETERMINED_YES = 2
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
                                  (state = 'GitHub_det_None').exists()).scalar()
        if not exists:
            self.session.add(COC_State(shortName = 'GH_DETERMINED_NONE', \
                                       prettyName = 'GitHub Determined None'))
            self.session.add(COC_State(shortName = 'GH_DETERMINED_YES', \
                                       prettyName = 'GitHub Determined Yes'))
            self.session.add(COC_State(shortName = 'IN_README', \
                                       prettyName = 'In Readme'))
            self.session.add(COC_State(shortName = 'IN_SEPARATE_FILES', \
                                       prettyName = 'In Separate Files'))
            self.session.commit()
        

    def code_of_conduct(self, owner, repo):
        """
        Determines whether a given repository has a code of conduct file
        and record the result in the Bossdi database.

        :param owner: The name of the Project owner.
        :param repo: The name of the repo
        :return: DataFrame with the result
        """

        # url = "http://api.github.com/repos/{}/{}/community/code_of_conduct".format\
        #        (owner, repo)
        # header = {'Accept': 'application/vnd.github.scarlet-witch-preview+json'}
        # json = requests.get(url, auth=('user', self.GITHUB_API_KEY), headers=header).json()

        data = get_data(self, owner, repo)

        exists = self.session.query(self.session.query(Projects).filter_by\
                                  (repo_name = repo).exists()).scalar()
        if data['body'] != None:
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

#COC_Collector(api_key = '7638ba942b41459175c33c3244c612e35674583c').code_of_conduct( owner = 'kubernetes', repo = 'kubernetes')