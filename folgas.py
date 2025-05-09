import pandas as pd
from datetime import datetime, timedelta
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXCEL_FILE_PATH = os.path.join(BASE_DIR, "ESCALAS.xlsx")

try:
    df_escalas = pd.read_excel(EXCEL_FILE_PATH, sheet_name="Planilha1")
except FileNotFoundError:
    df_escalas = None
except Exception as e:
    df_escalas = None

TURMA_COLUMNS = {
    1: "Turma 01", 2: "Turma 02", 3: "Turma 03",
    4: "Turma 04", 5: "Turma 05", 6: "Turma 06",
}

REFERENCE_DATE = datetime(2025, 5, 9)  # Sexta-feira
REFERENCE_OFF_TEAM = 4  # Turma 04 folga em 09/05/2025
TEAM_ROTATION_ORDER = [4, 5, 6, 1, 2, 3]

def _count_rotation_advances(d1, d2):
    advances = 0
    if d1 == d2:
        return 0

    current_date = d1
    if d1 < d2:  # Avançando
        # Loop até current_date ser igual a d2
        # O avanço é contado para o dia que current_date se torna
        while current_date < d2:
            current_date += timedelta(days=1)
            if current_date.weekday() == 6:  # Domingo
                continue
            if current_date.weekday() == 0:  # Segunda
                pass  # Não avança a rotação na segunda-feira
            else:  # Terça a Sábado
                advances += 1
    else:  # Retrocedendo (d1 > d2)
        while current_date > d2:
            current_date -= timedelta(days=1)
            if current_date.weekday() == 6:  # Domingo
                continue
            if current_date.weekday() == 0:  # Segunda
                # Ao chegar em uma segunda-feira (vindo do futuro), a rotação não "volta" neste dia
                pass
            else:  # Terça a Sábado (dias que causam mudança de rotação para trás)
                advances -= 1
    return advances

def calculate_off_team_for_day_logic(target_date):
    if target_date.weekday() == 6:  # Domingo
        return None

    if target_date == REFERENCE_DATE:
        return REFERENCE_OFF_TEAM

    try:
        initial_idx = TEAM_ROTATION_ORDER.index(REFERENCE_OFF_TEAM)
    except ValueError:
        # Should not happen if REFERENCE_OFF_TEAM is in TEAM_ROTATION_ORDER
        return None 

    advances = _count_rotation_advances(REFERENCE_DATE, target_date)
    
    final_idx = (initial_idx + advances) % len(TEAM_ROTATION_ORDER)
    return TEAM_ROTATION_ORDER[final_idx]

def get_off_duty_info(date_str):
    if df_escalas is None:
        return {"turma_folga": None, "dia_semana": "Erro", "escalas": [], "error": f"Planilha de escalas não carregada. Verifique o caminho: {EXCEL_FILE_PATH}"}

    try:
        if '/' in date_str:
            current_date = datetime.strptime(date_str, "%d/%m/%Y")
        else:
            current_date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return {"turma_folga": None, "dia_semana": "Data Inválida", "escalas": [], "error": "Formato de data inválido. Use DD/MM/AAAA."}

    day_of_week = current_date.weekday()
    dias_semana_map = {0: "Segunda-feira", 1: "Terça-feira", 2: "Quarta-feira", 3: "Quinta-feira", 4: "Sexta-feira", 5: "Sábado", 6: "Domingo"}
    dia_semana_nome = dias_semana_map.get(day_of_week, "Desconhecido")

    if day_of_week == 6:  # Domingo
        return {"turma_folga": None, "dia_semana": "Domingo (DSR)", "escalas": []}

    off_team = None
    if day_of_week == 0:  # Segunda-feira
        saturday_date = current_date - timedelta(days=2)
        off_team = calculate_off_team_for_day_logic(saturday_date)
    else:  # Terça a Sábado
        off_team = calculate_off_team_for_day_logic(current_date)

    schedules = []
    if off_team is not None:
        team_column_name = TURMA_COLUMNS.get(off_team)
        if team_column_name and team_column_name in df_escalas.columns:
            for _, row in df_escalas.iterrows():
                schedules.append({
                    "horario": str(row["Horário"]),
                    "escala": str(row[team_column_name])
                })
        else:
            return {"turma_folga": off_team, "dia_semana": dia_semana_nome, "escalas": [], "error": f"Coluna para turma {off_team} não encontrada na planilha."}
    
    return {"turma_folga": off_team, "dia_semana": dia_semana_nome, "escalas": schedules}

if __name__ == "__main__":
    test_dates = [
        "09/05/2025", "10/05/2025", "11/05/2025", "12/05/2025",
        "13/05/2025", "14/05/2025", "15/05/2025", "16/05/2025",
        "17/05/2025", "18/05/2025", "19/05/2025", "20/05/2025",
        "08/05/2025", "07/05/2025", "06/05/2025", "05/05/2025",
        "03/05/2025", "04/05/2025"
    ]
    expected_results = {
        "09/05/2025": 4, "10/05/2025": 5, "11/05/2025": None, "12/05/2025": 5,
        "13/05/2025": 6, "14/05/2025": 1, "15/05/2025": 2, "16/05/2025": 3,
        "17/05/2025": 4, "18/05/2025": None, "19/05/2025": 4, "20/05/2025": 5,
        "08/05/2025": 3, "07/05/2025": 2, "06/05/2025": 1, "05/05/2025": 6, 
        "03/05/2025": 6, "04/05/2025": None
    }

    print("Iniciando testes da lógica de folgas:")
    all_tests_passed = True
    for date_str_test in test_dates:
        result = get_off_duty_info(date_str_test)
        expected_team = expected_results.get(date_str_test)
        actual_team = result.get("turma_folga")
        
        status = "PASSOU" if actual_team == expected_team else "FALHOU"
        if actual_team != expected_team:
            all_tests_passed = False
        print(f"Data: {date_str_test} ({result.get('dia_semana')}) -> Esperado: T{expected_team}, Resultado: T{actual_team} - {status}")
        if result.get("error"):
            print(f"  Erro: {result.get('error')}")
    
    if all_tests_passed:
        print("\nTodos os testes passaram com sucesso!")
    else:
        print("\nAlguns testes falharam.")
