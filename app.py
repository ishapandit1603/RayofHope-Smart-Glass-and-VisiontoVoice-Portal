
import sqlite3
from flask import Flask, render_template_string, send_file

app = Flask(__name__)
DB_PATH = "smartlearn.db"

# HTML Templates
home_template = """
<!DOCTYPE html>
<html>
<head>
  <title>SmartLearn Portal</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="container mt-4">
  <h1 class="text-center">SmartLearn Portal</h1>
  <h3 class="mt-4">Select Subject</h3>
  <ul class="list-group">
  {% for subject in subjects %}
    <li class="list-group-item">
      <a href="/subject/{{subject}}">{{subject}}</a>
    </li>
  {% endfor %}
  </ul>
</body>
</html>
"""

subject_template = """
<!DOCTYPE html>
<html>
<head>
  <title>{{subject}} - SmartLearn</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>
<body class="container mt-4">
  <h2>{{subject}} - Learning Materials</h2>
  <a href="/" class="btn btn-secondary mb-3">Back to Home</a>
  <div class="accordion" id="accordionExample">
  {% for row in content %}
    <div class="accordion-item">
      <h2 class="accordion-header" id="heading{{loop.index}}">
        <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{{loop.index}}">
          {{row[2][:50]}}... (Source: {{row[1]}})
        </button>
      </h2>
      <div id="collapse{{loop.index}}" class="accordion-collapse collapse">
        <div class="accordion-body">
          <p>{{row[2][:500]}}...</p>
          <audio controls>
            <source src="/audio/{{row[0]}}" type="audio/mpeg">
          </audio>
        </div>
      </div>
    </div>
  {% endfor %}
  </div>
</body>
</html>
"""

@app.route("/")
def home():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT subject_name FROM LearningContent")
    subjects = [row[0] for row in cur.fetchall()]
    conn.close()
    return render_template_string(home_template, subjects=subjects)

@app.route("/subject/<subject>")
def subject_page(subject):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT content_id, source, extracted_text, audio_file FROM LearningContent WHERE subject_name=?", (subject,))
    content = cur.fetchall()
    conn.close()
    return render_template_string(subject_template, subject=subject, content=content)

@app.route("/audio/<int:content_id>")
def get_audio(content_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT audio_file FROM LearningContent WHERE content_id=?", (content_id,))
    row = cur.fetchone()
    conn.close()
    if row:
        return send_file(row[0], mimetype="audio/mpeg")
    return "Audio not found", 404

if __name__ == "__main__":
    app.run()
