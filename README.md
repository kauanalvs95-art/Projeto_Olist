# API da Biblioteca

API REST de uma biblioteca que armazena **autores** e **livros**. Foi construída como solução do desafio de backend [Work at Olist](https://github.com/olist/work-at-olist).

## Funcionalidades

- Importação de autores a partir de um arquivo CSV (mais de um milhão de linhas) com um script de linha de comando.
- Listagem paginada de autores, com busca opcional por nome.
- CRUD completo de autores e de livros.
- Um livro pode ter mais de um autor (relacionamento muitos-para-muitos).
- Livros podem ser filtrados por nome, edição, ano de publicação e autor. Todos os filtros são opcionais e podem ser combinados.
- Testes automatizados que rodam em um banco em memória, então nunca encostam nos dados reais.

## Tecnologias

| Área | Ferramenta |
| --- | --- |
| Linguagem | Python 3.14 |
| Framework web | FastAPI |
| ORM | SQLAlchemy 2 |
| Banco de dados | PostgreSQL 18 (driver psycopg 3) |
| Containers | Docker Compose (PostgreSQL e Adminer) |
| Testes | pytest, httpx |
| Dados de teste | Faker |

## Estrutura do projeto

```
.
├── app/
│   ├── main.py          # aplicação FastAPI
│   ├── database.py      # engine, sessão e dependência get_db
│   ├── models/          # modelos SQLAlchemy (Author, Book)
│   ├── schemas/         # schemas Pydantic (entrada e saída)
│   └── routes/          # endpoints de autores e livros
├── scripts/
│   ├── create_tables.py     # cria as tabelas do banco
│   ├── import_authors.py    # importa autores de um arquivo CSV
│   └── generate_test_csv.py # gera um CSV com nomes de autores falsos
├── tests/               # testes com pytest
├── docker-compose.yml
├── .env.example
└── requirements.txt
```

## Instalação

### 1. Clone o repositório e crie um ambiente virtual

```bash
git clone <url-do-repositorio>
cd <pasta-do-repositorio>
python -m venv venv
source venv/bin/activate        # Windows (PowerShell): venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Abra o `.env` e preencha com os seus próprios valores. O mesmo usuário, senha e nome de banco devem ser usados nas variáveis `POSTGRES_*` e na `DATABASE_URL`.

| Variável | Descrição |
| --- | --- |
| `POSTGRES_USER` | Usuário do banco (lida pelo Docker Compose) |
| `POSTGRES_PASSWORD` | Senha do banco (lida pelo Docker Compose) |
| `POSTGRES_DB` | Nome do banco (lida pelo Docker Compose) |
| `DATABASE_URL` | String de conexão usada pela aplicação |

Exemplo:

```
POSTGRES_USER=usuario
POSTGRES_PASSWORD=senha
POSTGRES_DB=nome_do_banco
DATABASE_URL=postgresql://usuario:senha@localhost:5432/nome_do_banco
```

O arquivo `.env` é ignorado pelo Git. Nunca faça commit dele.

> **Atenção:** o PostgreSQL só lê `POSTGRES_PASSWORD` na primeira vez que o volume é criado. Se você mudar a senha no `.env` depois disso, ela não muda no banco. Para trocar, use `ALTER USER usuario PASSWORD 'nova_senha';` ou apague o volume com `docker compose down -v` (isso apaga os dados).

### 3. Suba o banco de dados

Com Docker:

```bash
docker compose up -d
```

Isso inicia o PostgreSQL na porta `5432` e o [Adminer](https://www.adminer.org/) (interface web para o banco) na porta `8080`.

**Sem Docker:** instale o PostgreSQL localmente, crie um banco e um usuário, e aponte a `DATABASE_URL` do `.env` para ele. Nada mais muda.

### 4. Crie as tabelas

```bash
python -m scripts.create_tables
```

## Rodando a API

```bash
uvicorn app.main:app --reload
```

A documentação interativa (Swagger UI) fica em <http://127.0.0.1:8000/docs>.

## Importando autores de um arquivo CSV

O arquivo CSV deve ter uma única coluna chamada `name`, com um autor por linha:

```
name
Luciano Ramalho
Osvaldo Santana Neto
David Beazley
```

Rode a importação a partir da raiz do projeto:

```bash
python -m scripts.import_authors caminho/para/autores.csv
```

O script lê o arquivo linha a linha e insere os autores em lotes de 10.000 registros usando inserção em massa (*bulk insert*). Isso mantém o uso de memória baixo e evita um `INSERT` e um `COMMIT` por autor.

**Resultado:** a importação de um arquivo com **1.000.000 de autores levou cerca de 12 segundos** na minha máquina (veja a seção Ambiente, abaixo).

Para gerar um arquivo de teste com nomes falsos, use `scripts/generate_test_csv.py` (precisa do `Faker`, que está no `requirements.txt`). O nome do arquivo de saída e a quantidade de linhas são definidos dentro do script. Arquivos CSV são ignorados pelo Git.

> **Atenção:** a tabela `authors` não exige nomes únicos, então importar o mesmo arquivo duas vezes cria duplicatas. Para recomeçar, rode `TRUNCATE authors RESTART IDENTITY CASCADE;` no banco.

## Endpoints da API

### Autores

| Método | Caminho | Descrição |
| --- | --- | --- |
| `POST` | `/authors/` | Cria um autor |
| `GET` | `/authors/` | Lista autores (paginado) |
| `GET` | `/authors/{author_id}` | Busca um autor |
| `PUT` | `/authors/{author_id}` | Atualiza um autor |
| `DELETE` | `/authors/{author_id}` | Remove um autor |

Parâmetros de consulta do `GET /authors/`:

| Parâmetro | Padrão | Descrição |
| --- | --- | --- |
| `author_name` | nenhum | Busca parcial, sem diferenciar maiúsculas de minúsculas, no nome do autor |
| `skip` | `0` | Quantidade de registros a pular |
| `limit` | `10` | Quantidade máxima de registros retornados |

Criar ou atualizar um autor:

```json
{
  "name": "Machado de Assis"
}
```

### Livros

| Método | Caminho | Descrição |
| --- | --- | --- |
| `POST` | `/books/` | Cria um livro |
| `GET` | `/books/` | Lista livros (paginado, com filtros opcionais) |
| `GET` | `/books/{book_id}` | Busca um livro |
| `PUT` | `/books/{book_id}` | Atualiza um livro |
| `DELETE` | `/books/{book_id}` | Remove um livro |

Criar ou atualizar um livro. O campo `authors` é uma lista de ids de autores, ou seja, os ids de autores que já existem no banco:

```json
{
  "name": "Dom Casmurro",
  "edition": "1ª edição",
  "publication_year": 1899,
  "authors": [1]
}
```

A resposta traz os autores completos, não apenas os ids:

```json
{
  "id": 1,
  "name": "Dom Casmurro",
  "edition": "1ª edição",
  "publication_year": 1899,
  "authors": [
    { "id": 1, "name": "Machado de Assis" }
  ]
}
```

Se algum id em `authors` não existir, a API retorna `404` com a mensagem `Author not found`, e o livro não é criado nem alterado.

Parâmetros de consulta do `GET /books/` (todos opcionais e combináveis):

| Parâmetro | Descrição |
| --- | --- |
| `name` | Busca parcial, sem diferenciar maiúsculas de minúsculas, no nome do livro |
| `edition` | Busca parcial, sem diferenciar maiúsculas de minúsculas, na edição |
| `publication_year` | Ano de publicação exato |
| `authors_name` | Busca parcial, sem diferenciar maiúsculas de minúsculas, no nome de qualquer autor do livro |
| `skip` | Quantidade de registros a pular (padrão `0`) |
| `limit` | Quantidade máxima de registros retornados (padrão `10`) |

Sem nenhum filtro, o endpoint retorna todos os livros, paginados.

## Rodando os testes

```bash
python -m pytest -v
```

Os testes usam um banco SQLite em memória. A dependência `get_db` da aplicação é substituída durante os testes, então o PostgreSQL real nunca é usado e cada teste começa com as tabelas vazias. Não é preciso ter o Docker rodando.

A suíte tem 20 testes, que cobrem:

- Criar, ler, atualizar e remover autores e livros.
- Paginação e busca de autores.
- Paginação e cada filtro de livros (nome, ano de publicação e autor), além da listagem sem filtros.
- Respostas `404` para autores e livros que não existem.
- Rejeição de livros que referenciam autores inexistentes, tanto na criação quanto na atualização.

## Decisões de projeto

- **Relacionamento muitos-para-muitos:** livros e autores são ligados por uma tabela de associação (`relationships`), criada junto com as demais tabelas.
- **Importação em massa, em lotes:** o CSV é lido aos poucos e inserido 10.000 linhas por vez, em vez de carregar o arquivo inteiro na memória ou fazer commit linha a linha.
- **Paginação estável:** as listagens são ordenadas por `id` antes de aplicar `skip` e `limit`. Sem uma ordem explícita, o PostgreSQL não garante a ordem das linhas, e um registro poderia aparecer duas vezes ou ser pulado entre uma página e outra.
- **Filtro por autor sem duplicatas:** o filtro por autor nos livros usa `EXISTS` (`any()` no SQLAlchemy) em vez de `JOIN`, então um livro com vários autores que combinam com a busca aparece só uma vez.
- **Schemas separados para entrada e saída:** os schemas de entrada recebem uma lista de ids de autores, e os de saída devolvem os objetos completos dos autores.
- **Configuração por variáveis de ambiente:** as credenciais não ficam no código nem no `docker-compose.yml`, seguindo a abordagem do [12-Factor App](https://12factor.net).

## Limitações conhecidas

- A busca de autores usa `ILIKE '%texto%'`, que não consegue aproveitar um índice comum. Com um milhão de autores, ela varre a tabela inteira. Um índice trigram (`pg_trgm`) aceleraria a busca.
- A paginação com `OFFSET` fica mais lenta em páginas muito profundas de tabelas grandes.

## Ambiente

O projeto foi desenvolvido e testado neste ambiente:

- Arch Linux
- Python 3.14
- Docker e Docker Compose
- PostgreSQL 18
- Visual Studio Code
- Principais bibliotecas: FastAPI, SQLAlchemy, Pydantic, psycopg, pytest, httpx, Faker (veja o `requirements.txt`)
