from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import date, timedelta
from urllib.request import urlopen
import csv
import io

app = FastAPI()

# -------------------------------------------------
#  CORS – permite que o painel Netlify aceda à API
# -------------------------------------------------
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
#  IA AJUSTADA (FOCA-SE EM AVALIAR AS TUAS TIPS)
# -------------------------------------------------
def add_ai_to_games(games):
    """
    Adiciona previsões da IA a cada jogo, dando mais peso às tuas tips.
    - Calcula favorito pelas odds 1X2
    - Usa OU/BTTS como apoio
    - Avalia alinhamento entre a tua tip e o que as odds sugerem
    - Produz confiança entre 3 e 10 (mais afinada)
    """
    jogos = []

    for game in games:
        g = game.copy()

        odd1 = g.get("odd1") or 0
        oddX = g.get("oddX") or 0
        odd2 = g.get("odd2") or 0
        ou_tip_raw = (g.get("ouTip") or "").strip()
        ou_tip = ou_tip_raw.lower()
        ou_odd = g.get("ouOdd") or 0

        manual_main = (g.get("tipMain") or "").strip().upper()
        manual_btts = (g.get("bttsTip") or "").strip().upper()

        # ---------------------------
        #  PROBABILIDADES 1X2 PELAS ODDS
        # ---------------------------
        probs = {}
        if odd1 and odd1 > 1.01:
            probs["1"] = 1.0 / odd1
        if oddX and oddX > 1.01:
            probs["X"] = 1.0 / oddX
        if odd2 and odd2 > 1.01:
            probs["2"] = 1.0 / odd2

        best_key = None
        norm_probs = {}

        if probs:
            total_p = sum(probs.values())
            if total_p > 0:
                for k, v in probs.items():
                    norm_probs[k] = v / total_p
                best_key = max(norm_probs, key=norm_probs.get)

        # Sugestão 1X2 da IA (modelo)
        if best_key:
            model_main = best_key  # "1", "X" ou "2"
        else:
            model_main = "INDEFINIDO"

        # aiTipMain: a IA sugere o favorito das odds,
        # mas não substitui a tua tip – só avalia
        ai_main = model_main

        # ---------------------------
        #  BTTS PELAS ODDS DE OVER/UNDER
        # ---------------------------
        if "over 3.5" in ou_tip and ou_odd and ou_odd <= 2.20:
            ai_btts = "SIM"
        elif "over 2.5" in ou_tip and ou_odd and ou_odd <= 1.90:
            ai_btts = "SIM"
        elif "under 2.5" in ou_tip and ou_odd and ou_odd <= 1.80:
            ai_btts = "NÃO"
        else:
            ai_btts = "INDEFINIDO"

        # ---------------------------
        #  OVER/UNDER PELAS ODDS
        # ---------------------------
        if ou_tip_raw:
            ai_ou = ou_tip_raw
        else:
            # fallback: se favorito muito forte, tendência para Over
            if best_key and norm_probs.get(best_key, 0) >= 0.60:
                ai_ou = "Over 2.5"
            else:
                ai_ou = "Under 2.5"

        # ---------------------------
        #  CONFIDENCE – AFINADA
        # ---------------------------
        score = 0

        # 1) Quão claro é o favorito 1X2?
        if best_key and norm_probs:
            fav_p = norm_probs.get(best_key, 0)
            if fav_p >= 0.70:
                score += 4
            elif fav_p >= 0.60:
                score += 3
            elif fav_p >= 0.55:
                score += 2
            else:
                score += 1

        # 2) Força do mercado OU (odd baixa = mercado “forte”)
        if ou_odd:
            if ou_odd <= 1.40:
                score += 3
            elif ou_odd <= 1.60:
                score += 2
            elif ou_odd <= 1.80:
                score += 1

        # 3) Alinhamento tua tip 1X2 vs odds
        if manual_main in ("1", "X", "2") and model_main in ("1", "X", "2"):
            if manual_main == model_main:
                score += 3   # estás alinhado com o favorito do mercado
            else:
                score -= 2   # estás contra o favorito

        # 4) Alinhamento BTTS
        if manual_btts in ("SIM", "NÃO") and ai_btts in ("SIM", "NÃO"):
            if manual_btts == ai_btts:
                score += 2
            else:
                score -= 1

        # 5) Alinhamento Over/Under
        if ou_tip:
            manual_over = "over" in ou_tip
            manual_under = "under" in ou_tip
            ai_over = "over" in ai_ou.lower()
            ai_under = "under" in ai_ou.lower()

            if (manual_over and ai_over) or (manual_under and ai_under):
                score += 2
            elif (manual_over and ai_under) or (manual_under and ai_over):
                score -= 1

        # Base de 5, para não ficar demasiado baixa
        conf = 5 + score

        # Agressivo mas controlado: entre 3 e 10
        if conf < 3:
            conf = 3
        if conf > 10:
            conf = 10

        g["aiTipMain"] = ai_main
        g["aiBTTS"] = ai_btts
        g["aiOU"] = ai_ou
        g["aiConfidence"] = conf
        g["aiComment"] = (
            f"Odds indicam {ai_main}, BTTS {ai_btts}, {ai_ou}. "
            f"Tua tip: {manual_main or '-'}, BTTS {manual_btts or '-'}, OU {ou_tip_raw or '-'} "
            f"(confiança {conf}/10)."
        )

        jogos.append(g)

    return jogos


# -------------------------------------------------
#  ENDPOINTS
# -------------------------------------------------
@app.get("/")
def root():
    return {
        "status": "online",
        "message": "Backend Nuno Deca Football AI ativo (IA ajustada para avaliar as tuas tips).",
    }


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
