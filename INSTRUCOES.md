# Instruções para Executar o Consultor de Folgas

Este projeto é uma aplicação web Flask que permite consultar as turmas e escalas de folga com base em uma data fornecida.

## Estrutura do Projeto

O projeto está organizado da seguinte forma:

```
folga_app/
├── src/
│   ├── ESCALAS.xlsx  (Planilha com os dados das escalas e turmas)
│   ├── folgas.py     (Lógica para calcular as folgas)
│   └── main.py       (Aplicação Flask principal)
├── templates/
│   └── index.html    (Interface HTML da aplicação)
└── requirements.txt  (Dependências Python do projeto)
```

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## Como Executar Localmente

1.  **Descompacte o arquivo `folga_app.zip`** em um diretório de sua preferência.

2.  **Navegue até o diretório do projeto** pelo terminal:
    ```bash
    cd caminho/para/folga_app
    ```

3.  **(Opcional, mas recomendado) Crie e ative um ambiente virtual:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # No Linux/macOS
    # venv\Scripts\activate    # No Windows
    ```

4.  **Instale as dependências** listadas no arquivo `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Execute a aplicação Flask:**
    Navegue até o diretório `src` dentro de `folga_app`:
    ```bash
    cd src
    ```
    E então execute o arquivo `main.py`:
    ```bash
    python3 main.py
    ```

6.  **Acesse a aplicação no seu navegador:**
    Abra o seu navegador e acesse o endereço: `http://127.0.0.1:5000` ou `http://localhost:5000`

## Como Usar a Aplicação

-   Na página inicial, você verá um campo para selecionar a data.
-   Escolha a data desejada e clique no botão "Consultar Folgas".
-   Abaixo do formulário, será exibida a turma de folga para a data selecionada, juntamente com as escalas e horários correspondentes.
-   Lembre-se das regras:
    -   Domingos são DSR (Descanso Semanal Remunerado) e não há turma de folga.
    -   A turma que folga no sábado também folga na segunda-feira seguinte.

## Observações

-   A planilha `ESCALAS.xlsx` deve estar presente no diretório `folga_app/src/` para que a aplicação funcione corretamente.
-   O visual da página foi desenvolvido utilizando Bootstrap, com as cores branco e vermelho e cantos arredondados, conforme solicitado.

