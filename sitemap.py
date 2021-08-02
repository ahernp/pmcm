from datetime import datetime

from constants import PAGES_PATH
from template import get_template, populate_context

SITEMAP_TEMPLATE = """<table>
    <thead>
        <tr>
            <th>Page</th>
            <th>Updated</th>
        </tr>
    </thead>
    <tbody>
        {sitemap_rows}
    </tbody>
</table>"""

SITEMAP_ROW = """<tr>
        <td><a href="/pages/{name}">{name}</a></td>
        <td>{modified_time}</td>
    </tr>"""


def site_map():
    template = get_template()
    sitemap_rows = ""
    for file_path in PAGES_PATH.iterdir():
        modified_time = datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
        sitemap_rows += SITEMAP_ROW.format(
            name=file_path.name, modified_time=modified_time
        )
    context = populate_context(
        {
            "title": "Sitemap",
            "content": SITEMAP_TEMPLATE.format(sitemap_rows=sitemap_rows),
        }
    )
    return template.format(**context)
