import logging

from app import parsers

import flask
from flask import Response, jsonify

app = flask.Flask("user_profiles_api")
logger = flask.logging.create_logger(app)
logger.setLevel(logging.INFO)

#{dde490aa-a2db-40cb-81ca-99fd1f52b0ca} <- team name to test multiple pages of repos

@app.route("/profile", methods=["GET"])
def profile():
    """
    Endpoint to get unified profile from github and bitbucket
    """
    app.logger.info(f"Parsed bitbucket team as {flask.request.args.get('bitbucket-team')}")
    app.logger.info(f"Parsed github organization as {flask.request.args.get('github-org')}")

    try:
        bitbucket = parsers.parse_bitbucket(flask.request.args.get("bitbucket-team"))
        github = parsers.parse_github(flask.request.args.get("github-org"))
    except ConnectionError as e:
        return Response(str(e), status=500)
     
    return jsonify((bitbucket + github).dict())

@app.route("/health-check", methods=["GET"])
def health_check():
    """
    Endpoint to health check API
    """
    app.logger.info("Health Check!")
    return Response("All Good!", status=200)
