import subprocess, pathlib

def run(cmd):
    assert subprocess.call(cmd, shell=True) == 0

def test_build_validate_docs():
    run('python -m src.cli build')
    assert pathlib.Path('generated/ontology.ttl').exists()
    run('python -m src.cli validate-rdf')
    run('python -m src.cli validate-shacl')
    run('python -m src.cli docs')
    assert pathlib.Path('generated/docs/index.html').exists()
