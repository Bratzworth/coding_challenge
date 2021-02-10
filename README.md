# Coding Challenge App

A flask app to aggregate statistics between a bitbucket team and a github organization.

## Install:

You can use a virtual environment (conda, venv, etc):
```
conda env create -f environment.yml
source activate user-profiles
```

Or just pip install from the requirements file
``` 
pip install -r requirements.txt
```

## Running the code
Start up a local server (detailed in the next section)
You can request a unified profile for a given bitbucket team name and github organization name as follows
```
http://127.0.0.1:5000/profile?bitbucket-team={bitbucket team name}&github-org={github organization name}
```

The resulting profile is returned as json with the following format:
```
{
    "forks": int,
    "languages": {},
    "repos": int,
    "topics": {},
    "watchers": int 
}
```

### Spin up the service

```
# start up local server
python3.8 -m run 
```

### Making Requests

```
curl -i "http://127.0.0.1:5000/health-check"
```


## What'd I'd like to improve on...
Ideally more integration tests

## Notes:
Updated flask version to 1.1.2
Updated Werkzeug to 1.0.1
Using python3.8