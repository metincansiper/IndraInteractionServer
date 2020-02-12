from indra.assemblers.english import EnglishAssembler
from clare.capabilities.util import get_agent_from_gene_name
from bioagents.msa.msa import MSA
import json

msa = MSA()

def interactionFinder(genes):
    agents = list(map(get_agent_from_gene_name, genes))

    meth='binary_undirected'
    finder = msa.find_mechanisms(meth, *agents)

    stmts = finder.get_statements(block=True)

    dicts = list(map(indraStatementToDict , stmts))
    return dicts

def interactionFinderJsonStr(genes):
    dicts = interactionFinder(genes)
    jsons = json.dumps(dicts)
    return jsons

def indraStatementToDict(stmt):
    ea = EnglishAssembler([stmt])
    txt = ea.make_model()
    pmid = stmt.evidence[0].pmid

    return {'pmid': pmid, 'text': txt}
