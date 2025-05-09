from flask import Flask, render_template, request
from datetime import datetime
import sys
import os

# Adicionar o diretório src ao sys.path para importar folgas
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(src_path)

import folgas

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../templates'))

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    data_selecionada = datetime.today().strftime('%Y-%m-%d') # Data padrão é hoje
    data_selecionada_formatada = datetime.today().strftime('%d/%m/%Y')
    ano_atual = datetime.today().year

    if request.method == 'POST':
        data_consulta_str = request.form.get('data_consulta')
        if data_consulta_str:
            data_selecionada = data_consulta_str # Mantém o formato YYYY-MM-DD para o input date
            try:
                # Converter para DD/MM/YYYY para a função get_off_duty_info e para exibição
                data_obj = datetime.strptime(data_consulta_str, '%Y-%m-%d')
                data_consulta_formatada_para_funcao = data_obj.strftime('%d/%m/%Y')
                data_selecionada_formatada = data_consulta_formatada_para_funcao
                
                resultado = folgas.get_off_duty_info(data_consulta_formatada_para_funcao)
            except ValueError:
                resultado = {"error": "Formato de data inválido fornecido pelo formulário."}
        else:
            resultado = {"error": "Nenhuma data foi selecionada."}
            # Para exibição, se data_consulta_str for None, usamos a data de hoje formatada
            data_selecionada_formatada = datetime.today().strftime('%d/%m/%Y')

    return render_template('index.html', 
                           resultado=resultado, 
                           data_selecionada=data_selecionada, 
                           data_selecionada_formatada=data_selecionada_formatada,
                           ano_atual=ano_atual)

if __name__ == '__main__':
    # Garante que o Flask procure templates e arquivos estáticos no lugar certo
    # A estrutura esperada é:
    # folga_app/
    #   src/
    #     main.py
    #     folgas.py
    #     ESCALAS.xlsx
    #   templates/
    #     index.html
    #   venv/ (opcional)
    # requirements.txt (no diretório folga_app)
    app.run(host='0.0.0.0', port=5000, debug=True)

