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
    iso = day.isoformat()
    return [
        {
            "date": iso,
            "league": "Serie A",
            "home": "Como",
            "away": "Sassuolo",
            "odd1": 1.73,
            "oddX": 3.60,
            "odd2": 4.50,
            "tipMain": "1",
            "oddMain": 1.73,
            "valueMain": 0.07,
            "confidenceMain": 5,
            "bttsTip": "Sim",
            "bttsOdd": 1.90,
            "valueBTTS": 0.04,
            "confidenceBTTS": 4,
            "ouTip": "Over 2.5",
            "ouOdd": 2.00,
            "valueOU": 0.05,
            "confidenceOU": 4,
            "source": "Skores + SportyTrader"
        },
        {
            "date": iso,
            "league": "Championship",
            "home": "Oxford Utd",
            "away": "Ipswich",
            "odd1": 5.00,
            "oddX": 4.00,
            "odd2": 1.57,
            "tipMain": "2",
            "oddMain": 1.57,
            "valueMain": 0.05,
            "confidenceMain": 4,
            "bttsTip": "Não",
            "bttsOdd": 2.05,
            "valueBTTS": 0.03,
            "confidenceBTTS": 3,
            "ouTip": "Under 3.5",
            "ouOdd": 1.70,
            "valueOU": 0.02,
            "confidenceOU": 3,
            "source": "Skores"
        }
    ]

@app.get("/api/jogos-hoje")
def jogos_hoje():
    return base_games(date.today())

@app.get("/api/jogos-amanha")
def jogos_amanha():
    return base_games(date.today() + timedelta(days=1))
