from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD
from pathlib import Path
from .utils.io import load_yaml, write_text

def _build_prefixes(pfx):
    ns = {}
    for k,v in pfx.items():
        ns[k] = Namespace(v)
    return ns

def build(model_dir: str, out_dir: str):
    prefixes = load_yaml(f"{model_dir}/prefixes.yaml")
    classes = load_yaml(f"{model_dir}/classes.yaml")
    properties = load_yaml(f"{model_dir}/properties.yaml")
    alignments = load_yaml(f"{model_dir}/mappings/alignments.yaml")

    g = Graph()
    ns = _build_prefixes(prefixes['prefixes'])
    for k,v in ns.items():
        g.bind(k, v)

    # Ontology header
    base = URIRef(prefixes['baseIRI'])
    g.add((base, RDF.type, OWL.Ontology))
    g.add((base, OWL.versionIRI, URIRef(prefixes['versionIRI'])))
    g.add((base, OWL.versionInfo, Literal(prefixes['version'])))

    # Classes
    for c in classes:
        cid = c['id'].split(':',1)
        uri = ns[cid[0]][cid[1]] if len(cid)==2 else URIRef(c['id'])
        g.add((uri, RDF.type, OWL.Class))
        if 'subclassOf' in c:
            for sc in c['subclassOf']:
                scid = sc.split(':',1)
                suri = ns[scid[0]][scid[1]] if len(scid)==2 else URIRef(sc)
                g.add((uri, RDFS.subClassOf, suri))
        if 'label' in c:
            for lang, val in c['label'].items():
                g.add((uri, RDFS.label, Literal(val, lang=lang)))
        if 'comment' in c:
            for lang, val in c['comment'].items():
                g.add((uri, RDFS.comment, Literal(val, lang=lang)))

    # Properties
    for p in properties:
        pid = p['id'].split(':',1)
        puri = ns[pid[0]][pid[1]] if len(pid)==2 else URIRef(p['id'])
        if p['type'] == 'ObjectProperty':
            g.add((puri, RDF.type, OWL.ObjectProperty))
        else:
            g.add((puri, RDF.type, OWL.DatatypeProperty))
        for d in p.get('domain', []):
            did = d.split(':',1)
            duri = ns[did[0]][did[1]] if len(did)==2 else URIRef(d)
            g.add((puri, RDFS.domain, duri))
        for r in p.get('range', []):
            rid = r.split(':',1)
            ruri = ns[rid[0]][rid[1]] if len(rid)==2 else URIRef(r)
            g.add((puri, RDFS.range, ruri))
        if 'label' in p:
            for lang, val in p['label'].items():
                g.add((puri, RDFS.label, Literal(val, lang=lang)))

    # Alignments
    if alignments:
        for k, arr in alignments.items():
            if k == 'equivalentClass':
                for m in arr:
                    s = m['source'].split(':',1); t = m['target'].split(':',1)
                    s_uri = ns[s[0]][s[1]] if len(s)==2 else URIRef(m['source'])
                    t_uri = ns[t[0]][t[1]] if len(t)==2 else URIRef(m['target'])
                    g.add((s_uri, OWL.equivalentClass, t_uri))
            if k == 'equivalentProperty':
                for m in arr:
                    s = m['source'].split(':',1); t = m['target'].split(':',1)
                    s_uri = ns[s[0]][s[1]] if len(s)==2 else URIRef(m['source'])
                    t_uri = ns[t[0]][t[1]] if len(t)==2 else URIRef(m['target'])
                    g.add((s_uri, OWL.equivalentProperty, t_uri))

    Path(out_dir).mkdir(parents=True, exist_ok=True)
    write_text(f"{out_dir}/ontology.ttl", g.serialize(format='turtle'))
    write_text(f"{out_dir}/ontology.owl", g.serialize(format='xml'))
    write_text(f"{out_dir}/ontology.jsonld", g.serialize(format='json-ld', indent=2))
    return True
