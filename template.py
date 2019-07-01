import markdown
import os
import re

from constants import PAGES_PATH
from history import format_history, read_history

BASE_TEMPLATE = "template.html"
DELIMITERS_LENGTH = 4
MARKDOWN_EXTENSIONS = ["extra", "tables", "toc"]


def template_substitution(template, replacements):
    substitutions = []

    for old_string, new_string in replacements.items():
        starts = [
            match.start() for match in re.finditer("{{%s}}" % old_string, template)
        ]
        length = len(old_string) + DELIMITERS_LENGTH
        offsets = [(start, start + length) for start in starts]
        for (start, end) in offsets:
            substitutions.append((start, end, new_string))

    substitutions.sort(reverse=True)

    for (start, end, new_string) in substitutions:
        template = template[0:start] + new_string + template[end:]

    return template


def get_template():
    with open(BASE_TEMPLATE) as templatefile:
        return templatefile.read()


def markdown_to_html(content):
    return markdown.markdown(content, extensions=MARKDOWN_EXTENSIONS, safe_mode=False)


def populate_context(kwargs):
    context = {
        "title": "",
        "mainmenu": markdown_to_html(read_main_menu()),
        "mainmenu-extra": "",
        "version": "0.5.0",
        "history": format_history(read_history()),
        "content": "",
        "scripts-extra": "",
        "searchterm": "",
    }
    return {**context, **kwargs}


def read_main_menu():
    try:
        with open(os.path.join(PAGES_PATH, "main-menu")) as pagefile:
            return pagefile.read()
    except IOError:
        return ""
