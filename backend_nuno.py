from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import date, timedelta
from urllib.request import urlopen, Request
import csv
import io
import os
import json
import urllib.parse

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
#  CHAVE DA API-FOOTBALL (vem das variáveis de ambiente do Render)
# -------------------------------------------------
API_FOOTBALL_KEY = os.environ.get("API_FOOTBALL_KEY", "").strip()

# caches simples para não repetir chamadas
_TEAM_ID_CACHE = {}
_TEAM_STATS_CACHE = {}


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

        raw_date = raw_date.replace("/", "-")

        try:
            row_date = date.fromisoformat(raw_date)
        except ValueError:
            continue

        if row_date != day:
            continue

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
#  FUNÇÕES PARA LIGAR À API-FOOTBALL (ESTATÍSTICAS)
# -------------------------------------------------
def api_football_get(path: str, params: dict):
    """
    Faz um GET à API-FOOTBALL.
    Se não houver chave ou der erro, devolve None.
    """
    if not API_FOOTBALL_KEY:
        return None

    base_url = "https://v3.football.api-sports.io"
    url = base_url + path
    if params:
        url += "?" + urllib.parse.urlencode(params)

    headers = {
        "x-apisports-key": API_FOOTBALL_KEY,
    }

    req = Request(url, headers=headers)
    try:
        with urlopen(req, timeout=10) as resp:
            data = resp.read().decode("utf-8")
            return json.loads(data)
    except Exception as e:
        print("API_FOOTBALL ERROR:", e)
        return None


def get_team_id(team_name: str):
    """
    Procura o ID da equipa na API-FOOTBALL.
    Usa cache simples para não repetir pedidos.
    """
    if not API_FOOTBALL_KEY:
        return None

    key = (team_name or "").strip().lower()
    if not key:
        return None

    if key in _TEAM_ID_CACHE:
        return _TEAM_ID_CACHE[key]

    res = api_football_get("/teams", {"search": team_name})
    if not res or not res.get("response"):
        return None

    found_id = None
    for entry in res["response"]:
        t = (entry.get("team") or {})
        name = (t.get("name") or "").strip().lower()
        if name == key or key in name or name in key:
            found_id = t.get("id")
            break

    if not found_id:
        try:
            found_id = res["response"][0]["team"]["id"]
        except Exception:
            return None

    _TEAM_ID_CACHE[key] = found_id
    return found_id


def get_team_recent_stats(team_id: int, last_n: int = 5):
    """
    Lê os últimos N jogos da equipa na API-FOOTBALL e calcula:
      - média golos marcados
      - média golos sofridos
      - % BTTS
      - % Over 2.5
    Usa cache simples por equipa.
    """
    if not API_FOOTBALL_KEY or not team_id:
        return None

    cache_key = f"{team_id}_{last_n}"
    if cache_key in _TEAM_STATS_CACHE:
        return _TEAM_STATS_CACHE[cache_key]

    res = api_football_get("/fixtures", {"team": team_id, "last": last_n})
    if not res or not res.get("response"):
        return None

    total_gf = 0
    total_ga = 0
    matches = 0
    btts = 0
    over25 = 0

    for fx in res["response"]:
        goals = fx.get("goals") or {}
        g_home = goals.get("home")
        g_away = goals.get("away")
        if g_home is None or g_away is None:
            continue

        teams = fx.get("teams") or {}
        home_team = (teams.get("home") or {}).get("id")
        away_team = (teams.get("away") or {}).get("id")

        if team_id == home_team:
            gf = g_home
            ga = g_away
        elif team_id == away_team:
            gf = g_away
            ga = g_home
        else:
            gf = g_home
            ga = g_away

        matches += 1
        total_gf += gf
        total_ga += ga

        if gf > 0 and ga > 0:
            btts += 1

        if (gf + ga) >= 3:
            over25 += 1

    if matches == 0:
        return None

    stats = {
        "matches": matches,
        "avg_for": total_gf / matches,
        "avg_against": total_ga / matches,
        "btts_rate": btts / matches,
        "over25_rate": over25 / matches,
    }

    _TEAM_STATS_CACHE[cache_key] = stats
    return stats


def get_match_stats(home_name: str, away_name: str):
    """
    Junta as estatísticas recentes da equipa da casa e de fora
    e calcula alguns indicadores combinados.
    """
    try:
        home_id = get_team_id(home_name)
        away_id = get_team_id(away_name)
        if not home_id or not away_id:
            return None

        home_stats = get_team_recent_stats(home_id, last_n=5)
        away_stats = get_team_recent_stats(away_id, last_n=5)
        if not home_stats or not away_stats:
            return None

        btts_combined = (home_stats["btts_rate"] + away_stats["btts_rate"]) / 2.0
        over25_combined = (home_stats["over25_rate"] + away_stats["over25_rate"]) / 2.0
        goals_total_avg = home_stats["avg_for"] + away_stats["avg_for"]

        return {
            "home": home_stats,
            "away": away_stats,
            "btts_combined": btts_combined,
            "over25_combined": over25_combined,
            "goals_total_avg": goals_total_avg,
        }
    except Exception as e:
        print("MATCH_STATS ERROR:", e)
        return None


# -------------------------------------------------
#  IA AVANÇADA: AVALIA AS TUAS TIPS + ESTATÍSTICAS
# -------------------------------------------------
def add_ai_to_games(games):
    """
    Adiciona previsões da IA a cada jogo.
    - Usa odds 1X2, OU e BTTS
    - Usa estatísticas recentes da API-FOOTBALL (quando possível)
    - Avalia a qualidade das tuas tips e ajusta confiança
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

        if best_key:
            model_main = best_key  # "1", "X" ou "2"
        else:
            model_main = "INDEFINIDO"

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
            if best_key and norm_probs.get(best_key, 0) >= 0.60:
                ai_ou = "Over 2.5"
            else:
                ai_ou = "Under 2.5"

        # ---------------------------
        #  BASE DE SCORE (ODDS + TUA TIP)
        # ---------------------------
        score = 0

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

        if ou_odd:
            if ou_odd <= 1.40:
                score += 3
            elif ou_odd <= 1.60:
                score += 2
            elif ou_odd <= 1.80:
                score += 1

        if manual_main in ("1", "X", "2") and model_main in ("1", "X", "2"):
            if manual_main == model_main:
                score += 3
            else:
                score -= 2

        if manual_btts in ("SIM", "NÃO") and ai_btts in ("SIM", "NÃO"):
            if manual_btts == ai_btts:
                score += 2
            else:
                score -= 1

        if ou_tip:
            manual_over = "over" in ou_tip
            manual_under = "under" in ou_tip
            ai_over = "over" in ai_ou.lower()
            ai_under = "under" in ai_ou.lower()

            if (manual_over and ai_over) or (manual_under and ai_under):
                score += 2
            elif (manual_over and ai_under) or (manual_under and ai_over):
                score -= 1

        # ---------------------------
        #  ESTATÍSTICAS AVANÇADAS (API-FOOTBALL)
        # ---------------------------
        stats = None
        if API_FOOTBALL_KEY:
            try:
                stats = get_match_stats(g.get("home"), g.get("away"))
            except Exception as e:
                print("ERROR MATCH_STATS:", e)
                stats = None

        stats_comment = ""
        if stats:
            btts_rate = stats["btts_combined"]
            over25_rate = stats["over25_combined"]
            goals_avg = stats["goals_total_avg"]

            if btts_rate >= 0.70:
                stats_comment += f"BTTS forte ({btts_rate*100:.0f}%). "
                if manual_btts == "SIM":
                    score += 3
                elif manual_btts == "NÃO":
                    score -= 2
                elif ai_btts == "INDEFINIDO":
                    ai_btts = "SIM"
            elif btts_rate <= 0.35:
                stats_comment += f"BTTS fraco ({btts_rate*100:.0f}%). "
                if manual_btts == "NÃO":
                    score += 2
                elif manual_btts == "SIM":
                    score -= 2

            if over25_rate >= 0.70 or goals_avg >= 3.0:
                stats_comment += f"Over 2.5 forte ({over25_rate*100:.0f}% / média golos {goals_avg:.2f}). "
                if "over" in ai_ou.lower():
                    score += 2
                else:
                    ai_ou = "Over 2.5"
            elif over25_rate <= 0.35 or goals_avg <= 2.0:
                stats_comment += f"Under 2.5 forte ({(1-over25_rate)*100:.0f}% / média golos {goals_avg:.2f}). "
                if "under" in ai_ou.lower():
                    score += 2
                else:
                    ai_ou = "Under 2.5"

        conf = 5 + score
        if conf < 3:
            conf = 3
        if conf > 10:
            conf = 10

        g["aiTipMain"] = ai_main
        g["aiBTTS"] = ai_btts
        g["aiOU"] = ai_ou
        g["aiConfidence"] = conf

        comment_parts = []
        comment_parts.append(f"IA 1X2: {ai_main}")
        comment_parts.append(f"BTTS: {ai_btts}")
        comment_parts.append(f"OU: {ai_ou}")
        comment_parts.append(f"Confiança {conf}/10")
        if stats_comment:
            comment_parts.append(stats_comment.strip())

        g["aiComment"] = " | ".join(comment_parts)

        jogos.append(g)

    return jogos


# -------------------------------------------------
#  ENDPOINTS
# -------------------------------------------------
@app.get("/")
def root():
    return {
        "status": "online",
        "message": "Backend Nuno Deca Football AI ativo (IA avançada com estatísticas, quando disponíveis).",
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
