"""Misc. tests that don't fit anywhere.

XXX: Try our best to reduce tests in this file.
"""
from pipenv.project import Project


import pytest


@pytest.mark.code
@pytest.mark.install
@pytest.mark.skip(reason='non deterministic')
def test_code_import_manual(PipenvInstance):
    with PipenvInstance(chdir=True) as p:
        with open('t.py', 'w') as f:
            f.write('import requests')
        p.pipenv('install -c .')
        assert 'requests' in p.pipfile['packages']


@pytest.mark.lock
@pytest.mark.deploy
@pytest.mark.cli
def test_deploy_works(PipenvInstance, pypi):

    with PipenvInstance(pypi=pypi) as p:
        with open(p.pipfile_path, 'w') as f:
            contents = """
[packages]
requests = "==2.14.0"
flask = "==0.12.2"
[dev-packages]
pytest = "==3.1.1"
            """.strip()
            f.write(contents)
        c = p.pipenv('install')
        assert c.return_code == 0
        c = p.pipenv('lock')
        assert c.return_code == 0
        with open(p.pipfile_path, 'w') as f:
            contents = """
[packages]
requests = "==2.14.0"
            """.strip()
            f.write(contents)

        c = p.pipenv('install --deploy')
        assert c.return_code > 0
