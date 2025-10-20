import subprocess, sys, os, pathlib

def run(cmd):
    assert subprocess.call(cmd, shell=True) == 0

def test_build_and_validate():
    # Build
    run('python -m src.cli build')
    assert pathlib.Path('generated/ontology.ttl').exists()
    assert pathlib.Path('generated/shapes.ttl').exists()
    # Validate
    run('python -m src.cli validate-rdf')
    run('python -m src.cli validate-shacl')
