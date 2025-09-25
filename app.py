from flask import Flask, request, render_template_string, send_file
import pandas as pd
import matplotlib.pyplot as plt

APP_HTML = """
<!doctype html>
<title>TS-NOX-202 (interactivo)</title>
<h1>TS-NOX-202 (interactivo)</h1>
<form method="get" action="/">
  <label>Inicio (YYYY-MM-DD HH:MM): <input name="inicio" value="{{ inicio or '' }}"></label>
  <label>Fin (YYYY-MM-DD HH:MM): <input name="fin" value="{{ fin or '' }}"></label>
  <button type="submit">Generar</button>
</form>
<p>Deja ambos vacíos para usar todo el rango. Abre <a href="/png" target="_blank">/png</a> para ver la imagen.</p>
{% if mensaje %}<pre>{{ mensaje }}</pre>{% endif %}
"""

app = Flask(__name__)

def generar_png(inicio=None, fin=None):
    df = pd.read_csv("data/nox.csv", dtype=str)
    df["ts"] = pd.to_datetime(df["Date.Local"].str.strip()+" "+df["Time.Local"].str.strip(), errors="coerce")
    df["y"] = pd.to_numeric(df["Sample.Measurement"], errors="coerce")
    df = df.dropna(subset=["ts","y"])
    if inicio:
        df = df[df["ts"] >= pd.to_datetime(inicio)]
    if fin:
        df = df[df["ts"] <= pd.to_datetime(fin)]
    agg = df.groupby("ts", as_index=False)["y"].mean()
    plt.figure(figsize=(12,5))
    plt.plot(agg["ts"], agg["y"])
    plt.title("TS-NOX-202")
    plt.xlabel("Tiempo")
    plt.ylabel("Sample.Measurement")
    plt.tight_layout()
    plt.savefig("TS-NOX-202.png", dpi=150)
    plt.close()

@app.route("/", methods=["GET"])
def home():
    inicio = request.args.get("inicio") or None
    fin = request.args.get("fin") or None
    generar_png(inicio, fin)
    msg = f"Rango aplicado: {inicio or '(todo)'} -> {fin or '(todo)'} | PNG actualizado."
    return render_template_string(APP_HTML, inicio=inicio, fin=fin, mensaje=msg)

@app.route("/png")
def png():
    return send_file("TS-NOX-202.png", mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
