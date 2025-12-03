from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import date, timedelta

app = FastAPI()

# CORS para permitir acesso do painel no telemóvel / PC
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------
#   BASE DE JOGOS (MANUAL)
# -----------------------------------
def base_games(day: date):
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
            "ouOdd": 1.50
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
            "ouOdd": 1.55
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
            "ouOdd": 1.75
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
            "ouOdd": 1.55
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
            "ouOdd": 1.70
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
            "ouOdd": 1.60
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
            "ouOdd": 1.60
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
            "ouOdd": 1.85
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
            "ouOdd": 1.65
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
            "ouOdd": 1.75
        }
    ]


# -----------------------------------
#      IA SIMPLES (AUTOMÁTICA)
# -----------------------------------
def add_ai_to_games(games):
    jogos = []

    for game in games:
        g = game.copy()

        odd1 = g.get("odd1") or 0
        oddX = g.get("oddX") or 0
        odd2 = g.get("odd2") or 0
        ou_tip = (g.get("ouTip") or "").lower()
        ou_odd = g.get("ouOdd") or 0

        # TIP PRINCIPAL (odd mais baixa)
        odds_validas = [v for v in [odd1, oddX, odd2] if v]
        if odds_validas:
            menor = min(odds_validas)
            if menor == odd1: ai_main = "1"
            elif menor == oddX: ai_main = "X"
            else: ai_main = "2"
        else:
            ai_main = "Indefinido"

        # BTTS
        if "over" in ou_tip and ou_odd <= 1.70:
            ai_btts = "Sim"
        elif "under" in ou_tip and ou_odd <= 1.80:
            ai_btts = "Não"
        else:
            ai_btts = "Indefinido"

        # Over / Under
        if ou_tip:
            ai_ou = g["ouTip"]
        else:
            ai_ou = "Over 2.5" if menor < 1.70 else "Under 2.5"

        # Confiança
        conf = 5
        if odd1 <= 1.60 or odd2 <= 1.60:
            conf += 2
        if ou_odd <= 1.60:
            conf += 1
        conf = max(3, min(10, conf))

        g["aiTipMain"] = ai_main
        g["aiBTTS"] = ai_btts
        g["aiOU"] = ai_ou
        g["aiConfidence"] = conf
        g["aiComment"] = f"IA: {ai_main}, {ai_btts}, {ai_ou} (confiança {conf}/10)"

        jogos.append(g)

    return jogos


# -----------------------------------
#         ENDPOINTS
# -----------------------------------
@app.get("/")
def root():
    return {"status": "online", "message": "Backend Nuno + IA ativo."}


@app.get("/api/jogos-hoje")
def jogos_hoje():
    jogos = base_games(date.today())
    return add_ai_to_games(jogos)


@app.get("/api/jogos-amanha")
def jogos_amanha():
    jogos = base_games(date.today() + timedelta(days=1))
    return add_ai_to_games(jogos)
