import argparse, sys
from .generate_ontology import build as build_onto
from .build_shapes import build as build_shapes
from .build_context import build as build_ctx

def cmd_build(args):
    ok1 = build_onto('model', 'generated')
    ok2 = build_shapes('model', 'generated/shapes.ttl')
    ok3 = build_ctx('model', 'generated/context.json')
    print('Build completed:', ok1 and ok2 and ok3)

def cmd_lint_models(args):
    from .utils.io import load_yaml
    try:
        for f in ['prefixes.yaml','classes.yaml','properties.yaml']:
            _ = load_yaml(f'model/{f}')
        print('Model YAML loaded OK')
    except Exception as e:
        print('YAML load error:', e)
        sys.exit(1)

def cmd_validate_rdf(args):
    try:
        from rdflib import Graph
        for f in ['generated/ontology.ttl','generated/ontology.owl','generated/ontology.jsonld']:
            g = Graph(); g.parse(f)
        print('RDF parse OK')
    except Exception as e:
        print('RDF parse error:', e)
        sys.exit(1)

def cmd_validate_shacl(args):
    try:
        from pyshacl import validate
        from rdflib import Graph
        data_g = Graph(); data_g.parse('generated/ontology.ttl', format='turtle')
        shacl_g = Graph(); shacl_g.parse('generated/shapes.ttl', format='turtle')
        conforms, results_graph, results_text = validate(data_g, shacl_graph=shacl_g, inference='rdfs', abort_on_first=False, meta_shacl=False, advanced=True)
        print('SHACL on ontology itself:', conforms)
        print(results_text)
        if not conforms:
            sys.exit(1)
    except Exception as e:
        print('SHACL error:', e)
        sys.exit(1)

def cmd_docs(args):
    from .build_docs import build as build_docs
    # ensure latest ontology exists
    build_onto('model', 'generated')
    build_docs('generated/ontology.ttl', 'generated/docs')
    print('Docs generated at generated/docs/index.html')

def main():
    p = argparse.ArgumentParser(prog='ontology-kit')
    sub = p.add_subparsers()

    b = sub.add_parser('build'); b.set_defaults(func=cmd_build)
    l = sub.add_parser('lint-models'); l.set_defaults(func=cmd_lint_models)
    r = sub.add_parser('validate-rdf'); r.set_defaults(func=cmd_validate_rdf)
    s = sub.add_parser('validate-shacl'); s.set_defaults(func=cmd_validate_shacl)
    d = sub.add_parser('docs'); d.set_defaults(func=cmd_docs)

    args = p.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        p.print_help()

if __name__ == '__main__':
    main()
