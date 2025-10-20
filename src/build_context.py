from .utils.io import load_yaml, write_json

def build(model_dir: str, out_path: str):
    pfx = load_yaml(f"{model_dir}/prefixes.yaml")['prefixes']
    ctx = {k: v for k,v in pfx.items()}
    write_json(out_path, {"@context": ctx})
    return True
