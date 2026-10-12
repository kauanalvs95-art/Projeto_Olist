# Projeto Olist — API REST para Livros e Autores

Projeto desenvolvido como desafio prático de backend, inspirado no desafio técnico disponibilizado pela [Olist](https://github.com/olist/work-at-olist).

O objetivo foi colocar em prática meus conhecimentos em desenvolvimento backend, construindo uma API REST para gerenciamento de livros e autores, com persistência em banco de dados relacional, operações CRUD, filtros de consulta e importação de dados por CSV.

Mais do que desenvolver um projeto para meu portfólio, utilizei esse desafio como uma oportunidade de estudar, enfrentar problemas reais de desenvolvimento e aprimorar minhas habilidades com Python e construção de APIs.

## Objetivos do projeto

- Desenvolver uma API REST utilizando Python e FastAPI.
- Implementar operações CRUD para livros e autores.
- Modelar relacionamentos entre entidades em um banco de dados relacional.
- Implementar filtros e paginação nas consultas.
- Criar um processo de importação de autores por arquivos CSV, utilizando processamento em lotes.
- Praticar organização de código, validação de dados e testes automatizados.

## Tecnologias utilizadas

- **Python** — linguagem de programação.
- **FastAPI** — desenvolvimento dos endpoints da API REST.
- **SQLAlchemy** — ORM para interação com o banco de dados.
- **Pydantic** — validação e estruturação dos dados de entrada e saída.
- **PostgreSQL** — banco de dados relacional.
- **Docker Compose** — configuração do ambiente de banco de dados.
- **Pytest** — testes automatizados.
- **SQLite** — banco de dados em memória utilizado nos testes.
- **Uvicorn** — servidor ASGI para executar a aplicação.

## Funcionalidades

### Autores

- Cadastro de autores.
- Consulta de um autor pelo ID.
- Listagem de autores com paginação.
- Busca de autores pelo nome.
- Atualização de informações.
- Exclusão de autores.

### Livros

- Cadastro de livros associados a um ou mais autores.
- Consulta de um livro pelo ID.
- Listagem de livros com paginação.
- Filtros por nome, edição, ano de publicação e nome do autor.
- Atualização das informações de um livro e de seus autores associados.
- Exclusão de livros.

### Importação de autores por CSV

O projeto possui um script para importar autores de um arquivo CSV com a coluna `name`.

A importação utiliza lotes de até 10.000 registros, buscando reduzir a sobrecarga de executar operações individuais para cada autor.

## Estrutura do projeto

```text
Projeto_Olist/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   │   ├── author.py
│   │   └── book.py
│   ├── routes/
│   │   ├── author.py
│   │   └── book.py
│   └── schemas/
│       ├── author.py
│       └── book.py
├── scripts/
│   ├── create_tables.py
│   └── import_authors.py
├── tests/
├── .env.example
├── docker-compose.yml
└── requirements.txt
```

## Como executar o projeto

### Pré-requisitos

- Python instalado em uma versão compatível com as dependências.
- Docker e Docker Compose.
- Git.

### 1. Clone o repositório

```bash
git clone https://github.com/kauanalvs95-art/Projeto_Olist.git
cd Projeto_Olist
```

### 2. Crie um ambiente virtual

```bash
python -m venv .venv
```

Ative o ambiente virtual:

**Linux:**

```bash
source .venv/bin/activate
```

**Windows:**

```powershell
.venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie o arquivo `.env` a partir do exemplo disponibilizado:

```bash
cp .env.example .env
```

Configure as variáveis de conexão com o PostgreSQL de acordo com seu ambiente. Os valores de usuário, senha e banco de dados precisam corresponder aos configurados no Docker Compose.

### 5. Inicie o banco de dados

```bash
docker compose up -d db
```

### 6. Crie as tabelas

Com o banco de dados disponível e o arquivo `.env` configurado, execute:

```bash
python -m scripts.create_tables
```

### 7. Execute a API

```bash
uvicorn app.main:app --reload
```

A API estará disponível localmente em:

`http://127.0.0.1:8000`

## Documentação da API

O FastAPI disponibiliza documentação interativa para consultar e testar os endpoints.

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

## Exemplos de utilização

### Criar um autor

**POST** `/authors/`

```json
{
  "name": "Machado de Assis"
}
```

### Listar autores

**GET** `/authors/?skip=0&limit=10`

Para pesquisar pelo nome:

**GET** `/authors/?author_name=Machado`

### Criar um livro

**POST** `/books/`

```json
{
  "name": "Dom Casmurro",
  "edition": "1st",
  "publication_year": 1899,
  "authors": [1]
}
```

O campo `authors` recebe uma lista de IDs de autores previamente cadastrados.

### Consultar livros com filtros

**GET** `/books/?name=Dom&publication_year=1899`

Também é possível utilizar os parâmetros `edition` e `authors_name`, além dos parâmetros `skip` e `limit` para paginação.

### Atualizar e excluir registros

- **PUT** `/books/{book_id}` — atualiza um livro.
- **DELETE** `/books/{book_id}` — exclui um livro.
- **PUT** `/authors/{author_id}` — atualiza um autor.
- **DELETE** `/authors/{author_id}` — exclui um autor.

## Importação de autores

Prepare um arquivo CSV com a coluna `name` e os nomes dos autores:

```csv
name
Machado de Assis
José de Alencar
Clarice Lispector
```

Execute o comando na raiz do projeto:

```bash
python -m scripts.import_authors caminho/do/arquivo.csv
```

O script processa os registros em lotes e informa a quantidade de autores importados.

## Testes automatizados

Os testes utilizam Pytest e um banco SQLite em memória, permitindo validar as operações da API sem depender de uma instância do PostgreSQL para a execução da suíte de testes.

Para executar os testes, utilize:

```bash
pytest
```

Os testes contemplam operações CRUD, consultas com filtros, paginação e tratamento de registros inexistentes ou de referências a autores inválidos.

## Aprendizados

O desenvolvimento deste projeto foi uma oportunidade para aprofundar meus conhecimentos em:

- Construção e organização de APIs REST com FastAPI.
- Mapeamento objeto-relacional com SQLAlchemy.
- Modelagem de relacionamentos muitos-para-muitos.
- Validação de dados com Pydantic.
- Integração com PostgreSQL e configuração por variáveis de ambiente.
- Importação de dados em lotes.
- Escrita de testes automatizados com Pytest.
- Organização de um projeto backend e documentação técnica.

## Sobre o projeto

Este projeto foi desenvolvido individualmente como um desafio de aprendizado, com base nos requisitos do desafio técnico da Olist.

**Repositório:** [Projeto_Olist — GitHub](https://github.com/kauanalvs95-art/Projeto_Olist)

O projeto representa parte da minha jornada de aprendizado em desenvolvimento backend e meu interesse em evoluir por meio da prática, da resolução de problemas e da construção de aplicações reais.
