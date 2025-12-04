from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import date, timedelta
from urllib.request import urlopen
import csv
import io

app = FastAPI()

# CORS – permite que o painel Netlify aceda à API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
#  LINK DA TUA GOOGLE SHEET (versão CSV)
# -------------------------------------------------
GOOGLE_SHEET_CSV_URL = (
    "https://docs.google.com/spreadsheets/d/e/"
    "2PACX-1vRKUNPk2FnssvdL0sPFTIVudchDX4X--_mhp5TXTqRqBiA2WmjQL2Kf0FMT_xE-Fv5i9R_7ttJUYygL"
    "/pub?gid=0&single=true&output=csv"
)


# -------------------------------------------------
#  LER JOGOS DA GOOGLE SHEET
# -------------------------------------------------
def fetch_games_from_sheet(day: date):
    """
    Lê a Google Sheet publicada em CSV, filtra apenas os jogos da data 'day'
    e devolve uma lista de dicionários.
    Espera colunas: date, league, home, away, odd1, oddX, odd2, tipMain, bttsTip, ouTip, ouOdd
    """
    try:
        with urlopen(GOOGLE_SHEET_CSV_URL, timeout=10) as resp:
            raw = resp.read().decode("utf-8")
    except Exception as e:
        print("ERRO AO LER GOOGLE SHEET:", e)
        return []

    reader = csv.DictReader(io.StringIO(raw))
    jogos = []

    for row in reader:
        # data em texto
        raw_date = (row.get("date") or "").strip()
        if not raw_date:
            continue

        # aceitar datas com / ou -
        raw_date = raw_date.replace("/", "-")

        try:
            row_date = date.fromisoformat(raw_date)
        except ValueError:
            # data inválida → ignora
            continue

        # só queremos jogos do dia pedido
        if row_date != day:
            continue

        # helper para converter texto em float
        def to_float(v):
            if v is None:
                return None
            s = str(v).strip().replace(",", ".")
            if not s:
                return None
            try:
                return float(s)
            except ValueError:
                return None

        jogo = {
            "date": row_date.isoformat(),
            "league": (row.get("league") or "").strip(),
            "home": (row.get("home") or "").strip(),
            "away": (row.get("away") or "").strip(),
            "odd1": to_float(row.get("odd1")),
            "oddX": to_float(row.get("oddX")),
            "odd2": to_float(row.get("odd2")),
            "tipMain": (row.get("tipMain") or "").strip(),
            "bttsTip": (row.get("bttsTip") or "").strip(),
            "ouTip": (row.get("ouTip") or "").strip(),
            "ouOdd": to_float(row.get("ouOdd")),
        }

        # ignora linhas sem equipas
        if not jogo["home"] or not jogo["away"]:
            continue

        jogos.append(jogo)

    return jogos


# -------------------------------------------------
#  BASE DE JOGOS MANUAIS (BACKUP)
# -------------------------------------------------
def base_games(day: date):
    """
    Backup manual se a Google Sheet falhar ou estiver vazia.
    """
    iso = day.isoformat()

    return [
        {
            "date": iso,
            "league": "Premier League",
            "home": "Liverpool",
            "away": "Brighton",
            "odd1": 1.55,
            "oddX": 4.30,
            "odd2": 5.80,
            "tipMain": "1",
            "bttsTip": "Sim",
            "ouTip": "Over 2.5",
            "ouOdd": 1.50,
        },
        {
            "date": iso,
            "league": "LaLiga",
            "home": "Barcelona",
            "away": "Real Betis",
            "odd1": 1.40,
            "oddX": 4.80,
            "odd2": 7.50,
            "tipMain": "1",
            "bttsTip": "Sim",
            "ouTip": "Over 2.5",
            "ouOdd": 1.55,
        },
        {
            "date": iso,
            "league": "Serie A",
            "home": "Juventus",
            "away": "Bologna",
            "odd1": 1.85,
            "oddX": 3.40,
            "odd2": 4.20,
            "tipMain": "1",
            "bttsTip": "Não",
            "ouTip": "Under 2.5",
            "ouOdd": 1.75,
        },
        {
            "date": iso,
            "league": "Bundesliga",
            "home": "Borussia Dortmund",
            "away": "Stuttgart",
            "odd1": 1.90,
            "oddX": 3.70,
            "odd2": 3.90,
            "tipMain": "BTTS",
            "bttsTip": "Sim",
            "ouTip": "Over 2.5",
            "ouOdd": 1.55,
        },
        {
            "date": iso,
            "league": "Ligue 1",
            "home": "Marseille",
            "away": "Nice",
            "odd1": 2.05,
            "oddX": 3.20,
            "odd2": 3.60,
            "tipMain": "1X",
            "bttsTip": "Não",
            "ouTip": "Under 2.5",
            "ouOdd": 1.70,
        },
        {
            "date": iso,
            "league": "Primeira Liga",
            "home": "Sporting CP",
            "away": "Guimarães",
            "odd1": 1.45,
            "oddX": 4.30,
            "odd2": 7.00,
            "tipMain": "1",
            "bttsTip": "Sim",
            "ouTip": "Over 2.5",
            "ouOdd": 1.60,
        },
        {
            "date": iso,
            "league": "Eredivisie",
            "home": "Feyenoord",
            "away": "AZ Alkmaar",
            "odd1": 1.75,
            "oddX": 3.80,
            "odd2": 4.00,
            "tipMain": "1",
            "bttsTip": "Sim",
            "ouTip": "Over 2.5",
            "ouOdd": 1.60,
        },
        {
            "date": iso,
            "league": "Championship",
            "home": "Southampton",
            "away": "Cardiff",
            "odd1": 1.65,
            "oddX": 3.90,
            "odd2": 5.20,
            "tipMain": "1",
            "bttsTip": "Não",
            "ouTip": "Under 2.5",
            "ouOdd": 1.85,
        },
        {
            "date": iso,
            "league": "MLS",
            "home": "LA Galaxy",
            "away": "Austin FC",
            "odd1": 1.85,
            "oddX": 3.60,
            "odd2": 4.10,
            "tipMain": "Over 2.5",
            "bttsTip": "Sim",
            "ouTip": "Over 2.5",
            "ouOdd": 1.65,
        },
        {
            "date": iso,
            "league": "Saudi Pro League",
            "home": "Al Nassr",
            "away": "Al Ittihad",
            "odd1": 2.00,
            "oddX": 3.70,
            "odd2": 3.40,
            "tipMain": "BTTS",
            "bttsTip": "Sim",
            "ouTip": "Over 2.5",
            "ouOdd": 1.75,
        },
    ]


# -------------------------------------------------
#  IA SIMPLES PARA CADA JOGO
# -------------------------------------------------
def add_ai_to_games(games):
    jogos = []

    for game in games:
        g = game.copy()

        odd1 = g.get("odd1") or 0
        oddX = g.get("oddX") or 0
        odd2 = g.get("odd2") or 0
        ou_tip = (g.get("ouTip") or "").lower()
        ou_odd = g.get("ouOdd") or 0

        # TIP 1X2 PRINCIPAL (menor odd)
        odds_validas = [v for v in (odd1, oddX, odd2) if v]
        if odds_validas:
            menor = min(odds_validas)
            if menor == odd1:
                ai_main = "1"
            elif menor == oddX:
                ai_main = "X"
            else:
                ai_main = "2"
        else:
            ai_main = "Indefinido"

        # BTTS por cima de OU
        if "over" in ou_tip and ou_odd and ou_odd <= 1.70:
            ai_btts = "Sim"
        elif "under" in ou_tip and ou_odd and ou_odd <= 1.80:
            ai_btts = "Não"
        else:
            ai_btts = "Indefinido"

        # Over / Under estimado
        if ou_tip:
            ai_ou = g.get("ouTip") or ""
        else:
            if odds_validas and menor < 1.70:
                ai_ou = "Over 2.5"
            else:
                ai_ou = "Under 2.5"

        # Confiança IA
        conf = 5
        if odd1 and odd1 <= 1.60 or odd2 and odd2 <= 1.60:
            conf += 2
        if ou_odd and ou_odd <= 1.60:
            conf += 1
        conf = max(3, min(10, conf))

        g["aiTipMain"] = ai_main
        g["aiBTTS"] = ai_btts
        g["aiOU"] = ai_ou
        g["aiConfidence"] = conf
        g["aiComment"] = f"IA: {ai_main}, {ai_btts}, {ai_ou} (confiança {conf}/10)"

        jogos.append(g)

    return jogos


# -------------------------------------------------
#  ENDPOINTS
# -------------------------------------------------
@app.get("/")
def root():
    return {"status": "online", "message": "Backend Nuno Deca Football AI ativo."}


@app.get("/api/jogos-hoje")
def jogos_hoje():
    hoje = date.today()
    jogos = fetch_games_from_sheet(hoje)
    if not jogos:
        jogos = base_games(hoje)
    return add_ai_to_games(jogos)


@app.get("/api/jogos-amanha")
def jogos_amanha():
    amanha = date.today() + timedelta(days=1)
    jogos = fetch_games_from_sheet(amanha)
    if not jogos:
        jogos = base_games(amanha)
    return add_ai_to_games(jogos)
