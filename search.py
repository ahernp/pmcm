import os
import re

from constants import PAGES_PATH
from template import get_template, populate_context, template_substitution

SEARCH_TEMPLATE = """<h1>Search Results</h1>
<p>Page matches for "{{search_term}}":</p>
<ul>
    {{name_matches}}
    {{content_matches}}
</ul>"""

NAME_MATCHES = """<li>Names ({{number_name_matches}} found):
        <ul>{{name_match_rows}}</ul></li>"""

NAME_MATCH_ROW = """<li><a href="/pages/{{name}}">{{name}}</a></li>"""

CONTENT_MATCHES = """<li>Content ({{number_content_pages}} found):
        <ul>{{content_match_rows}}</ul></li>"""

CONTENT_MATCH_ROW = """<li>
    <a href="/pages/{{name}}">{{name}}</a>
    ({{number_content_matches}}):<br>
    {{content}}</li>"""

page_cache = {}


def populate_page_cache():
    filenames = os.listdir(PAGES_PATH)
    for filename in filenames:
        with open(os.path.join(PAGES_PATH, filename)) as pagefile:
            page_cache[filename] = pagefile.read()


def search(search_term):
    def find_name_matches(regex, filenames):
        name_match_rows = []
        for filename in filenames:
            match = regex.search(filename)
            if match:
                name_match_rows.append(
                    template_substitution(NAME_MATCH_ROW, {"name": filename})
                )
        return template_substitution(
            NAME_MATCHES,
            {
                "number_name_matches": str(len(name_match_rows)),
                "name_match_rows": "\n".join(name_match_rows),
            },
        )

    def find_content_matches(regex):
        content_matches = []
        for filename, content in page_cache.items():
            match = regex.search(content)
            if match:
                prev_line_end_pos = content.rfind("\n", 0, match.start())
                if prev_line_end_pos == -1:
                    prev_line_end_pos = 0
                next_line_end_pos = content.find("\n", match.end())
                if next_line_end_pos == -1:
                    next_line_end_pos = len(content)
                content_matches.append(
                    {
                        "content": f"{content[prev_line_end_pos:match.start()]}<b>{content[match.start():match.end()]}</b>{content[match.end():next_line_end_pos]}",
                        "name": filename,
                        "number_content_matches": str(len(regex.findall(content))),
                    }
                )

        content_matches.sort(key=lambda item: item["name"])
        content_matches.sort(
            key=lambda item: item["number_content_matches"], reverse=True
        )

        content_match_rows = ""
        for content_match in content_matches:
            content_match_rows += template_substitution(
                CONTENT_MATCH_ROW, content_match
            )

        return template_substitution(
            CONTENT_MATCHES,
            {
                "number_content_pages": str(len(content_matches)),
                "content_match_rows": content_match_rows,
            },
        )

    regex = re.compile(search_term, re.IGNORECASE)
    template = get_template()
    filenames = os.listdir(PAGES_PATH)
    filenames.sort()
    name_matches = find_name_matches(regex, filenames)
    content_matches = find_content_matches(regex)

    context = populate_context(
        {
            "searchterm": f'value="{search_term}"',
            "title": "Search Results",
            "content": template_substitution(
                SEARCH_TEMPLATE,
                {
                    "search_term": search_term,
                    "name_matches": name_matches,
                    "content_matches": content_matches,
                },
            ),
        }
    )

    return template_substitution(template, context)


populate_page_cache()
