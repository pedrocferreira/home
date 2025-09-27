# 🏦 Nubank Bug Bounty - Projeto Completo

## 📁 **Estrutura do Projeto**

### 📄 **Documentação**
- `nubank.md` - Guia original fornecido
- `nubank_testing_strategy.md` - Estratégia completa de testes
- `nubank_mobile_interception_guide.md` - Guia prático para interceptação móvel
- `nubank_compliance_checklist.md` - Checklist de compliance obrigatório
- `README.md` - Este arquivo

### 🔧 **Scripts de Teste**
- `nubank_bac_tester.py` - Script para testes de BAC/IDOR
- `nubank_mobile_tester.py` - Script para testes específicos móveis

---

## 🎯 **Resumo Executivo**

### **Alvo Principal**
**Nubank** - Instituição financeira brasileira
- **Recompensa P1**: $2000-$4000
- **Foco**: Aplicações móveis e lógica de negócios
- **Prioridade**: BAC em transações financeiras

### **Vulnerabilidades Prioritárias**
1. **BAC (Broken Access Control)** - Transações não autorizadas
2. **IDOR** - Acesso a dados financeiros alheios  
3. **Race Conditions** - Duplicação de transações
4. **Injeções** - SQLi/Code Injection em APIs críticas
5. **Lógica de Negócios** - Bypass de limites/validações

---

## 🚨 **Regras Críticas (COMPLIANCE)**

### **❌ NUNCA FAZER**
- DoS/DDoS ou Social Engineering
- Usar identificação falsa
- Exceder R$ 10 em PoCs financeiros
- Testar sem header `X-Correlation-Id: bc-handle`

### **✅ SEMPRE FAZER**
- Usar conta com CPF real
- Incluir header obrigatório em todas as requisições
- Documentar passos detalhados
- Focar em impacto real de segurança

---

## 📱 **Estratégia de Testes**

### **1. Aplicações Móveis (P1: $2000-$4000)**
```
Alvos: Android/iOS Nubank
Foco: BAC em transações financeiras
Método: Interceptação com Burp Suite
```

### **2. APIs de Produção**
```
Domínio: prod-*.nubank.com.br
Foco: Injeções de alto impacto
Método: Testes automatizados + manuais
```

### **3. Plataforma de Investimentos**
```
Domínio: *.nuinvest.com.br  
Foco: Lógica de investimentos
Recompensa: $500-$1000
```

---

## 🔧 **Como Usar os Scripts**

### **Script Principal (BAC/IDOR)**
```bash
cd /home/nubank_bug_bounty
python3 nubank_bac_tester.py
```

**Testa:**
- Transferências sem autenticação
- IDOR em contas/transações
- Race conditions
- GraphQL injection
- Lógica de investimentos

### **Script Móvel**
```bash
cd /home/nubank_bug_bounty  
python3 nubank_mobile_tester.py
```

**Testa:**
- Autenticação móvel
- Transações via app
- Exposição de dados
- Rate limiting
- Segredos hardcoded
- Vulnerabilidades PIX

---

## 📋 **Guias Práticos**

### **1. Interceptação Móvel**
Siga: `nubank_mobile_interception_guide.md`
- Configuração do Burp Suite
- Bypass de certificate pinning
- Endpoints críticos para interceptar
- Técnicas de manipulação de IDs

### **2. Compliance Check**
Use: `nubank_compliance_checklist.md`
- Verificação de regras obrigatórias
- Configuração técnica correta
- Documentação de vulnerabilidades
- Métricas de sucesso

---

## 🎯 **Endpoints Críticos**

### **Transações Financeiras**
```http
POST /api/mobile/pix/send
POST /api/mobile/transfers/ted  
POST /api/mobile/payments/boleto
PUT /api/mobile/limits/increase
```

### **Dados Sensíveis**
```http
GET /api/mobile/balance/current
GET /api/mobile/statements/download
GET /api/mobile/profile/complete
GET /api/mobile/investments/portfolio
```

### **Autenticação**
```http
POST /api/mobile/auth/login
POST /api/mobile/auth/refresh
POST /api/mobile/biometry/verify
```

---

## 🚨 **Vulnerabilidades de Alto Impacto**

### **BAC Horizontal - P1 ($2000-$4000)**
```
Cenário: Transferir dinheiro usando conta de outro usuário
Teste: Modificar parâmetros de origem/destino
Payload: {"amount": 10.00, "from_account": "outro_usuario"}
```

### **IDOR Financeiro - P1 ($2000-$4000)**
```
Cenário: Acessar saldo/extratos de terceiros
Teste: Incrementar IDs de conta/usuário
URL: /api/mobile/balance/123456 → 123457
```

### **Race Condition - P1 ($2000-$4000)**
```
Cenário: Duplicar transferência PIX
Teste: Envios simultâneos da mesma transação
Resultado: Múltiplos débitos para uma operação
```

---

## 📊 **Status do Projeto**

### **✅ Concluído**
- Análise completa do guia original
- Estratégia de testes desenvolvida
- Scripts automatizados criados
- Guias práticos elaborados
- Checklist de compliance finalizado

### **🔄 Em Execução**
- Testes práticos com scripts
- Interceptação de APIs móveis
- Validação de compliance
- Documentação de descobertas

### **🎯 Próximos Passos**
1. Executar testes automatizados
2. Configurar interceptação móvel
3. Testar endpoints críticos manualmente
4. Documentar vulnerabilidades encontradas
5. Submeter relatórios de alta qualidade

---

## 💡 **Dicas de Sucesso**

### **Foco em Quality over Quantity**
- 1 vulnerabilidade P1 = $2000-$4000
- Melhor que 10 vulnerabilidades baixas
- Documentação detalhada é crucial

### **Compliance é Crítico**
- Zero tolerância para violações
- Header X-Correlation-Id é obrigatório
- R$ 10 é limite absoluto para PoCs

### **Impacto Real**
- Foque em cenários que afetam dinheiro
- Demonstre exploração prática
- Quantifique o risco financeiro

---

## 📞 **Contato e Suporte**

### **Se Encontrar Vulnerabilidades**
1. Parar testes imediatamente
2. Documentar evidências
3. Criar PoC detalhado
4. Submeter relatório
5. Aguardar análise

### **Se For Bloqueado**
1. Parar atividades
2. Documentar bloqueio
3. Notificar equipe Nubank
4. Aguardar liberação

---

## 🏆 **Métricas de Sucesso**

### **ROI Esperado**
- **P1 BAC**: $2000-$4000 por vulnerabilidade
- **P1 IDOR**: $2000-$4000 por vulnerabilidade  
- **P2 Logic**: $500-$1000 por vulnerabilidade

### **Timeline Estimado**
- **Setup**: 1-2 dias
- **Testes**: 1-2 semanas
- **Documentação**: 2-3 dias por vulnerabilidade
- **Submissão**: Imediata após validação

---

**🎯 OBJETIVO: Encontrar vulnerabilidades P1 ($2000-$4000)**
**🔒 MÉTODO: Testes focados em BAC/IDOR financeiro**
**📱 FOCO: Aplicações móveis Android/iOS**
**💰 META: ROI máximo com compliance total**

---

*Projeto criado em: $(date)*
*Status: Pronto para execução*
*Alvo: Nubank Bug Bounty Program*
