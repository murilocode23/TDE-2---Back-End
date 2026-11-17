# TDE-2---Back-End

# API de Gestão de Avaliações — Programação Backend (UNIFAN)

API em **Python + Flask**, arquitetura **MVC**, banco relacional via **SQLAlchemy**,
autenticação com **JWT**. Todos os dados trafegam em **JSON**.

## Como rodar (Windows / PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1        # se der erro de política: Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
pip install -r requirements.txt
copy .env.example .env
```

Abra o `.env` e preencha (principalmente `JWT_SECRET_KEY`). Para gerar uma chave:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Depois, crie o banco (roda o `schema.sql`) e suba a API:

```powershell
flask --app run init-db            # use --reset para apagar e recriar
python run.py                      # http://127.0.0.1:5000
```

Rodar os testes: `pytest`

## Usuários de exemplo (vêm do schema.sql)

| E-mail               | Senha  | Tipo  |
|----------------------|--------|-------|
| admin@exemplo.com    | 123456 | admin |
| autor1@exemplo.com   | 654321 | autor |
| autor2@exemplo.com   | 213246 | autor |

## Como autenticar

```
POST /auth/login          (público — único endpoint sem token)
{"email": "admin@exemplo.com", "senha": "123456"}
→ 200 {"access_token": "...", "token_type": "Bearer", "expira_em_minutos": 60, "usuario": {...}}
```

Nos demais endpoints, envie o header `Authorization: Bearer <access_token>`.
Teste rápido no Postman/Insomnia: `GET /auth/me`.

## Estrutura (MVC com os nomes usados pelo professor)

```
app/
├── models/          # MODELS: uma classe por tabela (já estão todas prontas)
├── repositories/    # PERSISTÊNCIA: só falam com o banco (sem regra de negócio)
├── controllers/     # CONTROLLERS: regras de negócio (permissões, validações, restrições)
├── services/        # CAMADA DE SERVIÇOS: os endpoints (rotas) — registrados automaticamente
├── security/        # JWT, bcrypt, decorators de permissão
├── utils/           # paginação e leitura de requests
├── config.py        # variáveis de ambiente (nada de hardcode)
└── errors.py        # erros → JSON {"erro": "..."} com o status certo
```

Fluxo de uma requisição: **service** (lê a requisição) → **controller** (aplica as regras)
→ **repository** (lê/grava no banco) → volta como JSON.

## Regras do professor que a base JÁ garante

- **Todo endpoint exige login**, exceto `auth.login`. O padrão é negar: se você criar uma rota
  nova, ela já nasce protegida (há teste para isso). Não precisa decorator para exigir login.
- **Banco configurado só por variáveis de ambiente** (`DB_*`, `JWT_SECRET_KEY`). Nunca coloque
  senha/URL no código.
- **JSON em tudo**, inclusive login e token.
- **Paginação no banco** (LIMIT/OFFSET) com `?page=1&per_page=10`.

## Convenções (todo mundo segue, para o código ficar uniforme)

1. **Permissão por tipo de usuário:** `@roles_required("admin")` logo abaixo do `@bp.get/post/...`.
   O usuário logado é `usuario_logado()` (de `app.security.auth`).
2. **Regras de "só o autor ou admin"** ficam no **controller**, levantando `AcessoNegado`.
3. **Erros:** levante os de `app/errors.py` (`RequisicaoInvalida` 400, `AcessoNegado` 403,
   `NaoEncontrado` 404, `Conflito` 409, `RegraDeNegocio` 422). Não monte JSON de erro na mão.
4. **Listagem sempre paginada:** no repository use `listar_paginado(page, per_page, filtros)`;
   no controller devolva `serializar_pagina(...)`; no service use `obter_paginacao()`.
   Formato: `{"items": [...], "page": 1, "per_page": 10, "total": 25, "pages": 3}`.
5. **Corpo JSON obrigatório:** `dados = obter_json_obrigatorio("campo1", "campo2")`.
6. **Senha:** `hash_senha()` / `verificar_senha()` de `app/security/passwords.py`. Nunca texto puro,
   e nunca devolva o campo `senha` (o `to_dict()` do usuário já não devolve).
7. **Status codes:** criar → `201`; remover → `204` (corpo vazio); ler/atualizar → `200`.

## Como criar o seu módulo (passo a passo)

Cada pessoa mexe **só nos próprios arquivos**, para evitar conflito no git.
Exemplo para cursos (Lucas):

1. **Repository** (`app/repositories/curso_repository.py` já existe): adicione métodos de banco
   se precisar, ex.: contar disciplinas do curso.
2. **Controller** — crie `app/controllers/curso_controller.py` com a classe `CursoController`
   (regras: só admin cria/edita/remove, só remove se não houver disciplinas etc.).
3. **Service** — crie `app/services/curso_service.py`:

```python
from flask import Blueprint, jsonify
from app.controllers.curso_controller import CursoController
from app.models.usuario import Usuario
from app.security.auth import roles_required
from app.utils.request import obter_json_obrigatorio, obter_paginacao

bp = Blueprint("cursos", __name__, url_prefix="/cursos")   # <- precisa se chamar "bp"
controller = CursoController()

@bp.get("")
def listar():                                   # qualquer usuário logado
    page, per_page = obter_paginacao()
    return jsonify(controller.listar(page, per_page)), 200

@bp.post("")
@roles_required(Usuario.TIPO_ADMIN)
def criar():
    dados = obter_json_obrigatorio("nome", "descricao", "formato_aula")
    return jsonify(controller.criar(dados)), 201
```

Pronto: o arquivo `*_service.py` com `bp` é **registrado automaticamente**.
4. Escreva testes em `tests/test_<modulo>.py` (veja `tests/test_avaliacoes_listagem.py` como modelo).

## Quem faz o quê

| Pessoa    | Módulo | Arquivos que ela cria/edita |
|-----------|--------|-----------------------------|
| Murilo    | Base, login JWT, permissões, paginação e **4 listagens de avaliações** (prontos) | `security/`, `utils/`, `avaliacao_listagem_*` |
| Stephanie | CRUD de avaliações + associação às questões | `avaliacao_controller.py`, `avaliacao_service.py` |
| Allan     | Usuários: criar, atualizar, remover, listar, resetar e redefinir senha | `usuario_controller.py`, `usuario_service.py` |
| Lucas     | Cursos e disciplinas (CRUD, listagens, disciplinas por curso) | `curso_*`, `disciplina_*` |
| Felipe    | Questões (CRUD + listagem por disciplina), associação usuário↔curso/disciplina, ajuste do SQL | `questao_*`, `schema.sql` |
| Açucena   | Templates (CRUD) + geração do PDF a partir do template + testes no Postman | `template_*`, `avaliacao_pdf_*` |

> Para a senha padrão do reset (Allan), use `current_app.config["SENHA_PADRAO"]` (vem do `.env`).

## Pontos para o grupo decidir/confirmar

1. **`autor_id` em `questao` e `avaliacao`** (alteração proposta no `schema.sql`, marcada com comentário).
   Sem isso não dá para aplicar "só o autor ou admin altera/apaga" nem "não remover usuário que
   tenha questões ou avaliações". Os models já estão assim.
2. **SGBD:** o `schema.sql` usa `INTEGER PRIMARY KEY` (autoincrementa no SQLite). Se o grupo
   escolher MySQL ou PostgreSQL, troque por `AUTO_INCREMENT` / `SERIAL`, preencha `DB_*` no
   `.env` e instale o driver (`pymysql` ou `psycopg2-binary`).
3. **Confirmar com o professor** se o TDE2 e a AV2 entram juntos na entrega de 29/11 (os dois
   PDFs descrevem funcionalidades diferentes, com o mesmo prazo).
