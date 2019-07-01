from datetime import datetime
import os

from template import get_template, populate_context, template_substitution

UPLOADS_TEMPLATE = """<form action="/uploads/" method="post" class="pure-form" enctype="multipart/form-data">
    <label for="content">Upload file:</label>
    <input type="file" name="newFile" />
    <label for="dir">Directory:</label>
    <select name="dir">
        <option value="img">img</option>
        <option value="code">code</option>
        <option value="doc">doc</option>
        <option value="thumb">thumb</option>
    </select>
    <button type="submit" class="pure-button pure-button-primary">Upload</button>
</form>
<h2>Uploaded Files</h2>
<table>
    <thead><tr><th>File</th><th>Dir</th><th>Updated</th></tr></thead>
    <tbody>{{upload_rows}}</tbody>
</table>"""

UPLOAD_ROW = """<tr>
    <td><a href="/media/{{dir}}/{{name}}">{{name}}</a></td>
    <td>{{dir}}</td>
    <td>{{modified_time}}</td>
</tr>"""

UPLOAD_DIRS = ["img", "code", "doc", "thumb"]

def view_uploads():
    template = get_template()
    upload_rows = ""
    for directory in UPLOAD_DIRS:
        filenames = os.listdir(f"media/{directory}/")
        filenames.sort()
        for filename in filenames:
            mtime = os.path.getmtime(os.path.join(f"media/{directory}/", filename))
            modified_time = datetime.fromtimestamp(mtime).isoformat()
            upload_rows += template_substitution(
                UPLOAD_ROW,
                {"dir": directory, "name": filename, "modified_time": modified_time})
    context = populate_context({
        "title": "Sitemap",
        "content": template_substitution(UPLOADS_TEMPLATE, {"upload_rows": upload_rows}),
    })
    html = template_substitution(template, context)
    return html


def file_upload(directory, filename, data):
    with open(f"media/{directory}/{filename}", "wb") as uploadfile:
        uploadfile.write(data)
