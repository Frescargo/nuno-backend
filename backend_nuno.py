from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import date, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def base_games(day: date):
def base_games(day: date):
    """
    MODELO MANUAL PARA O NUNO
    - Se o dia for hoje -> devolve jogos de hoje.
    - Se o dia for amanhã -> devolve jogos de amanhã.
    - Para mudar, só alteras as listas em cada bloco.
    """
    iso = day.isoformat()
    hoje = date.today()
    amanha = hoje + timedelta(days=1)

    # -------------------------
    # JOGOS DE HOJE
    # -------------------------
    if day == hoje:
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
        ]

    # -------------------------
    # JOGOS DE AMANHÃ
    # -------------------------
    if day == amanha:
        return [
            {
                "date": iso,
                "league": "Premier League",
                "home": "Arsenal",
                "away": "Chelsea",
                "odd1": 2.05,
                "oddX": 3.50,
                "odd2": 3.40,
                "tipMain": "1",
                "oddMain": 2.05,
                "valueMain": 0.06,
                "confidenceMain": 4,
                "bttsTip": "Sim",
                "bttsOdd": 1.85,
                "valueBTTS": 0.03,
                "confidenceBTTS": 3,
                "ouTip": "Over 2.5",
                "ouOdd": 1.90,
                "valueOU": 0.03,
                "confidenceOU": 3,
                "source": "FreeSuperTips + Skores",
            },
            {
                "date": iso,
                "league": "LaLiga",
                "home": "Real Madrid",
                "away": "Sevilla",
                "odd1": 1.55,
                "oddX": 4.20,
                "odd2": 6.00,
                "tipMain": "1",
                "oddMain": 1.55,
                "valueMain": 0.04,
                "confidenceMain": 4,
                "bttsTip": "Não",
                "bttsOdd": 1.95,
                "valueBTTS": 0.02,
                "confidenceBTTS": 3,
                "ouTip": "Over 2.5",
                "ouOdd": 1.80,
                "valueOU": 0.02,
                "confidenceOU": 3,
                "source": "Andys + FST",
            },
            {
                "date": iso,
                "league": "Serie A",
                "home": "Inter",
                "away": "Napoli",
                "odd1": 2.10,
                "oddX": 3.25,
                "odd2": 3.40,
                "tipMain": "1",
                "oddMain": 2.10,
                "valueMain": 0.05,
                "confidenceMain": 4,
                "bttsTip": "Sim",
                "bttsOdd": 1.75,
                "valueBTTS": 0.02,
                "confidenceBTTS": 3,
                "ouTip": "Over 2.5",
                "ouOdd": 1.95,
                "valueOU": 0.03,
                "confidenceOU": 3,
                "source": "Skores + SportyTrader",
            },
            {
                "date": iso,
                "league": "Bundesliga",
                "home": "Bayern Munich",
                "away": "RB Leipzig",
                "odd1": 1.65,
                "oddX": 4.20,
                "odd2": 4.80,
                "tipMain": "1",
                "oddMain": 1.65,
                "valueMain": 0.04,
                "confidenceMain": 4,
                "bttsTip": "Sim",
                "bttsOdd": 1.60,
                "valueBTTS": 0.01,
                "confidenceBTTS": 3,
                "ouTip": "Over 3.5",
                "ouOdd": 2.10,
                "valueOU": 0.03,
                "confidenceOU": 3,
                "source": "FreeSuperTips",
            },
            {
                "date": iso,
                "league": "Primeira Liga",
                "home": "Benfica",
                "away": "Braga",
                "odd1": 1.75,
                "oddX": 3.60,
                "odd2": 4.50,
                "tipMain": "1",
                "oddMain": 1.75,
                "valueMain": 0.05,
                "confidenceMain": 4,
                "bttsTip": "Sim",
                "bttsOdd": 1.85,
                "valueBTTS": 0.03,
                "confidenceBTTS": 4,
                "ouTip": "Over 2.5",
                "ouOdd": 1.80,
                "valueOU": 0.03,
                "confidenceOU": 3,
                "source": "FreeSuperTips + Skores",
            },
        ]

    # Qualquer outro dia -> sem jogos
    return []

@app.get("/api/jogos-hoje")
def jogos_hoje():
    return base_games(date.today())


@app.get("/api/jogos-amanha")
def jogos_amanha():
    return base_games(date.today() + timedelta(days=1))    
