import jinja2.ext
import yaml
import black

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
env.add_extension(jinja2.ext.do)

template = env.get_template('model.pyi')

with open("models.yaml", "r") as inp:
    models = tuple(yaml.safe_load_all(inp))

for model in models:
    filename = f"pyml:model:{model['name']}_{model['category']}:{model['provider']}.py"
    print(filename)
    with open(filename, "w") as outp:
        outp.write(
            # Ensure pep8 compliance with Black
            black.format_str(template.render(**model),
                             mode=black.Mode(target_versions={black.TargetVersion.PY36,
                                                              black.TargetVersion.PY37,
                                                              black.TargetVersion.PY38},
                                             line_length=120,
                                             string_normalization=False,
                                             is_pyi=False)
                             )
        )
