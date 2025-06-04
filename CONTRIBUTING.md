# Contributing Guidelines

Obrigado por considerar contribuir com este projeto de MicroSaaS de Cobrança P2P. Para manter a qualidade e a organização do código, estabelecemos as seguintes diretrizes de contribuição. Por favor, leia atentamente antes de enviar qualquer alteração.

## 📦 Pré-requisitos

- Python 3.11+
- Docker e Docker Compose
- PostgreSQL
- Virtualenv ou equivalente
- Familiaridade com Django, Django Rest Framework, Celery

## 🛠️ Setup do Ambiente de Desenvolvimento

1. Clone o repositório:

```bash
git clone <URL-DO-REPOSITORIO>
cd <NOME-DO-PROJETO>
```

2. Copie o arquivo de variáveis de ambiente e configure:

```bash
cp .env.example .env
```

3. Suba os serviços com Docker Compose:

```bash
docker-compose up --build
```

4. Acesse o container `web` e aplique as migrações:

```bash
docker-compose exec web python manage.py migrate
```

5. Crie um superusuário (opcional):

```bash
docker-compose exec web python manage.py createsuperuser
```

## 📄 Convenções de Código

- Seguir PEP8 rigorosamente.
- Utilizar `black` para formatação automática.
- Ordenar imports com `isort`.
- Manter consistência no uso de tipagem estática (`type hints`).
- Comentários e docstrings obrigatórios para métodos públicos.

## 🔀 Fluxo de Branches

- `main`: branch protegida, sempre pronta para produção.
- `develop`: branch de integração, onde as novas funcionalidades são unificadas.
- `feature/*`: para desenvolvimento de novas funcionalidades.
- `bugfix/*`: para correção de bugs.
- `hotfix/*`: para correções urgentes em produção.

## ✅ Requisitos para Pull Requests

Antes de enviar um Pull Request (PR):

1. Certifique-se de que os testes estão passando:

```bash
docker-compose exec web pytest
```

2. Execute o linter:

```bash
docker-compose exec web black . && isort .
```

3. Atualize a documentação relevante, se aplicável.
4. Descreva claramente a motivação e a solução no corpo do PR.
5. Relacione o PR à issue correspondente.

## 📝 Padrão de Commits

Utilizamos **Conventional Commits**:

- `feat`: nova funcionalidade
- `fix`: correção de bug
- `docs`: alteração na documentação
- `style`: formatação, sem alteração de código
- `refactor`: refatoração de código
- `test`: adição ou alteração de testes
- `chore`: tarefas de manutenção

Exemplo:

```
feat: implementar autenticação via Djoser
```

## 🔒 Qualidade e Segurança

- Não exponha dados sensíveis em commits, PRs ou logs.
- Variáveis de ambiente devem ser configuradas apenas em `.env`, nunca em arquivos versionados.
- Submeta código com foco em segurança, principalmente relacionado a autenticação, autorização e validação de dados.

## 🚨 Revisão de Código

Todos os Pull Requests serão revisados por pelo menos um mantenedor do projeto, que avaliará:

- Aderência aos padrões de código.
- Cobertura de testes.
- Clareza e objetividade da descrição.
- Impacto na base de código existente.

## 📢 Comunicação

Em caso de dúvidas ou sugestões:

- Abrir uma **Issue** no GitHub com a devida descrição.
- Marcar os responsáveis pela área afetada.
- Evitar comunicação fora dos canais oficiais.

## 🤝 Código de Conduta

Este projeto adota um Código de Conduta baseado na [Contributor Covenant](https://www.contributor-covenant.org/).  
Todos os colaboradores devem manter um ambiente colaborativo, respeitoso e inclusivo.

**Agradecemos sua contribuição e empenho para manter este projeto seguro, robusto e sustentável.**  

**Equipe MicroSaaS Cobrança P2P**
