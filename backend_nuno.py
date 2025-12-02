from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import date, timedelta
import requests
import csv
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 👉 LINK CSV DA TUA GOOGLE SHEET (já convertido para CSV)
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRKUNPk2FnssvdL0sPFTIVudchDX4X--_mhp5TXTqRqBiA2WmjQL2Kf0FMT_xE-Fv5i9R_7ttJUYygL/pub?gid=0&single=true&output=csv"


def carregar_jogos_google_sheets():
    """Lê todos os jogos da Google Sheet e devolve uma lista de dicionários no formato do painel."""
    resp = requests.get(SHEET_CSV_URL, timeout=10)
    resp.raise_for_status()

    csv_text = resp.text
    f = io.StringIO(csv_text)
    reader = csv.DictReader(f)

    jogos = []

    for row in reader:
        # Ignorar linhas sem equipas
        if not row.get("home") or not row.get("away"):
            continue

        def to_float(v):
            v = (v or "").strip()
            try:
                return float(v) if v != "" else None
            except ValueError:
                return None

        jogos.append(
            {
                "date": row.get("date", "").strip(),
                "league": row.get("league", "").strip(),
                "home": row.get("home", "").strip(),
                "away": row.get("away", "").strip(),
                "odd1": to_float(row.get("odd1")),
                "oddX": to_float(row.get("oddX")),
                "odd2": to_float(row.get("odd2")),
                "tipMain": row.get("tipMain", "").strip(),
                "oddMain": to_float(row.get("oddMain")),
                "bttsTip": (row.get("bttsTip") or "").strip() or None,
                "bttsOdd": to_float(row.get("bttsOdd")),
                "ouTip": (row.get("ouTip") or "").strip() or None,
                "ouOdd": to_float(row.get("ouOdd")),
                "source": row.get("source", "").strip(),
            }
        )

    return jogos


@app.get("/")
def root():
    return {
        "message": "Backend Nuno OK",
        "endpoints": ["/api/jogos-hoje", "/api/jogos-amanha"],
    }


@app.get("/api/jogos-hoje")
def jogos_hoje():
    hoje_iso = date.today().isoformat()
    todos = carregar_jogos_google_sheets()
    jogos_hoje = [j for j in todos if j["date"] == hoje_iso]
    return jogos_hoje


@app.get("/api/jogos-amanha")
def jogos_amanha():
    amanha_iso = (date.today() + timedelta(days=1)).isoformat()
    todos = carregar_jogos_google_sheets()
    jogos_amanha = [j for j in todos if j["date"] == amanha_iso]
    return jogos_amanha
