from datetime import datetime
import os

from constants import PAGES_PATH
from template import get_template, populate_context, template_substitution

SITEMAP_TEMPLATE = """<table>
    <thead>
        <tr>
            <th>Page</th>
            <th>Updated</th>
        </tr>
    </thead>
    <tbody>
        {{sitemap_rows}}
    </tbody>
</table>"""

SITEMAP_ROW = """<tr>
        <td><a href="/pages/{{name}}">{{name}}</a></td>
        <td>{{modified_time}}</td>
    </tr>"""


def site_map():
    template = get_template()
    filenames = os.listdir(PAGES_PATH)
    filenames.sort()
    sitemap_rows = ""
    for filename in filenames:
        mtime = os.path.getmtime(os.path.join(PAGES_PATH, filename))
        modified_time = datetime.fromtimestamp(mtime).isoformat()
        sitemap_rows += template_substitution(
            SITEMAP_ROW, {"name": filename, "modified_time": modified_time}
        )
    context = populate_context(
        {
            "title": "Sitemap",
            "content": template_substitution(
                SITEMAP_TEMPLATE, {"sitemap_rows": sitemap_rows}
            ),
        }
    )
    return template_substitution(template, context)
