# 📈 INOA - Monitoramento de Ativos

Este projeto é um sistema para monitorar ativos da B3, coletando preços periodicamente e enviando alertas por e-mail.

## 🚀 Como Rodar o Projeto

### **1️⃣ Clone o Repositório**

```bash
  git clone https://github.com/Luccascarpa/inoa-monitoramento-ativos.git
  cd inoa-monitoramento-ativos
```

### **2️⃣ Configure as Variáveis de Ambiente**

Crie um arquivo `.env` na raiz do projeto com:

```env
EMAIL_HOST_USER=seu-email@gmail.com
EMAIL_HOST_PASSWORD=sua-senha
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
CELERY_BROKER_URL=redis://redis:6379/0
DJANGO_SECRET_KEY=sua-chave-secreta
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

## 📊 Como Usar

### **1️⃣ Criar um Usuário Admin**

```bash
docker-compose exec web python manage.py createsuperuser
```

Acesse `http://127.0.0.1:8000/admin` e faça login.

### **2️⃣ Endpoints Disponíveis**
Além do Django Admin, os seguintes endpoints estão disponíveis:

- `GET /monitoring/` → Listar todos os ativos
- `POST /monitoring/create/` → Criar um novo ativo
- `GET /monitoring/<id>/edit/` → Editar um ativo específico
- `POST /monitoring/<id>/delete/` → Excluir um ativo

> ⚡ Esses endpoints permitem gerenciar os ativos diretamente via interface web ou API.

### **3️⃣ Testar a Coleta de Preços**

```bash
docker-compose exec web python manage.py shell
```

```python
from monitoring.tasks import check_asset_price_task
check_asset_price_task.apply_async(kwargs={"asset_id": 1})
```

### **4️⃣ Monitorar Logs**

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
- [ ] E-mails sendo enviados

Desenvolvido por [Lucca Scarpa](https://github.com/Luccascarpa) 🚀

