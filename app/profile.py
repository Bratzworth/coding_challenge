from collections import defaultdict

from flask import jsonify

class OrganizationProfile:
    """
    Class to hold all the relevant profile information from a given git SVN host
    """
    def __init__(self, repos: int = 0, forks: int = 0, watchers: int = 0, languages: defaultdict = defaultdict(int, {}), topics: defaultdict = defaultdict(int, {})):
        """
        Initializes an OrganizationProfile object

        :optional param repos: number of public repos
        :optional param forks: number of forked repos
        :optional param watchers: number of watchers
        :optional param languages: count of each repo language
        :optional param topics: count of each repo topic
        :returns: an OrganizationProfile object
        """
        self.repos = repos
        self.forks = forks
        self.watchers = watchers
        self.languages = languages
        self.topics = topics

    def __add__(self, other):
        """
        Adds two OrganizationProfile objects together by aggregating their values
        """
        repos = self.repos + other.repos
        forks = self.forks + other.forks
        watchers = self.watchers + other.watchers

        # merge count from languages field, only using initialized values
        languages = defaultdict(int)
        for profile in [self, other]:
            if profile.languages != defaultdict(int, {}):
                for language, count in profile.languages.items():
                    languages[language] += count

        # merge count from topics field, only using initialized values
        topics = defaultdict(int)
        for profile in [self, other]:
            if profile.topics != defaultdict(int, {}):
                for topic, count in profile.topics.items():
                    topics[topic] += count
        
        return OrganizationProfile(repos, forks, watchers, languages, topics)

    def dict(self) -> dict:
        """
        Converts the profile data to a pretty-printable dict
        
        :returns: a dict object with all of the formatted data
        """
        profile_dict = {"repos": self.repos, "forks": self.forks, "watchers": self.watchers, 
            "languages": dict(self.languages or {}), "topics": dict(self.topics or {})}
        return profile_dict
