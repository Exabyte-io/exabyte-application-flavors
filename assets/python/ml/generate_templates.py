import jinja2
import yaml

loader = jinja2.FileSystemLoader('templates/')

def quoted_strings(value):
    if isinstance(value, str):
        result = f'"{value}"'
    else:
        result = value
    return result

def convert_nonetype(value):
    if isinstance(value, str) and value.title() == "None":
        result = None
    else:
        result = value
    return result

env = jinja2.Environment(autoescape=True, loader=loader)
env.filters['quoted_strings'] = quoted_strings
env.filters['convert_nonetype'] = convert_nonetype

template = env.get_template('model.pyi')

with open("models.yaml", "r") as inp:
    models = tuple(yaml.safe_load_all(inp))

for model in models:
    print(model['default_args'])
    filename = f"pyml:model:{model['name']}:{model['provider']}.py"
    print(filename)
    with open(filename, "w") as outp:
        outp.write(template.render(**model))

