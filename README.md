
# Micro SaaS — Plataforma de Cobranças P2P

Este projeto é uma plataforma SaaS para que **pessoas físicas possam realizar cobranças** de outras pessoas físicas, seja por serviços, produtos ou empréstimos.  
Desenvolvido em **Python** com **Django**, utilizando arquitetura moderna baseada em containers Docker.

## 🚀 Tecnologias e Ferramentas

- **Python** 3.11
- **Django** 4.x
- **PostgreSQL** (persistência de dados)
- **Redis** (broker para Celery)
- **Celery** (execução assíncrona de tarefas)
- **Poetry** (gerenciamento de dependências)
- **Docker + Docker Compose** (containerização)
- **pre-commit** (boas práticas e qualidade de código)
  - `flake8` — análise de código
  - `black` — formatação automática
  - `isort` — organização de imports
- **pytest** — framework de testes
- **Sentry** — monitoramento de erros em produção
- **Djoser** — autenticação com API REST
- **CustomUser** — autenticação via CPF

## 🗂️ Estrutura do Projeto

```
/app
  /project
  /users
  /core
docker-compose.yml
pyproject.toml
.pre-commit-config.yaml
Makefile
```

## ✅ Funcionalidades Implementadas

- ✅ Autenticação via **DRF + Djoser** utilizando **CPF** como campo de login
- ✅ Estrutura de **CustomUser** com campos específicos: CPF, email, telefone, endereço, etc.
- ✅ Execução assíncrona com **Celery + Redis**
- ✅ **Pre-commit hooks** com `flake8`, `black`, `isort`
- ✅ Testes automatizados com **pytest**
- ✅ Monitoramento de erros com **Sentry**
- ✅ Ambiente totalmente containerizado com **Docker Compose**
- ✅ Makefile com comandos automatizados

## ⚙️ Como rodar o projeto

### ✅ 1. Clone o repositório

```bash
git clone https://github.com/seu_usuario/seu_projeto.git
cd seu_projeto
```

### ✅ 2. Configure o `.env`

Adicione as variáveis de ambiente necessárias, como:  

```env
POSTGRES_DB=
POSTGRES_USER=
POSTGRES_PASSWORD=
SENTRY_DSN=
```

### ✅ 3. Suba os containers

```bash
docker-compose up --build
```

### ✅ 4. Acesse

- Django: http://localhost:8000  
- Admin: http://localhost:8000/admin  
- API: http://localhost:8000/api/

## ✅ Comandos úteis

```bash
make run            # Executa o servidor Django
make migrate        # Aplica as migrations
make createsuperuser # Cria um superusuário
make worker         # Inicia o worker Celery
make test           # Executa os testes com pytest
make lint           # Roda o flake8 para análise de código
make build          # Builda as imagens Docker
```

## ✅ Teste do pre-commit

Já configurado para rodar automaticamente `flake8`, `black` e `isort` a cada commit.

Se quiser rodar manualmente:

```bash
pre-commit run --all-files
```

## ✅ Testando Sentry

Para verificar a integração com Sentry:

```bash
docker-compose run web poetry run python manage.py shell
```

```python
import sentry_sdk
sentry_sdk.capture_message("Teste: integração com Sentry funcionando!")
```

## 📝 Considerações

Este projeto foi desenvolvido como um **MVP** (Produto Mínimo Viável) e possui estrutura robusta para:

- Escalabilidade futura
- Extensão para mobile e frontend com Django ou outras stacks
- Ampliação para profissionais liberais e pequenas empresas

## 🤝 Contribuição

Sinta-se à vontade para abrir **issues** ou enviar **pull requests**!

## 📄 Licença

Este projeto está licenciado sob a **MIT License**.
