from typing import Any

import jinja2.ext
import yaml
import black


def quoted_strings(value: Any) -> Any:
    """
    Filter to ensure strings are surrounded in quotes in Jinja templating.

    Args:
        value: The value to be adjusted.

    Returns:
        A string wrapped in quotes, if a string was passed in. Otherwise none.
    """
    if isinstance(value, str):
        result = f'"{value}"'
    else:
        result = value
    return result


def convert_nonetype(value: Any) -> Any:
    """
    Filter for converting the string "None" to the None literal in Jinja templating.
    Note that the string is converted to title-case before being tested, so any variation of casing works too, such as
    "none," "NONE," "NoNe," etc.

    Args:
        value: The value to be adjusted.

    Returns:
        A literal None if "None" was passed in, otherwise returns the value that was passed in.
    """
    if isinstance(value, str) and value.title() == "None":
        result = None
    else:
        result = value
    return result


if __name__ == "__main__":
    # Tell Jinja where our templates are located
    loader = jinja2.FileSystemLoader('templates/')

    # Populate the Jinja environment with our defined filters
    env = jinja2.Environment(autoescape=True, loader=loader)
    env.filters['quoted_strings'] = quoted_strings
    env.filters['convert_nonetype'] = convert_nonetype
    env.add_extension(jinja2.ext.do)

    # Deal with model templates
    template_type = "model"
    template = env.get_template(f'{template_type}.pyi')

    with open(f"{template_type}.yaml", "r") as inp:
        models = tuple(yaml.safe_load_all(inp))

    for model in models:
        filename = f"pyml:{template_type}:{model['name']}_{model['category']}:{model['provider']}.py"
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
