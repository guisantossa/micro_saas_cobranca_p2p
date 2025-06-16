# 📌 MicroSaaS de Cobrança P2P — ROADMAP PRÉ-LANÇAMENTO

---

## ✅ 1. Robustez e Segurança

- [ ] Revisar autenticação com Djoser: (deixar para quando tivermos registro)
  - Registro
  - Recuperação de senha
  - Confirmação de e-mail
- [ x] Garantir que só o dono da cobrança pode alterar/deletar
- [x ] Validar CPF (`validate-docbr` ou `cpf_cnpj`)
- [x ] Validar telefone no formato E.164 (Twilio)
- [x ] Garantir campos obrigatórios/documentação de erro
- [ x] Configurar logs para arquivo
- [x ] Configurar monitoramento com Sentry

---

## ✅ 2. Funcionalidades-Chave

- [x ] Criar painel de controle web:
  - Visualização de cobranças
  - CRUD completo
  - Status atualizado das notificações
- [ ] Implementar webhook de pagamento:
  - Definir gateway: MercadoPago, Stripe, Pagar.me
  - Ou implementar botão manual de “Confirmar Pagamento”
- [ x] Implementar política de reenvio de lembretes:
  - Definir após quantos dias reenvia
  - Ajustar tasks do Celery
- [x ] Definir o opt-in do cobrador autorizando a cobrança via zap

---

## ✅ 3. Templates e UX

- [ x] Criar templates de mensagens (WhatsApp e Email)
- [x ] Definir serviço de e-mail:
  - Mailgun, SES ou ***SendGrid***
- [ ] Autenticar domínio (SPF, DKIM)

---

## ✅ 4. Rate Limit e Antifraude

- [ ] Implementar fila controlada no Celery (rate limit)
- [ ] Garantir retry com backoff exponencial
- [ ] Criar limites para evitar spam:
  - Restringir número de cobranças por usuário/dia

---

## ✅ 5. Deployment Real

- [ ] Escolher ambiente: Heroku, Render ou AWS
- [ ] Configurar CI/CD (GitHub Actions ou similar)
- [ ] Banco de dados em produção (RDS?)
- [ ] Configurar backups e migração

---

## ✅ 6. Legal e Compliance

- [ ] Criar Política de Privacidade e Termos de Uso
- [ ] Implementar aceite de termos no onboarding
- [ ] Garantir compliance LGPD se for processar pagamento

---

## ✅ 7. Performance e Escalabilidade

- [ ] Rodar testes de carga (Locust ou k6)
- [ ] Separar ambientes: dev e prod
- [ ] Configurar múltiplos workers no Celery

---

## ✅ 8. Experiência do Usuário

- [ ] Criar notificações para cobrador:
  - “Cobrança enviada”
  - “Cobrança paga”
- [ ] Criar painel de métricas:
  - Total cobrado
  - Pendente
  - Pago
  - Histórico de envios

---

## ✅ 9. Testes Automatizados

- [ ] Configurar pytest e pytest-django
- [ ] Criar testes:
  - Modelos
  - Endpoints
  - Tasks do Celery

---

## ✅ 10. Documentação

- [ ] Melhorar README:
  - Setup de desenvolvimento
  - Execução das tasks
  - Configuração de ambiente
- [ ] Documentar API com DRF-Spectacular ou Swagger

---

## 🚀 RESUMO FINAL

| Status | Tarefa                                   |
|---------|-----------------------------------------|
| ✅       | Revisar autenticação                   |
| ✅       | Validações de dados                    |
| ✅       | Logs e monitoramento                   |
| ✅       | Painel web                             |
| ❌       | Webhook de pagamento                   |
| ❌       | Reenvio de lembretes                   |
| ❌       | Templates e personalização             |
| ✅       | Serviço de e-mail                      |
| ❌       | Rate limit e antifraude                |
| ❌       | Deploy real e CI/CD                    |
| ❌       | Legal e compliance                     |
| ❌       | Testes de carga                        |
| ❌       | Notificações pro cobrador              |
| ❌       | Testes automatizados                   |
| ❌       | Documentação                           |

---

## 🚨 Bora executar? Só marcar as checkboxes e subir!  
**O SaaS tá quase na pista, só falta dar aquele talento final.**  

Tamo junto até o lançamento, Guigas! 🚀💥  
