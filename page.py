from history import update_history
from template import get_template, markdown_to_html, populate_context, template_substitution

EDIT_MAINMENU_EXTRA = """<hr>
<p><a href="/pages/{{name}}">View</a></p>
<p><a href="/pages/markdown">Markdown</a></p>"""

EDIT_TEMPLATE = """<form action="/save/{{name}}" method="POST" class="pure-form pure-form-stacked">
    <label for="content">Edit Markdown content</label>
    <textarea name="content" rows="20" cols="60">{{content}}</textarea>
    <button type="submit" class="pure-button pure-button-primary">Save</button>
</form>"""

VIEW_MAINMENU_EXTRA = """<hr>
<p><a href="/edit/{{name}}">Edit</a></p>
<hr>
<button title="Toggle display of page Table of Contents" onClick="$('div.toc').toggle()" class="pure-button">ToC</button>"""


def read_page(name):
    with open(f"data/pages/{name}") as pagefile:
        return pagefile.read()


def edit_page(name):
    template = get_template()
    try:
        page_content = read_page(name)
    except IOError as e:
        page_content = ""
    context = populate_context({
        "title": name,
        "content": template_substitution(EDIT_TEMPLATE, {"name": name, "content": page_content}),
        "mainmenu-extra": template_substitution(EDIT_MAINMENU_EXTRA, {"name": name}),
    })
    html = template_substitution(template, context)
    return html


def view_page(name):
    try:
        template = get_template()
        page_content = read_page(name)
        update_history(name)
        context = populate_context({
            "title": name,
            "content": markdown_to_html("[TOC]\n" + page_content),
            "mainmenu-extra": template_substitution(VIEW_MAINMENU_EXTRA, {"name": name}),
        })
        html = template_substitution(template, context)
        return html
    except IOError as e:
        return edit_page(name)

def save_page(name, content):
    with open(f"data/pages/{name}", "w") as pagefile:
        pagefile.write(content)
