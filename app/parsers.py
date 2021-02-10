import logging
import asyncio
import operator
from typing import List
from collections import defaultdict

from app import profile

import httpx
import flask

app = flask.Flask("user_profiles_api")
logger = flask.logging.create_logger(app)

async def get_request_json(endpoint: str, headers: dict = {}) -> dict:
    """
    Sends a get request to a given endpoint and returns the response as json
    
    :param endpoint: endpoint to make a get request to
    :param headers: headers to pass to the endpoint for the request
    :returns: json output from the request
    :raises ConnectionError: raises an exception if a valid request could not be sent
    """
    app.logger.debug(f"Sending get request to '{endpoint}' with the following headers: {headers}")
    async with httpx.AsyncClient() as client:
        response = await client.get(endpoint, headers = headers)
        if response.status_code != 200:
            raise ConnectionError("Failed to recieve data from " + endpoint)
        return response.json()

async def get_multiple_json(endpoints: List[str], headers: dict = {}) -> List[dict]:
    """
    Sends a get request to given endpoints and returns the responses as json
    
    :param endpoints: endpoints to make get requests to
    :param headers: headers to pass to the endpoint for the request
    :returns: json output from the request
    :raises ConnectionError: raises an exception if a valid request could not be sent
    """
    responses = []
    for endpoint in endpoints:
        responses.append(get_request_json(endpoint, headers = headers))
    results = await asyncio.gather(*responses)
    return results

def parse_language(entry: str) -> str:
    """
    Converts a string to our unified language format for storage:
        - empty strings are stored as 'none'
        - all strings are converted to lowercase

    :param entry: value to parse
    :returns: modified value that conforms to our styling
    """
    if entry == "" or entry == None:
        return "none"
    return entry.lower()

def parse_bitbucket(team: str) -> profile.OrganizationProfile:
    """
    Requests info from the bitbucket api for a given team to get profile stats:
        - number of public repos
        - count of total followers on all repos
        - count of languages used across all repos
    Bitbucket doesn't have topics, nor does it define if a repo is a fork
    
    :param team: bitbucket team to gather the stats of
    :returns: an OrganizationProfile object that holds all of the gathered statistics
    """
    app.logger.debug(f"parse_bitbucket entered with team name of {team}")
    
    if team is None:
        return profile.OrganizationProfile()

    json = asyncio.run(get_request_json(f"https://api.bitbucket.org/2.0/repositories/{team}"))

    # Get number of public repos (I don't think bitbucket displays if a repo is forked)
    repos = json["size"]

    # Get statistics of repos
    watchers = 0
    languages = defaultdict(int)
    watcher_endpoints = []
    while(True):
        for repo in json["values"]:
            watcher_endpoints.append(repo["links"]["watchers"]["href"])
            languages[parse_language(repo["language"])] += 1
        
        # get number of watchers asynchronously
        results = asyncio.run(get_multiple_json(watcher_endpoints))
        for result in results:
            watchers += result["size"]

        # check if there's another page to request
        if "next" not in json:
            break;
        json = asyncio.run(get_request_json(json["next"]))
    return profile.OrganizationProfile(repos = repos, watchers = watchers, languages = languages)

def parse_github(organization:str) -> profile.OrganizationProfile:
    """
    Requests info from the github api for a given team to get profile stats:
        - number of public repos
        - number of forked repos
        - count of total watchers on all repos
        - count of languages used across all repos
        - count of topics used across all repos

    :param organization: github organization to gather the stats of
    :returns: an OrganizationProfile object that holds all of the gathered statistics
    """
    app.logger.debug(f"parse_github entered with organization name of {organization}")

    if organization is None:
        return profile.OrganizationProfile()

    # send a request w/ header to enable topics since it's in the preview period
    json = asyncio.run(get_request_json(f"https://api.github.com/orgs/{organization}/repos", headers = {"Accept": "application/vnd.github.mercy-preview+json"}))

    # initialize bookkeeping variables
    repos = len(json)
    forks = 0
    watchers = 0
    languages = defaultdict(int)
    topics = defaultdict(int)

    for repo in json:
        # update count of forks vs repos
        if repo["fork"]:
            repos -= 1
            forks += 1
        
        watchers += repo["watchers_count"]

        # github reports language as being "null" for forks of closed repos. we can manually
        # find the language by accessing the languages_url endpoint & sorting for highest
        language = parse_language(repo["language"])
        if language == "none":
            repo_languages = asyncio.run(get_request_json(repo["languages_url"]))
            if len(repo_languages) > 0:
                language = parse_language(max(repo_languages.items(), key=operator.itemgetter(1))[0])
            
        languages[language] += 1

        for topic in repo["topics"]:
            topics[topic] += 1

    return profile.OrganizationProfile(repos, forks, watchers, languages, topics)
