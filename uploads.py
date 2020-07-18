from datetime import datetime
import os

from constants import MEDIA_ROOT
from template import get_template, populate_context

UPLOADS_TEMPLATE = """<form action="/uploads/" method="post" enctype="multipart/form-data">
    <label for="content">Upload file:</label>
    <input type="file" name="newFile" required />
    <label for="dir">Directory:</label>
    <select name="dir">
        <option value="img">img</option>
        <option value="code">code</option>
        <option value="doc">doc</option>
        <option value="thumb">thumb</option>
    </select>
    <button type="submit">Upload</button>
</form>
<h2>Uploaded Files</h2>
<table>
    <thead><tr><th>File</th><th>Dir</th><th>Updated</th></tr></thead>
    <tbody>{upload_rows}</tbody>
</table>"""

UPLOAD_ROW = """<tr>
    <td><a href="/media/{dir}/{name}">{name}</a></td>
    <td>{dir}</td>
    <td>{modified_time}</td>
</tr>"""

UPLOAD_DIRS = ["img", "code", "doc", "thumb"]


def view_uploads():
    template = get_template()
    upload_rows = ""
    for directory in UPLOAD_DIRS:
        directory_path = os.path.join(MEDIA_ROOT, directory)
        filenames = os.listdir(directory_path)
        filenames.sort()
        for filename in filenames:
            mtime = os.path.getmtime(os.path.join(directory_path, filename))
            modified_time = datetime.fromtimestamp(mtime).isoformat()
            upload_rows += UPLOAD_ROW.format(
                dir=directory, name=filename, modified_time=modified_time
            )
    context = populate_context(
        {
            "title": "Sitemap",
            "content": UPLOADS_TEMPLATE.format(upload_rows=upload_rows),
        }
    )
    return template.format(**context)


def file_upload(directory, filename, data):
    with open(os.path.join(MEDIA_ROOT, directory, filename), "wb") as uploadfile:
        uploadfile.write(data)
