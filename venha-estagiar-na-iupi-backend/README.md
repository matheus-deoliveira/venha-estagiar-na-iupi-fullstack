# Controle de Despesas (Backend Challenge - IUPI)

API REST desenvolvida para o desafio técnico de estágio Backend na IUPI. O sistema gerencia transações financeiras (entradas e saídas) com autenticação segura, isolamento de dados por usuário e relatórios consolidados.

## Stack Tecnológica

* **Linguagem:** Python 3.12+
* **Framework:** Django 5.x
* **API Toolkit:** Django REST Framework (DRF)
* **Auth:** SimpleJWT (Autenticação via Token)
* **Banco de Dados:** SQLite (Padrão para desenvolvimento)
* **Ferramentas:** Insomnia (Testes de API)

## Arquitetura e Decisões de Projeto

Para garantir a escalabilidade e a manutenibilidade do código, optei por refatorar a estrutura padrão do Django, utilizando **Modularização de Pacotes**:

* **Models, Views e Serializers:** Em vez de arquivos únicos gigantes (`models.py`), foram transformados em pacotes (pastas) com módulos específicos (`core/models/transaction.py`, etc.). Isso facilita a leitura e evita conflitos em times grandes.
* **Lógica de Negócio:**
    * **CRUD:** Implementado com `ModelViewSet` para produtividade e padronização.
    * **Resumo (/summary):** Implementado com `APIView` e otimizado com `aggregate` do banco de dados para evitar processamento excessivo em memória.
    * **Filtros:** Busca textual (`icontains`) e filtro exato por tipo implementados via sobrescrita do `get_queryset`.

## Como Rodar o Projeto

### Pré-requisitos
* Python instalado.
* Git instalado.

### Passo a Passo

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/matheus-deoliveira/venha-estagiar-na-iupi-backend
    cd venha-estagiar-na-iupi-backend
    ```

2.  **Crie e ative o ambiente virtual:**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\Activate
    ```
    ```bash
    # Linux/Mac
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute as migrações (Banco de Dados):**
    ```bash
    python manage.py migrate
    ```

5.  **Crie um Usuário (Obrigatório para Login):**
    ```bash
    python manage.py createsuperuser
    # Siga as instruções para definir username e senha
    ```

6.  **Inicie o servidor:**
    ```bash
    python manage.py runserver
    ```

A API estará disponível em: `http://127.0.0.1:8000/api/`

## Como usar (Autenticação)

**Esta API é protegida.** Para acessar qualquer rota, você precisa de um Token JWT.

1. **Obter Token (Login):**
    - Faça um POST em `/login/` com seu `username` e `password`.
    - A resposta conterá um token `access`.

2. **Acessar Rotas:**
    - Em todas as requisições subsequentes, adicione o cabeçalho: `Authorization: Bearer <SEU_TOKEN_ACCESS>`

## Testando a API

### Endpoints Principais

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/login/` | Autenticação (Retorna Token JWT) |
| `GET` | `/api/transactions/` | Lista todas as transações (Paginado) |
| `POST` | `/api/transactions/` | Cria nova transação |
| `PUT` | `/api/transactions/:id/` | Atualiza transação completa (Substitui tudo) |
| `PATCH`| `/api/transactions/:id/` | Atualiza parcialmente (ex: mudar só o valor) |
| `DELETE`| `/api/transactions/:id/` | Remove uma transação |
| `GET` | `/api/transactions/?type=income` | Filtra por tipo (income/expense) |
| `GET` | `/api/transactions/?description=termo` | Filtra por descrição (busca parcial) |
| `GET` | `/api/transactions/?type=expense&description=uber` | **Filtro Combinado:** Tipo E Descrição juntos |
| `GET` | `/api/summary/` | Retorna o balanço total consolidado |
| `POST` | `/api/populate/` | **(Debug)** Cria 40 transações aleatórias para teste |

### Collection do Insomnia
Para facilitar os testes, o arquivo de coleção do Insomnia está incluído na raiz do projeto: `insomnia_collection.json`. Basta importar e testar.

## Rodando os Testes

Para verificar a integridade da aplicação e a segurança (Cobertura de testes nas regras de negócio):

```bash
python manage.py test