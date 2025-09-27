# ✅ Nubank Bug Bounty - Checklist de Compliance

## 🚨 **REGRAS CRÍTICAS - OBRIGATÓRIAS**

### **❌ NUNCA FAZER (Desqualificação)**
- [ ] **NÃO** usar identificação falsa
- [ ] **NÃO** fazer DoS/DDoS
- [ ] **NÃO** fazer Social Engineering  
- [ ] **NÃO** testar Subdomain Takeover
- [ ] **NÃO** exceder R$ 10 em PoCs financeiros
- [ ] **NÃO** testar sem header X-Correlation-Id

### **✅ SEMPRE FAZER (Obrigatório)**
- [ ] Usar conta com CPF real
- [ ] Incluir header: `X-Correlation-Id: bc-handle`
- [ ] Limitar PoCs a R$ 10 máximo
- [ ] Documentar passos de reprodução detalhados
- [ ] Focar em impacto real de segurança
- [ ] Notificar se for bloqueado

---

## 🎯 **PRIORIDADES DE TESTE**

### **P1: $2000-$4000 (FOCO MÁXIMO)**
- [ ] BAC em aplicações móveis Android/iOS
- [ ] Transações não autorizadas (PIX/TED/DOC)
- [ ] Bypass de autenticação em transferências
- [ ] IDOR em dados financeiros
- [ ] Race conditions em pagamentos
- [ ] Injeções em prod-*.nubank.com.br

### **P2: $500-$1000**
- [ ] Lógica de investimentos em *.nuinvest.com.br
- [ ] Falhas de cálculo de rendimentos
- [ ] Manipulação de cotas/ativos
- [ ] Bypass de limites de resgate

---

## 🔧 **CONFIGURAÇÃO TÉCNICA**

### **Headers Obrigatórios**
```http
X-Correlation-Id: bc-handle  # CRÍTICO - sempre incluir
```

### **Headers Móveis Recomendados**
```http
X-Platform: android
X-App-Version: 8.45.0
X-Device-Model: SM-G975F
User-Agent: Nubank/8.45.0 (Android 10; SM-G975F)
```

### **Limites de PoC**
```json
{
  "amount": 10.00,        // MÁXIMO permitido
  "description": "PoC compliance test"
}
```

---

## 📱 **TESTE DE APLICAÇÕES MÓVEIS**

### **Configuração do Ambiente**
- [ ] Burp Suite configurado (proxy 8080)
- [ ] Certificado CA instalado no dispositivo
- [ ] Certificate pinning contornado (Frida)
- [ ] App Nubank instalado e funcionando
- [ ] Conta autenticada com CPF real

### **Interceptação de Tráfego**
- [ ] Todas as requisições interceptadas
- [ ] Headers de correlação verificados
- [ ] Endpoints críticos mapeados
- [ ] Tokens de autenticação identificados

---

## 🚨 **TESTES DE BAC/IDOR**

### **Cenários Obrigatórios**
- [ ] Transferência sem token válido
- [ ] PIX em nome de outro usuário
- [ ] Acesso a saldo de conta alheia
- [ ] Modificação de limite sem autorização
- [ ] Visualização de extratos de terceiros

### **Manipulação de IDs**
- [ ] IDs sequenciais testados (+1, -1)
- [ ] IDs de conta modificados
- [ ] IDs de transação alterados
- [ ] IDs de usuário manipulados
- [ ] Padrões de ID identificados

---

## 💸 **TESTES FINANCEIROS**

### **PIX Testing**
```json
{
  "amount": 10.00,  // Máximo permitido
  "pix_key": "test@test.com",
  "description": "PoC BAC test"
}
```

### **Transferências TED/DOC**
```json
{
  "amount": 5.00,   // Dentro do limite
  "destination_account": "12345678",
  "destination_bank": "001"
}
```

### **Pagamentos**
```json
{
  "amount": 1.00,   // Valor mínimo
  "barcode": "valid_test_barcode",
  "due_date": "2024-12-31"
}
```

---

## 🔄 **RACE CONDITIONS**

### **Configuração do Burp**
- [ ] Requisições duplicadas no Repeater
- [ ] "Send group in parallel" configurado
- [ ] Timing de requisições documentado
- [ ] Resultados múltiplos analisados

### **Cenários de Teste**
- [ ] Transferência PIX simultânea
- [ ] Resgate de investimento duplo
- [ ] Pagamento de boleto múltiplo
- [ ] Ajuste de limite concorrente

---

## 📊 **DOCUMENTAÇÃO DE VULNERABILIDADES**

### **Informações Obrigatórias**
- [ ] **Endpoint** exato testado
- [ ] **Payload** completo usado
- [ ] **Headers** incluindo X-Correlation-Id
- [ ] **Response** completa capturada
- [ ] **Impacto** financeiro descrito
- [ ] **Passos** de reprodução detalhados

### **Evidências Necessárias**
- [ ] Screenshot da vulnerabilidade
- [ ] Request/Response completos
- [ ] Burp Suite project exportado
- [ ] Video de demonstração (opcional)

---

## ⚠️ **VERIFICAÇÕES FINAIS**

### **Antes de Submeter Relatório**
- [ ] Vulnerabilidade reproduzida 3+ vezes
- [ ] Impacto P1 confirmado ($2000-$4000)
- [ ] Compliance com todas as regras
- [ ] PoC limitado a R$ 10 máximo
- [ ] Cenário de exploração real descrito

### **Qualidade do Relatório**
- [ ] Título claro e específico
- [ ] Resumo executivo incluído
- [ ] Passos técnicos detalhados
- [ ] Recomendações de correção
- [ ] Timeline de descoberta

---

## 🎯 **MÉTRICAS DE SUCESSO**

### **Vulnerabilidades P1 ($2000-$4000)**
- [ ] BAC Horizontal confirmado
- [ ] Transação não autorizada executada
- [ ] Dados financeiros de terceiros acessados
- [ ] Bypass de autenticação demonstrado
- [ ] Race condition em pagamento explorada

### **ROI Esperado**
- **P1**: $2000-$4000 por vulnerabilidade
- **P2**: $500-$1000 por vulnerabilidade
- **Tempo investido**: Foco em quality over quantity

---

## 📞 **Suporte e Escalação**

### **Se Bloqueado**
1. Parar testes imediatamente
2. Documentar comportamento do bloqueio
3. Notificar equipe do Nubank
4. Aguardar liberação antes de continuar

### **Dúvidas sobre Escopo**
1. Consultar guia oficial
2. Verificar regras atualizadas
3. Contactar programa se necessário
4. Documentar comunicações

---

**🏦 LEMBRE-SE: Nubank é uma instituição financeira**
**🔒 SEGURANÇA: Máxima responsabilidade nos testes**
**💰 FOCO: Vulnerabilidades que afetam dinheiro real**
**📋 COMPLIANCE: Zero tolerância para violações**
