from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import date, timedelta
import requests
import csv
import io
def ai_predict_from_last5(game: dict) -> dict:
    """
    IA baseada nos últimos 5 jogos de casa e fora.
    Não usa API externa (versão grátis).
    """
    gf_home = game.get("home_last5_gf", 0) or 0
    ga_home = game.get("home_last5_ga", 0) or 0
    gf_away = game.get("away_last5_gf", 0) or 0
    ga_away = game.get("away_last5_ga", 0) or 0
    btts_home = game.get("home_last5_btts", 0) or 0
    btts_away = game.get("away_last5_btts", 0) or 0

    # Médias por jogo
    home_avg_gf = gf_home / 5
    home_avg_ga = ga_home / 5
    away_avg_gf = gf_away / 5
    away_avg_ga = ga_away / 5

    # ---------- IA TIP 1X2 ----------
    if home_avg_gf - away_avg_gf > 0.6 and home_avg_ga <= away_avg_ga + 0.2:
        ai_tip_main = "1"
    elif away_avg_gf - home_avg_gf > 0.6 and away_avg_ga <= home_avg_ga + 0.2:
        ai_tip_main = "2"
    else:
        ai_tip_main = "X"

    # ---------- BTTS ----------
    btts_total = btts_home + btts_away  # 0–10
    if btts_total >= 6:
        ai_btts = "Sim"
    elif btts_total <= 3:
        ai_btts = "Não"
    else:
        ai_btts = "Indefinido"

    # ---------- OVER/UNDER ----------
    soma_medias = home_avg_gf + away_avg_gf
    if soma_medias >= 3:
        ai_ou = "Over 2.5"
    elif soma_medias <= 2:
        ai_ou = "Under 2.5"
    else:
        ai_ou = "Neutro"

    # ---------- CONFIANÇA (0–10) ----------
    confiança = 5
    if ai_tip_main in ("1", "2") and abs(home_avg_gf - away_avg_gf) > 0.8:
        confiança += 2
    if ai_btts in ("Sim", "Não") and btts_total >= 7:
        confiança += 1
    if ai_ou in ("Over 2.5", "Under 2.5") and abs(soma_medias - 2.5) > 0.8:
        confiança += 1

    confiança = max(1, min(10, confiança))

    comentario = (
        f"IA: Casa {gf_home}-{ga_home} golos nos últimos 5; "
        f"Fora {gf_away}-{ga_away}; BTTS total {btts_total}/10."
    )

    return {
        "aiTipMain": ai_tip_main,
        "aiBTTS": ai_btts,
        "aiOU": ai_ou,
        "aiConfidence": confiança,
        "aiComment": comentario,
    }
    ...
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
