# 🏦 Nubank Bug Bounty - Estratégia de Testes

## 🎯 **ALVOS PRIORITÁRIOS (P1: $2000-$4000)**

### **1. Aplicações Móveis (Android/iOS)**
- **Foco**: BAC em transações financeiras
- **Recompensa**: $2000-$4000
- **Prioridade**: MÁXIMA

### **2. APIs de Produção**
- **Domínio**: `prod-*.nubank.com.br`
- **Foco**: Injeções de alto impacto
- **Alvos**: SQLi, Code Injection, SSRF

### **3. Plataforma de Investimentos**
- **Domínio**: `*.nuinvest.com.br`
- **Foco**: Lógica de investimentos
- **Recompensa**: $500-$1000

---

## 🚨 **VULNERABILIDADES DE MAIOR IMPACTO**

### **A. BAC (Broken Access Control) - PRIORIDADE 1**

#### **Cenários de Teste:**
1. **Transferências Não Autorizadas**
   ```
   - Tentar transferir dinheiro sem token de autenticação
   - Modificar parâmetros de conta origem/destino
   - Bypass da senha de 4 dígitos
   - Bypass da biometria
   ```

2. **Ajuste de Limite Sem Autorização**
   ```
   - Aumentar limite de cartão sem aprovação
   - Modificar limite de PIX
   - Alterar limite de TED/DOC
   ```

3. **Pagamentos em Nome de Terceiros**
   ```
   - Pagar boletos com conta de outro usuário
   - Fazer PIX usando dados de terceiros
   - Confirmar pagamentos sem autorização
   ```

#### **Endpoints Críticos para Testar:**
```
POST /api/transfers
POST /api/payments
POST /api/pix
PUT /api/limits
POST /api/cards/transactions
GET /api/account/balance
```

---

### **B. IDOR (Insecure Direct Object Reference) - PRIORIDADE 2**

#### **Técnicas de Teste:**
1. **Manipulação de IDs Sequenciais**
   ```bash
   # Exemplo de teste
   GET /api/transactions/123456
   GET /api/transactions/123457  # Testar ID +1
   GET /api/transactions/123455  # Testar ID -1
   ```

2. **IDs de Contas e Usuários**
   ```bash
   GET /api/accounts/user123
   GET /api/accounts/user124
   GET /api/profile/456
   GET /api/statements/789
   ```

3. **IDs de Investimentos**
   ```bash
   GET /api/investments/portfolio/123
   GET /api/nuinvest/positions/456
   ```

---

### **C. Race Conditions - PRIORIDADE 3**

#### **Cenários de Teste:**
1. **Duplicação de Transferências**
   ```python
   # Enviar múltiplas requisições simultâneas
   import threading
   import requests
   
   def transfer_money():
       requests.post('/api/transfers', json={
           'amount': 10.00,
           'destination': 'conta_destino'
       })
   
   # Executar simultaneamente
   for i in range(5):
       threading.Thread(target=transfer_money).start()
   ```

2. **Bypass de Limites**
   ```python
   # Tentar exceder limite com requisições simultâneas
   def pix_transfer():
       requests.post('/api/pix', json={
           'amount': 950.00  # Próximo do limite de R$ 1000
       })
   ```

---

## 🔧 **CONFIGURAÇÃO OBRIGATÓRIA**

### **Header Essencial:**
```http
X-Correlation-Id: bc-handle
```
**⚠️ CRÍTICO: Sempre incluir este header em todas as requisições!**

### **Limites de PoC:**
- **Valor máximo**: R$ 10,00
- **Usar conta real** com CPF válido
- **Não usar identificação falsa**

---

## 📱 **ESTRATÉGIA PARA MOBILE**

### **1. Interceptação de Tráfego**
```bash
# Configurar proxy (Burp Suite/OWASP ZAP)
# Interceptar todas as chamadas de API
# Focar em endpoints financeiros
```

### **2. Análise de Segurança**
- **Chaves hardcoded** no código
- **Tokens** armazenados inseguramente
- **Logs** com dados sensíveis
- **Certificados** pinning bypass

### **3. Endpoints Móveis Críticos**
```
/api/mobile/auth
/api/mobile/transactions
/api/mobile/balance
/api/mobile/pix
/api/mobile/cards
```

---

## 🚫 **EVITAR (FORA DO ESCOPO)**

### **❌ NÃO TESTAR:**
- **Subdomain Takeover**
- **DoS/DDoS**
- **Social Engineering**
- **CSRF** em formulários não sensíveis
- **Missing headers** (HttpOnly, Secure, CSP)
- **Open Redirect** (sem impacto adicional)
- **LLM Applications**

---

## 🎯 **FOCO PRINCIPAL**

### **Ordem de Prioridade:**
1. **BAC** em transações financeiras
2. **IDOR** em dados/fundos
3. **Race Conditions** em pagamentos
4. **Injeções** em APIs críticas
5. **Lógica de negócios** em investimentos

### **Impacto Desejado:**
- **Perda/roubo de fundos**
- **Acesso não autorizado a contas**
- **Bypass de limites financeiros**
- **Duplicação de transações**

---

## 📋 **CHECKLIST DE TESTE**

### **Antes de Começar:**
- [ ] Conta criada com CPF real
- [ ] Header X-Correlation-Id configurado
- [ ] Limite de R$ 10 respeitado
- [ ] Proxy configurado para mobile

### **Durante os Testes:**
- [ ] Focar em endpoints financeiros
- [ ] Testar BAC em cada transação
- [ ] Verificar IDOR em todos os IDs
- [ ] Documentar passos detalhados

### **Ao Encontrar Vulnerabilidade:**
- [ ] PoC com impacto real
- [ ] Passos de reprodução claros
- [ ] Valor máximo R$ 10
- [ ] Cenário de exploração descrito

---

*Criado para maximizar chances de encontrar vulnerabilidades P1 ($2000-$4000)*
