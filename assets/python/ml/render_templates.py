from typing import Any
import textwrap

import jinja2.ext
import yaml
import black

MAX_CHARACTERS = 120


def comment_box(value: str, documentation_box_common_text: str = "", maxlength: int = int(MAX_CHARACTERS // 2)) -> str:
    """
    Creates a comment box around a bunch of lines, up to a max length.

    Args:
        value: The actual value to be templated
        documentation_box_common_text: Boilerplate that goes at the bottom of every comment box
        maxlength: Maximum column width for the text box

    Returns:
        A nicely-formatted text box
        # --------- #
        # like this #
        # --------- #
    """
    result = ""

    # Format the actual content
    wrapped_content = textwrap.wrap(value, width=maxlength)
    content_lines = (f"# {line.ljust(maxlength)} #" for line in wrapped_content)

    # Format the boilerplate
    if documentation_box_common_text:
        # Convert n-spaced to single space strings
        single_spaced_boilerplate = " ".join(documentation_box_common_text.split())
        wrapped_boilerplate = textwrap.wrap(single_spaced_boilerplate, width=maxlength)
        boilerplate_lines = (f"# {line.ljust(maxlength)} #" for line in wrapped_boilerplate)

    # Blank line, offset 2
    blank_line = f"# {' '.ljust(maxlength)} #"

    # The "#-----#' line
    comment_bound = bot_line = f"# {'-' * maxlength} #"

    result += comment_bound + "\n"  # Top comment line
    result += "\n".join(content_lines) + "\n"
    result += blank_line + "\n"
    if documentation_box_common_text:
        result += "\n".join(boilerplate_lines) + "\n"
    result += comment_bound + "\n"  # Bottom comment line
    return result


def is_yaml_string_list_dict_or_tuple(value: Any) -> bool:
    """
    Checks whether a string in YAML represents a list, dict, or tuple.

    Args:
        value:

    Returns:

    """
    enclosing_characters = {
        "(": ")",
        "[": "]",
        "{": "}",
    }
    if isinstance(value, str) and value[0] in enclosing_characters.keys():
        ending = enclosing_characters[value[0]]
        if value.endswith(ending):
            result = True
        else:
            result = False
    else:
        result = False
    return result


def generate_nonetype(value: Any) -> Any:
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


def quoted_strings(value: Any) -> Any:
    """
    Filter to ensure strings are surrounded in quotes in Jinja templating.

    Args:
        value: The value to be adjusted.

    Returns:
        A string wrapped in quotes, if a string was passed in. Otherwise none.
    """
    if isinstance(value, str) and not is_yaml_string_list_dict_or_tuple(value):
        result = f'"{value}"'
    else:
        result = value
    return result


if __name__ == "__main__":
    # Load general configuration
    with open("config.yaml", "r") as inp:
        config = yaml.safe_load(inp)

    # Tell Jinja where our templates are located
    loader = jinja2.FileSystemLoader('templates/')

    # Populate the Jinja environment with our defined filters
    env = jinja2.Environment(autoescape=True, loader=loader)
    env.filters['quoted_strings'] = quoted_strings
    env.filters['generate_nonetype'] = generate_nonetype
    env.filters['comment_box'] = comment_box
    env.add_extension(jinja2.ext.do)

    # Deal with model templates
    template_type = "model"
    template = env.get_template(f'{template_type}.pyi')

    with open(f"{template_type}.yaml", "r") as inp:
        models = tuple(yaml.safe_load_all(inp))

    for model in models:
        filename = f"pyml:{template_type}:{model['name']}_{model['category']}:{model['provider']}.pyi"
        print(filename)
        with open(filename, "w") as outp:
            outp.write(
                # Ensure pep8 compliance with Black
                black.format_str(template.render(**model, **config),
                                 mode=black.Mode(target_versions={black.TargetVersion.PY36,
                                                                  black.TargetVersion.PY37,
                                                                  black.TargetVersion.PY38},
                                                 line_length=MAX_CHARACTERS,
                                                 string_normalization=False,
                                                 is_pyi=False)
                                 )
            )
