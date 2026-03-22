from flask import Flask, request, redirect
import os

app = Flask(__name__)

LOG_FILE = "log.txt"

# Criar ficheiro se não existir
if not os.path.exists(LOG_FILE):
    open(LOG_FILE, "w").close()


def sanitize(text):
    """Remove caracteres perigosos"""
    return text.replace("<", "").replace(">", "")


def load_posts():
    """Lê posts do ficheiro"""
    posts = []
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            parts = line.strip().split("|||")
            if len(parts) == 2:
                posts.append((parts[0], parts[1]))
    return posts


def save_post(url, message):
    """Guarda novo post"""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{url}|||{message}\n")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = sanitize(request.form.get("url", ""))
        message = sanitize(request.form.get("message", ""))

        if url and message:
            save_post(url, message)

        return redirect("/")

    posts = load_posts()

    # HTML direto (simples)
    html = """
    <html>
    <head>
        <title>Blog Simples</title>
        <style>
            body {
                background-color: black;
                color: white;
                font-family: Arial;
                margin: 20px;
            }
            textarea, input {
                width: 100%;
                background: #111;
                color: white;
                border: 1px solid #555;
                padding: 10px;
                margin-top: 5px;
            }
            button {
                margin-top: 10px;
                padding: 10px;
                background: #333;
                color: white;
                border: none;
                cursor: pointer;
            }
            hr {
                border: 1px solid #444;
            }
        </style>
    </head>
    <body>

        <h2>Deixar mensagem</h2>
        <form method="POST">
            <label>Endereço (URL):</label>
            <input type="text" name="url" required>

            <label>Mensagem:</label>
            <textarea name="message" rows="4" required></textarea>

            <button type="submit">Submit</button>
        </form>

        <hr>

        <h2>Mensagens</h2>
    """

    # Adicionar posts
    for url, msg in reversed(posts):
        html += f"""
        <div>
            <b>{url}</b><br>
            <p>{msg}</p>
        </div>
        <hr>
        """

    html += "</body></html>"

    return html


if __name__ == "__main__":
    app.run(debug=True)
