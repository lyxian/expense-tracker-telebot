import yaml
import os

def updateSecretsEnv():
    with open('secrets.yaml', 'r') as file:
        data = {k: str(v) for k,v in yaml.safe_load(file).items()}
    tmpEnv = os.environ.copy()
    return {**tmpEnv, **data}