import os

defaults = {
  'HOST': '127.0.0.1',
  'PORT': 8000,
  'INDRA_GROUND_URL': 'http://grounding.indra.bio/ground'
}

env = os.environ

def read_from_config(_key):
    if _key in env:
        return env[_key]
    if _key in defaults:
        return defaults[_key]

    return None
