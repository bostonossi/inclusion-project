from ossdi_collector import *

class Readme_Statuses(Enum):
    """
    This class enumerates the various potential states of a repository's
    code of conduct.
    """
    GH_DETERMINED_NONE = 1
    GH_DETERMINED_YES = 2

class Readme_Collector(OSSDI_Collector):
    """
    This class collects data on the state of a given repository's Readme
    file, and populate the corresponding table in the Bossdi database.
    """
    def __init__(self, api_key):
        super().__init__(api_key)

        exists = self.session.query(self.session.query(Readme_State).filter_by\
                                  (state='GitHub_det_Yes').exists()).scalar()
        if not exists:
            self.session.add(Readme_State(shortName = 'GH_DETERMINED_NONE', \
                                          prettyName = 'GitHub Determined None'))
            self.session.add(Readme_State(shortName = 'GH_DETERMINED_YES',\
                                          prettyName = 'GitHub Determined Yes'))
            self.session.commit()

    def readme(self, owner, repo):
        """
        Determines whether a given repository has a Readme file
        and record the result in the Bossdi database.

        :param owner: The name of the Project owner.
        :param repo: The name of the repo
        :return: DataFrame with the result
        """
        
        # url = "http://api.github.com/repos/{}/{}/readme".format\
        #       (owner, repo)
        # data = requests.get(url, auth=('user', self.GITHUB_API_KEY)).json()

        data = get_data(self, owner, repo)

        exists = self.session.query(self.session.query(Projects).filter_by\
                                   (repo_name = repo).exists()).scalar()

        if data['content'] != None:
            if not exists:
                self.session.add(Projects(repo_owner = owner, repo_name = repo, readme_state = 2))
                self.session.commit()
            else:
                repo_object = self.session.query(Projects).filter_by(repo_name = repo).first()
                repo_object.readme_state = 2
                self.session.commit()   
        else:
            if not exists:
                self.session.add(Projects(repo_owner = owner, repo_name = repo, readme_state = 1))
                self.session.commit()
            else:
                repo_object = self.session.query(Projects).filter_by(repo_name = repo).first()
                repo_object.readme_state = 1
                self.session.commit()

