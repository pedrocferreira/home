# 📱 Guia Prático - Interceptação de APIs Móveis Nubank

## 🎯 **Configuração do Ambiente**

### **1. Burp Suite Setup**
```bash
# Configurar proxy
- IP: 127.0.0.1 (ou IP da máquina)
- Porta: 8080
- Habilitar "Support invisible proxying"
- Configurar certificado CA
```

### **2. Dispositivo/Emulador**
```bash
# Android Studio Emulator (recomendado)
- Android 10+ com Google Play
- Proxy configurado para IP:8080
- Certificado Burp instalado
- Apps: Nubank Android/iOS
```

### **3. Bypass de Certificate Pinning**
```bash
# Usar Frida para bypass
frida -U -f com.nu.production -l ssl-kill-switch.js

# Ou usar Magisk + MagiskTrustUserCerts
# Para permitir certificados de usuário
```

---

## 🔍 **Endpoints Críticos para Interceptar**

### **A. Autenticação**
```http
POST /api/mobile/auth/login
POST /api/mobile/auth/refresh
POST /api/mobile/biometry/verify
POST /api/mobile/pin/verify
GET /api/mobile/session/validate
```

### **B. Transações Financeiras**
```http
POST /api/mobile/pix/send
POST /api/mobile/transfers/ted
POST /api/mobile/payments/boleto
POST /api/mobile/cards/transactions
PUT /api/mobile/limits/increase
```

### **C. Dados Sensíveis**
```http
GET /api/mobile/balance/current
GET /api/mobile/statements/download
GET /api/mobile/profile/complete
GET /api/mobile/accounts/summary
GET /api/mobile/investments/portfolio
```

---

## 🚨 **Testes de BAC/IDOR Prioritários**

### **1. Manipulação de Parâmetros**

#### **A. IDs de Usuário**
```http
# Original
GET /api/mobile/profile/123456

# Testar
GET /api/mobile/profile/123457
GET /api/mobile/profile/123455
GET /api/mobile/profile/000001
GET /api/mobile/profile/admin
```

#### **B. IDs de Transação**
```http
# Original  
GET /api/mobile/transactions/txn_abc123

# Testar
GET /api/mobile/transactions/txn_abc124
GET /api/mobile/transactions/txn_000001
```

#### **C. IDs de Conta**
```http
# Original
GET /api/mobile/accounts/acc_456789

# Testar
GET /api/mobile/accounts/acc_456790
GET /api/mobile/accounts/acc_000001
```

### **2. Bypass de Autenticação**

#### **A. Remover Headers de Auth**
```http
# Original
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
X-Session-Token: sess_123abc

# Testar sem headers
# Testar com tokens inválidos
Authorization: Bearer fake_token
X-Session-Token: invalid_session
```

#### **B. Modificar User Context**
```http
# Original
X-User-Id: 123456
X-Account-Id: acc_789

# Testar
X-User-Id: 123457
X-Account-Id: acc_790
X-User-Id: admin
X-Account-Id: acc_admin
```

---

## 💸 **Testes Específicos de Transações**

### **1. PIX Vulnerabilities**

#### **A. Valor Excessivo**
```json
{
  "amount": 999999.99,
  "pix_key": "test@test.com",
  "description": "Teste"
}
```

#### **B. Chaves PIX Inválidas**
```json
{
  "amount": 10.00,
  "pix_key": "admin@nubank.com.br",
  "description": "PIX interno"
}
```

#### **C. PIX sem Validação**
```json
{
  "amount": 10.00,
  "pix_key": "../../../etc/passwd",
  "description": "Path traversal"
}
```

### **2. Transferências TED/DOC**

#### **A. Conta Inexistente**
```json
{
  "amount": 10.00,
  "destination_account": "00000000",
  "destination_bank": "999",
  "cpf": "00000000000"
}
```

#### **B. Bypass de Limite**
```json
{
  "amount": 999999.99,
  "destination_account": "12345678",
  "destination_bank": "001",
  "bypass_limit": true
}
```

### **3. Pagamentos**

#### **A. Boleto Inválido**
```json
{
  "barcode": "00000000000000000000000000000000000000000000000000",
  "amount": 999999.99,
  "due_date": "2099-12-31"
}
```

---

## 🔄 **Race Conditions Testing**

### **Configuração do Burp**
```
1. Enviar requisição para Repeater
2. Duplicar requisição (Ctrl+D) várias vezes
3. Selecionar todas as abas
4. Usar "Send group in parallel (single-packet attack)"
```

### **Cenários para Testar**
```json
// Transferência PIX simultânea
{
  "amount": 1.00,
  "pix_key": "test@test.com",
  "transaction_id": "race_test_001"
}

// Resgate de investimento duplo
{
  "investment_id": "inv_123",
  "amount": 1.00,
  "action": "redeem"
}
```

---

## 📊 **Headers Obrigatórios e Críticos**

### **Sempre Incluir**
```http
X-Correlation-Id: bc-handle
```

### **Headers Móveis Importantes**
```http
X-Platform: android
X-App-Version: 8.45.0
X-Device-Model: SM-G975F
X-OS-Version: 10
X-Client-Type: mobile
User-Agent: Nubank/8.45.0 (Android 10; SM-G975F)
```

### **Headers de Segurança**
```http
X-Request-Id: mobile-test-123
X-Session-Token: [session_token]
X-Device-Id: [device_id]
X-Fingerprint: [device_fingerprint]
```

---

## 🚨 **Indicadores de Vulnerabilidade**

### **BAC Horizontal Encontrado**
```
✅ Status 200 com dados de outro usuário
✅ Transação autorizada sem token válido
✅ Acesso a saldo/extratos alheios
✅ Modificação de dados de terceiros
```

### **IDOR Confirmado**
```
✅ ID +1/-1 retorna dados diferentes
✅ IDs sequenciais expostos
✅ Dados sensíveis via ID manipulation
✅ Acesso a documentos/fotos alheios
```

### **Race Condition Sucesso**
```
✅ Múltiplas transações aceitas simultaneamente
✅ Saldo debitado múltiplas vezes
✅ Limite ultrapassado via timing
✅ Duplicação de resgates/depósitos
```

---

## 📋 **Checklist de Teste**

### **Antes de Começar**
- [ ] Burp Suite configurado com certificado
- [ ] App Nubank instalado e funcionando
- [ ] Conta criada com CPF real
- [ ] Certificate pinning contornado
- [ ] Header X-Correlation-Id configurado

### **Durante os Testes**
- [ ] Interceptar todas as requisições
- [ ] Testar cada endpoint crítico
- [ ] Manipular IDs sistemáticamente  
- [ ] Tentar bypass de autenticação
- [ ] Respeitar limite de R$ 10
- [ ] Documentar passos detalhados

### **Ao Encontrar Vulnerabilidade**
- [ ] Reproduzir múltiplas vezes
- [ ] Documentar impacto financeiro
- [ ] Capturar evidências (requests/responses)
- [ ] Criar PoC detalhado
- [ ] Verificar se é P1 ($2000-$4000)

---

## 💡 **Dicas Avançadas**

### **1. GraphQL Testing**
```graphql
# Introspection query
{ __schema { types { name fields { name type { name } } } } }

# Dados sensíveis
{ user { id cpf balance transactions { amount date } } }
```

### **2. WebSocket Monitoring**
- Monitorar conexões WebSocket para notificações
- Testar subscription hijacking
- Verificar dados em tempo real

### **3. Deep Link Testing**
```
nubank://transfer?amount=10&destination=test
nubank://pix?key=admin@nubank.com.br&amount=10
```

---

**⚠️ CRÍTICO: Sempre usar X-Correlation-Id: bc-handle**
**⚠️ MÁXIMO: R$ 10,00 por PoC**
**⚠️ FOCO: P1 vulnerabilities ($2000-$4000)**
