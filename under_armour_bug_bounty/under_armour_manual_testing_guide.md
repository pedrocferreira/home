# 🕵️ Guia de Testes Manuais - Under Armour Bug Bounty

## 🎯 Estratégia Alternativa: Testes Manuais

### **Situação Atual:**
- ✅ Proteção anti-bot detectada (HTTP 418)
- ✅ Scripts automatizados bloqueados
- ✅ Necessário usar abordagem manual

---

## 🌐 **Passo 1: Testes com Navegador**

### **1.1 Acessar o Site**
1. Abra o navegador (Chrome/Firefox)
2. Acesse: `https://www.underarmour.com`
3. Faça login com suas credenciais:
   - **Email**: pedroocferreira@gmail.com
   - **Senha**: @Pedro9cce22f2

### **1.2 Descobrir Endpoints**
1. Abra **DevTools** (F12)
2. Vá para a aba **Network**
3. Navegue pelas seções do site:
   - Perfil do usuário
   - Treinos/Workouts
   - Pedidos/Orders
   - Fotos/Media

### **1.3 Identificar Requisições**
Procure por requisições que contenham:
- `/api/`
- `/user/`
- `/profile/`
- `/workouts/`
- `/orders/`
- `/photos/`

---

## 🔧 **Passo 2: Testes com Burp Suite**

### **2.1 Configuração do Burp**
1. Abra o Burp Suite
2. Configure o proxy (127.0.0.1:8080)
3. Configure o navegador para usar o proxy
4. Ative o **Intercept**

### **2.2 Interceptar Requisições**
1. Navegue pelo site da Under Armour
2. Intercepte requisições interessantes
3. Modifique IDs nos parâmetros
4. Envie requisições modificadas

### **2.3 Testes de BAC Horizontal**
Para cada requisição interceptada:
```
# Exemplo de modificação:
GET /api/user/profile?id=123
# Modificar para:
GET /api/user/profile?id=124
GET /api/user/profile?id=125
GET /api/user/profile?id=999
```

---

## 🎯 **Passo 3: Endpoints Prioritários**

### **3.1 Dados de Perfil**
```
/api/user/profile?id=123
/api/profile/123
/api/athlete/123
/api/user/123
/api/me
/api/account
```

### **3.2 Treinos/Workouts**
```
/api/workouts/user/123
/api/training/123
/api/exercise/123
/api/sessions/123
```

### **3.3 Pedidos/Orders**
```
/api/orders/123
/api/purchases/123
/api/checkout/123
/api/payment/123
```

### **3.4 Fotos/Media**
```
/api/photos/user/123
/api/media/123
/api/gallery/123
/api/images/123
```

---

## 🔍 **Passo 4: Técnicas de Teste**

### **4.1 Incremento Sequencial**
- Teste IDs: 1, 2, 3, 4, 5...
- Teste IDs: 100, 101, 102...
- Teste IDs: 1000, 1001, 1002...

### **4.2 IDs Específicos**
- ID do seu próprio usuário
- IDs de usuários conhecidos
- IDs administrativos (1, 0, -1)

### **4.3 Parâmetros Alternativos**
```
?id=123
&user_id=123
&uid=123
&user=123
&profile_id=123
```

---

## 📋 **Passo 5: Sinais de Vulnerabilidade**

### **✅ BAC Horizontal Encontrado:**
- **HTTP 200** com dados de outro usuário
- **Dados pessoais** expostos (nome, email, endereço)
- **Treinos** de outros usuários
- **Pedidos** de outros usuários
- **Fotos** de outros usuários

### **❌ Protegido:**
- **HTTP 403** Forbidden
- **HTTP 401** Unauthorized
- **HTTP 404** Not Found
- **Mensagem de erro** "Access denied"

---

## 🚀 **Passo 6: Próximos Passos**

### **6.1 Documentar Descobertas**
1. **Screenshot** da vulnerabilidade
2. **URL** completa da requisição
3. **Response** completa
4. **Dados** expostos

### **6.2 Preparar Relatório**
1. **Descrição** da vulnerabilidade
2. **Impacto** (P1/P2 conforme guia)
3. **Passos** para reproduzir
4. **Evidências** coletadas

---

## 🎯 **Foco Principal (Conforme Guia)**

### **Prioridade 1: BAC Horizontal**
- Acessar dados de outros usuários
- Modificar dados de outros usuários
- Excluir dados de outros usuários

### **Prioridade 2: Dados do Atleta**
- Treinos/Workouts
- Pedidos/Orders
- Fotos/Media
- Dados de perfil

---

## ⚠️ **Lembretes Importantes**

1. **NÃO** fazer ataques DoS ou Brute Force
2. **Focar** em BAC Horizontal (P1/P2)
3. **Proteger** dados do atleta
4. **Documentar** todas as descobertas
5. **Respeitar** o escopo do programa

---

## 🔧 **Ferramentas Recomendadas**

1. **Burp Suite** (Professional/Community)
2. **OWASP ZAP**
3. **Browser DevTools**
4. **Postman** (para testes manuais)
5. **curl** (para testes rápidos)

---

## 📞 **Suporte**

Se encontrar dificuldades:
1. Verifique se está logado corretamente
2. Confirme que está no escopo do programa
3. Teste com diferentes navegadores
4. Use diferentes User-Agents
5. Tente em horários diferentes

**Boa sorte na caça aos bugs! 🐛🎯**
