from config import read_from_config
from entity_sign import EntitySign

from indra.assemblers.english import EnglishAssembler
from bioagents.msa.msa import MSA
from indra.statements import Agent
from indra.databases import hgnc_client, chebi_client
from indra.preassembler.grounding_mapper import GroundingMapper

import json
import requests

msa = MSA()

def get_agent(name):
    opts = {'text': name}

    indra_url = read_from_config('INDRA_GROUND_URL')
    res = requests.post(indra_url, json=opts)

    if res.status_code != 200 and not res.json():
        return Agent(name, db_refs={'TEXT': name})

    js = res.json()
    top_term = js[0]['term']

    agent = Agent(name, db_refs={'TEXT': name,
                              top_term['db']: top_term['id']})

    GroundingMapper.standardize_agent_name(agent, standardize_refs=True)
    return agent

def interactionFinder(entities, sign):
    agents = list(map(get_agent, entities))

    # TODO: Does sign parameter needed? Should always use 'binary_undirected'?
    meth = 'binary_undirected' if sign == EntitySign.UNSIGNED else 'binary_directed'
    finder = msa.find_mechanisms(meth, *agents)

    stmts = finder.get_statements(block=True)

    filter_fcn = None

    if sign == EntitySign.UNSIGNED:
        filter_fcn = is_unsigned_stmt
    elif sign == EntitySign.POSITIVE:
        filter_fcn = is_positive_stmt
    elif sign == EntitySign.NEGATIVE:
        filter_fcn = is_negative_stmt

    stmts = filter(filter_fcn, stmts)

    dicts = list(map(indraStatementToDict , stmts))
    return dicts

def interactionFinderJsonStr(entities, sign):
    dicts = interactionFinder(entities, sign)
    jsons = json.dumps(dicts)
    return jsons

def indraStatementToDict(stmt):
    ea = EnglishAssembler([stmt])
    txt = ea.make_model()
    pmid = stmt.evidence[0].pmid
    _type = get_type(stmt)

    return {'pmid': pmid, 'text': txt, 'type': _type}

def is_negative_stmt(stmt):
    return is_negative_stmt_type(get_type(stmt))

def is_positive_stmt(stmt):
    return is_positive_stmt_type(get_type(stmt))

def is_unsigned_stmt(stmt):
    return is_unsigned_stmt_type(get_type(stmt))

# TODO: Revise what is positive/negative/unsigned.
# Current implementations are to be used temporarily.
def is_negative_stmt_type(_type):
    return _type == 'Inhibition'\
            or _type.startswith('De')\
            or _type.startswith('Un')\
            or _type.startswith('Decrease')

def is_unsigned_stmt_type(_type):
    types = ['Complex', 'Association', 'Statement', 'Event']
    return _type in types

def is_positive_stmt_type(_type):
    return not is_negative_stmt_type(_type) and not is_unsigned_stmt_type(_type)


def get_type(o):
    return type(o).__name__
