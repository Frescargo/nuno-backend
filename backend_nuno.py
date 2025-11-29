{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww38200\viewh24100\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from fastapi import FastAPI\
from fastapi.middleware.cors import CORSMiddleware\
from datetime import date, timedelta\
\
app = FastAPI()\
\
# Permitir acesso do teu painel (Netlify, etc.)\
app.add_middleware(\
    CORSMiddleware,\
    allow_origins=["*"],   # podes restringir mais tarde\
    allow_credentials=True,\
    allow_methods=["*"],\
    allow_headers=["*"],\
)\
\
\
def base_games(day: date):\
    """\
    LISTA DE JOGOS PARA ESSE DIA.\
    \'c9 AQUI QUE VAIS MEXER PARA P\'d4R OS JOGOS DE AMANH\'c3.\
    """\
    iso = day.isoformat()\
\
    games = [\
        \{\
            "date": iso,\
            "league": "Serie A",\
            "home": "Como",\
            "away": "Sassuolo",\
            "odd1": 1.73,\
            "oddX": 3.60,\
            "odd2": 4.50,\
            # Mercado 1X2\
            "tipMain": "1",\
            "oddMain": 1.73,\
            "valueMain": 0.07,\
            "confidenceMain": 5,\
            # Mercado BTTS\
            "bttsTip": "Sim",\
            "bttsOdd": 1.90,\
            "valueBTTS": 0.04,\
            "confidenceBTTS": 4,\
            # Mercado Over/Under\
            "ouTip": "Over 2.5",\
            "ouOdd": 2.00,\
            "valueOU": 0.05,\
            "confidenceOU": 4,\
            "source": "Skores + SportyTrader",\
        \},\
        \{\
            "date": iso,\
            "league": "Championship",\
            "home": "Oxford Utd",\
            "away": "Ipswich",\
            "odd1": 5.00,\
            "oddX": 4.00,\
            "odd2": 1.57,\
            "tipMain": "2",\
            "oddMain": 1.57,\
            "valueMain": 0.05,\
            "confidenceMain": 4,\
            "bttsTip": "N\'e3o",\
            "bttsOdd": 2.05,\
            "valueBTTS": 0.03,\
            "confidenceBTTS": 3,\
            "ouTip": "Under 3.5",\
            "ouOdd": 1.70,\
            "valueOU": 0.02,\
            "confidenceOU": 3,\
            "source": "Skores",\
        \},\
        \{\
            "date": iso,\
            "league": "LaLiga",\
            "home": "Getafe",\
            "away": "Elche",\
            "odd1": 2.10,\
            "oddX": 2.88,\
            "odd2": 4.00,\
            "tipMain": "X",\
            "oddMain": 2.88,\
            "valueMain": 0.02,\
            "confidenceMain": 3,\
            "bttsTip": "Sim",\
            "bttsOdd": 2.20,\
            "valueBTTS": 0.01,\
            "confidenceBTTS": 3,\
            "ouTip": "Under 2.5",\
            "ouOdd": 1.85,\
            "valueOU": 0.03,\
            "confidenceOU": 3,\
            "source": "SportyTrader",\
        \},\
        \{\
            "date": iso,\
            "league": "Ligue 1",\
            "home": "Metz",\
            "away": "Rennes",\
            "odd1": 3.80,\
            "oddX": 3.40,\
            "odd2": 1.95,\
            "tipMain": "2",\
            "oddMain": 1.95,\
            "valueMain": 0.06,\
            "confidenceMain": 4,\
            "bttsTip": "Sim",\
            "bttsOdd": 1.95,\
            "valueBTTS": 0.05,\
            "confidenceBTTS": 4,\
            "ouTip": "Over 1.5",\
            "ouOdd": 1.40,\
            "valueOU": 0.01,\
            "confidenceOU": 4,\
            "source": "Skores + SportyTrader",\
        \},\
        \{\
            "date": iso,\
            "league": "Bundesliga",\
            "home": "Monchengladbach",\
            "away": "Leipzig",\
            "odd1": 2.90,\
            "oddX": 3.80,\
            "odd2": 2.20,\
            "tipMain": None,\
            "oddMain": None,\
            "valueMain": 0.00,\
            "confidenceMain": 3,\
            "bttsTip": "Sim",\
            "bttsOdd": 1.80,\
            "valueBTTS": 0.04,\
            "confidenceBTTS": 3,\
            "ouTip": "Over 2.5",\
            "ouOdd": 1.95,\
            "valueOU": 0.03,\
            "confidenceOU": 3,\
            "source": "Skores + SportyTrader",\
        \},\
        \{\
            "date": iso,\
            "league": "CAF Champions League",\
            "home": "MC Alger",\
            "away": "Mamelodi Sundowns",\
            "odd1": 2.75,\
            "oddX": 2.90,\
            "odd2": 2.45,\
            "tipMain": None,\
            "oddMain": None,\
            "valueMain": 0.00,\
            "confidenceMain": 3,\
            "bttsTip": "N\'e3o",\
            "bttsOdd": 1.70,\
            "valueBTTS": 0.03,\
            "confidenceBTTS": 3,\
            "ouTip": "Under 2.5",\
            "ouOdd": 1.85,\
            "valueOU": 0.04,\
            "confidenceOU": 3,\
            "source": "Skores + SportyTrader",\
        \},\
    ]\
\
    return games\
\
\
@app.get("/api/jogos-hoje")\
def jogos_hoje():\
    today = date.today()\
    return base_games(today)\
\
\
@app.get("/api/jogos-amanha")\
def jogos_amanha():\
    tomorrow = date.today() + timedelta(days=1)\
    return base_games(tomorrow)}
