import markdown
import re

from history import format_history, read_history

DELIMITERS_LENGTH = 4
MARKDOWN_EXTENSIONS = ["extra", "tables", "toc"]


def template_substitution(template, replacements):
    substitutions = []

    for old_string, new_string in replacements.items():
        starts = [match.start() for match in re.finditer("{{%s}}" % old_string, template)]
        length = len(old_string) + DELIMITERS_LENGTH
        offsets = [(start, start + length) for start in starts]
        for (start, end) in offsets:
            substitutions.append((start, end, new_string))

    substitutions.sort(reverse=True)

    for (start, end, new_string) in substitutions:
        template = template[0:start] + new_string + template[end:]

    return template


def get_template():
    with open("template.html") as templatefile:
        return templatefile.read()


def markdown_to_html(content):
    return markdown.markdown(
        content,
        extensions=MARKDOWN_EXTENSIONS,
        safe_mode=False,
    )


def populate_context(kwargs):
    context = {
        "title": "",
        "mainmenu": markdown_to_html(read_main_menu()),
        "mainmenu-extra": "",
        "version": "0.1.0",
        "history": format_history(read_history()),
        "content": "",
        "scripts-extra": "",
    }
    return {**context, **kwargs}


def read_main_menu():
    try:
        with open("data/pages/main-menu") as pagefile:
            return pagefile.read()
    except IOError:
        return ""
