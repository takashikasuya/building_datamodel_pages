# ontology-kit (starter)

人が編集しやすい **YAML/CSV** を「真実の源泉」にして、
プログラムで **RDF/OWL/JSON-LD/SHACL** を生成・検証・公開するためのスターターです。

## 使い方

```bash
pip install -r requirements.txt
python -m src.cli build
python -m src.cli validate-rdf
python -m src.cli validate-shacl
pytest -q
```

生成物は `generated/` 配下に出力されます：

- `ontology.ttl`, `ontology.owl`, `ontology.jsonld`
- `shapes.ttl`
- `context.json`

YAMLは `model/` を編集してください。RDFは自動生成されます。
