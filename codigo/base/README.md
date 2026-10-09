# Base - Controle De Leituras

Esta é a aplicação-base da avaliação de reposição da turma 2V.

Ela já possui CRUD de leituras com SQLite, Blueprint de autenticação, Blueprint de leituras e uma função de segurança iniciada em `seguranca.py`. A autenticação com `session` e o controle de acesso por usuário ainda precisam ser implementados.

## Executar

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Acesse `http://127.0.0.1:5000`.

## Arquivos Principais

- `app.py`: cria a aplicação e registra os Blueprints.
- `auth.py`: rotas de cadastro, login e logout a serem completadas.
- `leituras.py`: rotas do CRUD de leituras.
- `seguranca.py`: função de proteção das rotas privadas.
- `database.py`: funções de banco de dados.
- `templates/`: páginas HTML.

## Observação

Não substitua a aplicação por outro projeto. A tarefa é adaptar esta base para autenticação com `session`, vinculando cada leitura ao usuário logado.




## Justificativa

1- Por que as rotas de leituras ficaram em leituras.py e não no app.py?
Modularização com Blueprints do Flask melhora organização, manutenibilidade e escalabilidade.

2- Como a aplicação identifica o usuário logado usando session?
O ID do usuário é armazenado em session['user_id'] após login bem-sucedido.

3- Como impedem o acesso a leituras de outro usuário?
seguranca.py: decorator valida user_id em session.
leituras.py: rotas filtram consultas pelo usuário logado.
database.py: funções consultam/modificam leituras apenas do proprietário.