from rdflib import Graph, Namespace, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD
from pathlib import Path
from .utils.io import load_yaml, write_text

SH = Namespace('http://www.w3.org/ns/shacl#')

def build(model_dir: str, out_path: str):
    prefixes = load_yaml(f"{model_dir}/prefixes.yaml")
    props = load_yaml(f"{model_dir}/properties.yaml")

    g = Graph()
    for k,v in prefixes['prefixes'].items():
        g.bind(k, v)
    g.bind('sh', SH)

    # Node shapes per domain class
    domains_by_prop = {}
    for p in props:
        for d in p.get('domain', []):
            domains_by_prop.setdefault(d, []).append(p)

    for cls_qname, props_for_class in domains_by_prop.items():
        ns, local = cls_qname.split(':',1) if ':' in cls_qname else (None, cls_qname)
        class_uri = URIRef(prefixes['prefixes'][ns] + local) if ns else URIRef(cls_qname)
        shape_uri = URIRef(str(class_uri) + "Shape")
        g.add((shape_uri, RDF.type, SH.NodeShape))
        g.add((shape_uri, SH.targetClass, class_uri))

        for p in props_for_class:
            p_ns, p_local = p['id'].split(':',1) if ':' in p['id'] else (None, p['id'])
            prop_uri = URIRef(prefixes['prefixes'][p_ns] + p_local) if p_ns else URIRef(p['id'])

            ps = URIRef(str(shape_uri) + "#" + p_local)
            g.add((shape_uri, SH.property, ps))
            g.add((ps, SH.path, prop_uri))

            for r in p.get('range', []):
                if r.startswith("xsd:"):
                    g.add((ps, SH.datatype, URIRef(prefixes['prefixes']['xsd'] + r.split(':',1)[1])))
                else:
                    r_ns, r_local = r.split(':',1) if ':' in r else (None, r)
                    r_uri = URIRef(prefixes['prefixes'][r_ns] + r_local) if r_ns else URIRef(r)
                    g.add((ps, SH['class'], r_uri))

            cons = p.get('constraints', {})
            if 'minCount' in cons:
                g.add((ps, SH.minCount, Literal(int(cons['minCount']))))
            if 'pattern' in cons:
                g.add((ps, SH.pattern, Literal(cons['pattern'])))

    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    write_text(out_path, g.serialize(format='turtle'))
    return True
