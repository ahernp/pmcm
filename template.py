import markdown
import os
import re

from constants import PAGES_PATH
from history import format_history, read_history

SCRIPT = """<script type="text/javascript">
    $(document).ready(function() {
        $.fancybox.defaults.loop = true;
        $("a:has(img)").not("#logo").attr({"data-fancybox": "gallery", "data-caption": function(i, val) {return $(this).children("img:first").attr("title")}});
        $('table').not('.non-datatable').DataTable({"aaSorting": []});
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
        "version": "0.6.0",
        "history": format_history(read_history()),
        "content": "",
        "script": SCRIPT,
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
