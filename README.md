# ontology-kit (starter with local HTML docs)

人が編集しやすい **YAML/CSV** を「真実の源泉」にして、
プログラムで **RDF/OWL/JSON-LD/SHACL** を生成・検証し、
さらに **pyLODE** により **ローカルで単一HTMLのドキュメント生成** を行うスターターです。

## セットアップ
```bash
pip install -r requirements.txt
```

## 生成 & 検証 & ドキュメント
```bash
python -m src.cli build
python -m src.cli validate-rdf
python -m src.cli validate-shacl
python -m src.cli docs   # → generated/docs/index.html
```

## Makefile も利用可
```bash
make build
make validate
make docs
```
