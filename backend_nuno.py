from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import date, timedelta

app = FastAPI()

# CORS para permitir o painel aceder à API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def base_games(day: date):
    """
    Jogos base (manuais) todos com a mesma data (day).
    Mais tarde podemos trocar isto para ler da Google Sheet.
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
            "oddMain": 1.55,
            "valueMain": 0.06,
            "confidenceMain": 4,
            "bttsTip": "Sim",
            "bttsOdd": 1.70,
            "valueBTTS": 0.03,
            "confidenceBTTS": 3,
            "ouTip": "Over 2.5",
            "ouOdd": 1.50,
            "valueOU": 0.03,
            "confidenceOU": 4,
            "source": "FreeSuperTips + Skores",
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
            "oddMain": 1.40,
            "valueMain": 0.05,
            "confidenceMain": 5,
            "bttsTip": "Sim",
            "bttsOdd": 1.75,
            "valueBTTS": 0.02,
            "confidenceBTTS": 3,
            "ouTip": "Over 2.5",
            "ouOdd": 1.55,
            "valueOU": 0.02,
            "confidenceOU": 3,
            "source": "FST + SportyTrader",
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
            "oddMain": 1.85,
            "valueMain": 0.05,
            "confidenceMain": 4,
            "bttsTip": "Não",
            "bttsOdd": 1.80,
            "valueBTTS": 0.03,
            "confidenceBTTS": 3,
            "ouTip": "Under 2.5",
            "ouOdd": 1.75,
            "valueOU": 0.03,
            "confidenceOU": 4,
            "source": "SportyTrader",
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
            "oddMain": 1.50,
            "valueMain": 0.04,
            "confidenceMain": 4,
            "bttsTip": "Sim",
            "bttsOdd": 1.50,
            "valueBTTS": 0.04,
            "confidenceBTTS": 4,
            "ouTip": "Over 2.5",
            "ouOdd": 1.55,
            "valueOU": 0.03,
            "confidenceOU": 4,
            "source": "FST + Skores",
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
            "oddMain": 1.45,
            "valueMain": 0.03,
            "confidenceMain": 4,
            "bttsTip": "Não",
            "bttsOdd": 1.90,
            "valueBTTS": 0.02,
            "confidenceBTTS": 3,
            "ouTip": "Under 2.5",
            "ouOdd": 1.70,
            "valueOU": 0.02,
            "confidenceOU": 3,
            "source": "SportyTrader",
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
            "oddMain": 1.45,
            "valueMain": 0.06,
            "confidenceMain": 5,
            "bttsTip": "Sim",
            "bttsOdd": 1.95,
            "valueBTTS": 0.03,
            "confidenceBTTS": 3,
            "ouTip": "Over 2.5",
            "ouOdd": 1.60,
            "valueOU": 0.02,
            "confidenceOU": 3,
            "source": "FreeSuperTips + Skores",
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
            "oddMain": 1.75,
            "valueMain": 0.05,
            "confidenceMain": 4,
            "bttsTip": "Sim",
            "bttsOdd": 1.55,
            "valueBTTS": 0.04,
            "confidenceBTTS": 4,
            "ouTip": "Over 2.5",
            "ouOdd": 1.60,
            "valueOU": 0.03,
            "confidenceOU": 4,
            "source": "FST",
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
            "oddMain": 1.65,
            "valueMain": 0.05,
            "confidenceMain": 4,
            "bttsTip": "Não",
            "bttsOdd": 1.75,
            "valueBTTS": 0.02,
            "confidenceBTTS": 3,
            "ouTip": "Under 2.5",
            "ouOdd": 1.85,
            "valueOU": 0.02,
            "confidenceOU": 3,
            "source": "SportyTrader",
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
            "oddMain": 1.65,
            "valueMain": 0.04,
            "confidenceMain": 4,
            "bttsTip": "Sim",
            "bttsOdd": 1.50,
            "valueBTTS": 0.04,
            "confidenceBTTS": 4,
            "ouTip": "Over 2.5",
            "ouOdd": 1.65,
            "valueOU": 0.04,
            "confidenceOU": 4,
            "source": "FST + Skores",
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
            "oddMain": 1.60,
            "valueMain": 0.04,
            "confidenceMain": 4,
            "bttsTip": "Sim",
            "bttsOdd": 1.60,
            "valueBTTS": 0.04,
            "confidenceBTTS": 4,
            "ouTip": "Over 2.5",
            "ouOdd": 1.75,
            "valueOU": 0.03,
            "confidenceOU": 4,
            "source": "Stats + FST",
        },
    ]


def add_ai_to_games(games):
    """
    Adiciona campos simples de IA com base nas odds do jogo.
    Versão grátis apenas para testar comportamento.
    """
    jogos_com_ia = []

    for g in games:
        game = g.copy()

        odd1 = game.get("odd1") or 0
        oddX = game.get("oddX") or 0
        odd2 = game.get("odd2") or 0
        ou_tip = (game.get("ouTip") or "").lower()
        ou_odd = game.get("ouOdd") or 0

        # --- IA Tip 1X2 (odd mais baixa = tip mais provável) ---
        valids = [v for v in [odd1, oddX, odd2] if v]
        lowest = min(valids) if valids else 0

        if lowest and lowest == odd1:
            ai_tip_main = "1"
        elif lowest and lowest == oddX:
            ai_tip_main = "X"
        elif lowest and lowest == odd2:
            ai_tip_main = "2"
        else:
            ai_tip_main = "Indefinido"

        # --- IA BTTS ---
        if "over" in ou_tip and ou_odd and ou_odd <= 1.70:
            ai_btts = "Sim"
        elif "under" in ou_tip and ou_odd and ou_odd <= 1.80:
            ai_btts = "Não"
        else:
            ai_btts = "Indefinido"

        # --- IA Over/Under ---
        if ou_tip:
            ai_ou = game.get("ouTip")
        else:
            if lowest and lowest < 1.70:
                ai_ou = "Over 2.5"
            elif lowest and lowest > 2.20:
                ai_ou = "Under 2.5"
            else:
                ai_ou = "Neutro"

        # --- Confiança (0–10) ---
        confiança = 5
        if lowest and lowest <= 1.60:
            confiança += 2
        elif lowest and lowest <= 1.80:
            confiança += 1

        if ou_odd and ou_odd <= 1.60:
            confiança += 1

        confiança = max(3, min(10, confiança))

        comentario = (
            f"IA simples: odd mais forte aponta para {ai_tip_main}, "
            f"tendência {ai_ou} e BTTS {ai_btts}."
        )

        game["aiTipMain"] = ai_tip_main
        game["aiBTTS"] = ai_btts
        game["aiOU"] = ai_ou
        game["aiConfidence"] = confiança
        game["aiComment"] = comentario

        jogos_com_ia.append(game)

    return jogos_com_ia


@app.get("/")
def root():
    return {"status": "ok", "message": "Backend Nuno com IA simples ativo"}


@app.get("/api/jogos-hoje")
def jogos_hoje():
    jogos = base_games(date.today())
    return add_ai_to_games(jogos)


@app.get("/api/jogos-amanha")
def jogos_amanha():
    jogos = base_games(date.today() + timedelta(days=1))
    return add_ai_to_games(jogos)
