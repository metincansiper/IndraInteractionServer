from config import read_from_config

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

def interactionFinder(sources):
    agents = list(map(get_agent, sources))

    meth='binary_undirected'
    finder = msa.find_mechanisms(meth, *agents)

    stmts = finder.get_statements(block=True)

    dicts = list(map(indraStatementToDict , stmts))
    return dicts

def interactionFinderJsonStr(sources):
    dicts = interactionFinder(sources)
    jsons = json.dumps(dicts)
    return jsons

def indraStatementToDict(stmt):
    ea = EnglishAssembler([stmt])
    txt = ea.make_model()
    pmid = stmt.evidence[0].pmid

    return {'pmid': pmid, 'text': txt}
