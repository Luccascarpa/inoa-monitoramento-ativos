# INOA - Monitoramento de Ativos

Este projeto é um sistema para monitorar ativos, coletando preços periodicamente de uma fonte pública e enviando alertas por e-mail.

## Como Rodar o Projeto

### **1️⃣ Clone o Repositório**

```bash
  git clone https://github.com/Luccascarpa/inoa-monitoramento-ativos.git
  cd inoa-monitoramento-ativos
  cd core
```

### **2️⃣ Configure as Variáveis de Ambiente**

Crie um arquivo `.env` na raiz do projeto (pasta core) com:

```env
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
CELERY_BROKER_URL=redis://redis:6379/0
DEFAULT_FROM_EMAIL=<seu-email@gmail.com>
EMAIL_HOST_PASSWORD=<senha-de-aplicação>
EMAIL_HOST_USER=seu-email@gmail.com>
```

### **3️⃣ Rode a Aplicação com Docker**

```bash
docker-compose up --build -d
```

Isso inicia:

- **Django** (servidor web)
- **Redis** (mensageria para Celery)
- **Celery Worker** (processador de tarefas)
- **Celery Beat** (agendador de tarefas)

---

## Como Usar

### **1️⃣ Criar um Usuário Admin**

```bash
docker-compose exec web python manage.py createsuperuser
```

Acesse `http://127.0.0.1:8000/admin` e faça login.

### **2️⃣ Cadastrar E-mail para Alertas**
- Acesse `http://127.0.0.1:8000/monitoring/alert-emails/` para ver a lista de e-mails cadastrados.
- Clique em "Adicionar Novo E-mail" para cadastrar um e-mail que receberá os alertas.
- Para remover um e-mail, clique no botão "Remover" ao lado do e-mail cadastrado.

Agora, todos os e-mails cadastrados receberão notificações quando um ativo cruzar os limites configurados.

### **3️⃣ Cadastrar Ativos**
- Acesse `http://127.0.0.1:8000/monitoring/`
- Adicione os ativos a serem monitorados
- Defina o intervalo de verificação e os limites de alerta

### **4️⃣ Endpoints Disponíveis**
Além do Django Admin, os seguintes endpoints estão disponíveis:

- `GET /monitoring/` → Listar todos os ativos
- `POST /monitoring/create/` → Criar um novo ativo
- `GET /monitoring/<id>/edit/` → Editar um ativo específico
- `POST /monitoring/<id>/delete/` → Excluir um ativo
- `GET /alert-emails/` → Listar todos os e-mails cadastrados
- `POST /alert-emails/create/` → Adicionar um novo e-mail
- `POST /alert-emails/delete/<id>/` → Remover um e-mail da lista

> ⚡ Esses endpoints permitem gerenciar os ativos e os destinatários dos alertas diretamente via interface web ou API.

### **5️⃣ Para Testar a Coleta de Preços pelo Terminal**

```bash
docker-compose exec web python manage.py shell
```

```python
from monitoring.tasks import check_asset_price_task
check_asset_price_task.apply_async(kwargs={"asset_id": 1})
```

### **6️⃣ PAra Monitorar Logs pelo Terminal** 

```bash
# Logs do Celery Worker
docker-compose logs --tail=50 celery

# Logs do Celery Beat
docker-compose logs --tail=50 celery-beat
```

---

## ✅ Verificações

- [ ] Aplicação rodando em `http://127.0.0.1:8000`
- [ ] Celery Worker e Beat ativos
- [ ] Prices sendo coletados corretamente
- [ ] E-mails sendo enviados para os usuários cadastrados

## Melhorias/próximos passos
- Controle de acesso para diferentes usuários, medidas de autenticação/segurança
- Gráficos para melhorar a visualização dos dados
- Melhorar a gestão dos erros na aplicação
- Restringir o cadastro de ativos a ativos existentes

Desenvolvido por [Lucca Scarpa](https://github.com/Luccascarpa) 🚀

