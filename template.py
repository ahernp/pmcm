import time

import markdown

from constants import PAGES_PATH
from history import format_history, read_history

SCRIPT = """<script type="text/javascript">
    $(document).ready(function() {
        $("a:has(img)").not("#logo").attr({"data-fancybox": "gallery", "data-caption": function(i, val) {return $(this).children("img:first").attr("title")}});
        $('table').not('.non-datatable').DataTable({"order": [[ 0, "asc" ]]});
        hljs.highlightAll();

    });
</script>"""

BASE_TEMPLATE = "template.html"
DELIMITERS_LENGTH = 4
MARKDOWN_EXTENSIONS = ["extra", "tables", "toc"]


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
        "version": "1.0.2",
        "history": format_history(read_history()),
        "content": "",
        "script": SCRIPT,
        "scripts-extra": "",
        "searchterm": "",
        "loadtime": time.strftime("%a %Y-%m-%d %H:%M:%S", time.localtime()),
    }
    return {**context, **kwargs}


def read_main_menu():
    try:
        with open(PAGES_PATH / "main-menu") as pagefile:
            return pagefile.read()
    except IOError:
        return ""
