# 🎯 Bug Bounty Setup - Arsenal Completo

<div align="center">

![Bug Bounty](https://img.shields.io/badge/Bug%20Bounty-Arsenal-red?style=for-the-badge)
![Projects](https://img.shields.io/badge/Projects-2-blue?style=for-the-badge)
![ROI](https://img.shields.io/badge/ROI-High%20Value-gold?style=for-the-badge)

**🏆 Arsenal completo para Bug Bounty em múltiplas empresas**

[📖 Como Usar](#-como-usar) • [🏦 Nubank](#-nubank) • [⚔️ Under Armour](#️-under-armour) • [🚀 Quick Start](#-quick-start)

</div>

---

## 📋 **Visão Geral**

Este repositório contém **arsenais completos** para Bug Bounty em **duas empresas principais**, cada uma com estratégias específicas e ferramentas otimizadas para **vulnerabilidades de alto valor**.

### **🎪 Projetos Incluídos:**

| Empresa | Foco Principal | Recompensa Max | Ferramentas | Status |
|---------|---------------|----------------|-------------|--------|
| **🏦 Nubank** | BAC/IDOR Financeiro | $2000-$4000 | Python + Burp | ✅ Completo |
| **⚔️ Under Armour** | BAC + GraphQL | P1/P2 | Bash + Manual | ✅ Completo |

---

## 🚀 **Quick Start**

### **⚡ Execução Rápida (5 minutos)**

```bash
# 1. Escolher projeto
cd nubank_bug_bounty    # Para Nubank
# ou
cd under_armour_bug_bounty    # Para Under Armour

# 2. Executar setup automático
./setup_burp_nubank.sh --auto     # Nubank
# ou
./under_armour_bac_test.sh         # Under Armour

# 3. Executar testes
python3 nubank_bac_tester.py      # Nubank
# ou seguir guia manual Under Armour
```

---

## 🏦 **Projeto Nubank**

### **📂 Localização:** `/home/nubank_bug_bounty/`

### **🎯 Características:**
- **Foco**: Aplicações móveis Android/iOS
- **Vulnerabilidades**: BAC Horizontal, IDOR, Race Conditions
- **Recompensa**: $2000-$4000 (P1)
- **Automação**: Scripts Python + Burp Suite

### **🔧 Como Usar:**

#### **1. Setup Automático (RECOMENDADO)**
```bash
cd /home/nubank_bug_bounty

# Setup completo em 1 comando
./setup_burp_nubank.sh --auto
```

#### **2. Executar Testes**
```bash
# Testes automatizados BAC/IDOR
python3 Scripts/nubank_bac_tester.py

# Testes específicos móveis
python3 Scripts/nubank_mobile_tester.py
```

#### **3. Interceptação Manual**
```bash
# Seguir guia visual
cat Guides/burp_quick_setup_visual.md

# Ou guia detalhado
cat Guides/burp_suite_setup_guide.md
```

### **📊 Vulnerabilidades Alvo:**

#### **💰 P1 ($2000-$4000) - FOCO MÁXIMO**
```http
# BAC Horizontal em Transferências
POST /api/mobile/pix/send
{"amount": 10.00, "from_account": "conta_alheia"}

# IDOR em Dados Financeiros  
GET /api/mobile/balance/123456 → 123457

# Race Conditions em Pagamentos
# Envios simultâneos via Burp Suite
```

### **⚠️ Compliance Nubank:**
- ✅ Header obrigatório: `X-Correlation-Id: bc-handle`
- ✅ Limite máximo: R$ 10 por PoC
- ✅ Conta com CPF real
- ❌ NÃO fazer DoS/DDoS

---

## ⚔️ **Projeto Under Armour**

### **📂 Localização:** `/home/under_armour_bug_bounty/`

### **🎯 Características:**
- **Foco**: Dados do atleta (treinos, pedidos, fotos)
- **Vulnerabilidades**: BAC Horizontal (P1/P2)
- **Método**: Testes manuais com Burp Suite
- **Desafio**: Proteção anti-bot robusta (HTTP 418)

### **🔧 Como Usar:**

#### **1. Abordagem Manual (OBRIGATÓRIA)**
```bash
cd /home/under_armour_bug_bounty

# Ler estratégia completa
cat under_armour_manual_testing_guide.md
```

#### **2. Configurar Burp Suite**
```bash
# Instalar Burp Suite
# Configurar proxy 127.0.0.1:8080
# Configurar navegador para usar proxy
```

#### **3. Testes Práticos**
```bash
# Login: pedroocferreira@gmail.com
# Senha: @Pedro9cce22f2

# Navegue manualmente:
# - Perfil do usuário
# - Treinos/Workouts  
# - Pedidos/Orders
# - Fotos/Media

# Intercepte no Burp e teste:
# - Modificação de IDs
# - Bypass de autenticação
# - IDOR em dados pessoais
```

### **🎯 Endpoints Prioritários:**
```http
# Dados de Perfil
GET /api/user/profile?id=123
GET /api/athlete/123

# Treinos  
GET /api/workouts/user/123
GET /api/training/123

# Pedidos
GET /api/orders/123
GET /api/purchases/123

# Fotos
GET /api/photos/user/123
GET /api/media/123
```

### **⚠️ Desafios Under Armour:**
- 🚫 **HTTP 418**: Proteção anti-bot detecta automação
- 🛡️ **WAF**: Web Application Firewall robusto
- 📱 **Testes manuais**: Única forma de contornar proteção
- 🎯 **Foco P1/P2**: Vulnerabilidades críticas de acesso

---

## 🔄 **Comparação dos Projetos**

### **🏦 Nubank vs ⚔️ Under Armour**

| Aspecto | 🏦 Nubank | ⚔️ Under Armour |
|---------|-----------|-----------------|
| **Automação** | ✅ Scripts Python | ❌ Manual apenas |
| **Proteção** | 🔒 Moderada | 🛡️ Muito alta |
| **Recompensa** | 💰 $2000-$4000 | 💰 P1/P2 variável |
| **Compliance** | 📋 Regras específicas | 📋 Padrão |
| **Dificuldade** | 🔥 Média-Alta | 🔥🔥 Alta |
| **ROI** | 📈 Alto/Previsível | 📈 Alto/Desafiador |

---

## 📚 **Estrutura dos Projetos**

### **🏦 Nubank Bug Bounty**
```
📁 nubank_bug_bounty/
├── 📄 README.md                              # Visão geral
├── 🔧 Scripts/
│   ├── nubank_bac_tester.py                 # BAC/IDOR automático
│   ├── nubank_mobile_tester.py              # Testes móveis
│   └── setup_burp_nubank.sh                 # Setup Burp
├── 📚 Guides/
│   ├── burp_suite_setup_guide.md            # Setup detalhado
│   ├── burp_quick_setup_visual.md           # Setup rápido
│   ├── nubank_mobile_interception_guide.md  # Interceptação
│   └── nubank_compliance_checklist.md       # Compliance
└── 📊 Results/
    └── vulnerability_reports/               # Relatórios
```

### **⚔️ Under Armour Bug Bounty**
```
📁 under_armour_bug_bounty/
├── 📄 README.md                             # Visão geral
├── 📄 under_armour_bug_bounty_guide.md     # Guia original
├── 📄 under_armour_manual_testing_guide.md # Guia manual
├── 🔧 under_armour_bac_test.sh             # Script básico
├── 🔧 under_armour_stealth_test.sh         # Evasão anti-bot
├── 🐍 under_armour_selenium_test.py        # Selenium (limitado)
└── 🐍 under_armour_simple_test.py          # Requests simples
```

---

## 🎯 **Estratégias por Projeto**

### **🏦 Estratégia Nubank**

#### **Foco Principal:**
1. **📱 Aplicações Móveis** (Android/iOS)
2. **💰 Transações Financeiras** (PIX, TED, Boletos)
3. **🔐 Controle de Acesso** (BAC Horizontal)
4. **📊 Dados Sensíveis** (Saldo, Extratos, Investimentos)

#### **Metodologia:**
```
1. 🔧 Setup automatizado → 5 min
2. 📱 Interceptação móvel → Burp + Frida
3. 🎯 Testes automatizados → Scripts Python
4. 📋 Compliance check → Checklist
5. 💰 Submissão P1 → $2000-$4000
```

### **⚔️ Estratégia Under Armour**

#### **Foco Principal:**
1. **🏃 Dados do Atleta** (Treinos, Performance)
2. **🛒 E-commerce** (Pedidos, Produtos)
3. **📷 Mídia** (Fotos, Vídeos)
4. **👤 Perfil** (Dados pessoais)

#### **Metodologia:**
```
1. 🔧 Setup manual → Burp Suite
2. 🕵️ Reconnaissance → Endpoints mapping
3. 🎯 Testes manuais → Modificação IDs
4. 🛡️ Bypass proteção → Timing/Headers
5. 💰 Submissão P1/P2 → Variável
```

---

## ⚡ **Execução Rápida por Cenário**

### **🎯 Cenário 1: Foco em ROI Alto (Nubank)**
```bash
# Setup completo automatizado
cd /home/nubank_bug_bounty
./Scripts/setup_burp_nubank.sh --auto

# Executar testes
python3 Scripts/nubank_bac_tester.py
python3 Scripts/nubank_mobile_tester.py

# ROI esperado: $6K-$20K
```

### **🎯 Cenário 2: Desafio Técnico (Under Armour)**
```bash
# Análise manual necessária
cd /home/under_armour_bug_bounty
cat under_armour_manual_testing_guide.md

# Configurar Burp manualmente
# Interceptar aplicação web
# Testar endpoints sistematicamente

# ROI esperado: P1/P2 variável
```

### **🎯 Cenário 3: Aprendizado Completo (Ambos)**
```bash
# Começar com Nubank (automatizado)
cd /home/nubank_bug_bounty
./Scripts/setup_burp_nubank.sh --auto

# Depois Under Armour (manual)
cd /home/under_armour_bug_bounty
# Seguir guias manuais

# Objetivo: Dominar ambas as abordagens
```

---

## 🔧 **Dependências e Instalação**

### **📋 Pré-requisitos Comuns**
```bash
# Sistema base
- Linux/macOS/Windows
- Python 3.8+
- Git

# Ferramentas de segurança
- Burp Suite Professional/Community
- OWASP ZAP (alternativa)
- Browser moderno
```

### **🏦 Específico Nubank**
```bash
# Adicional para Nubank
- Android Studio + Emulador
- ADB (Android Debug Bridge)
- Frida + frida-tools
- Java 11+ (para Burp)

# Instalação rápida
pip3 install frida-tools requests
```

### **⚔️ Específico Under Armour**
```bash
# Adicional para Under Armour  
- Navegador configurado
- Proxy manual
- Paciência para testes manuais

# Sem dependências especiais
```

---

## 📊 **ROI e Resultados Esperados**

### **💰 Potencial de Retorno**

#### **🏦 Nubank (Automatizado)**
| Vulnerabilidade | Quantidade | Valor Unit. | Total |
|-----------------|------------|-------------|-------|
| BAC P1 | 3-5 | $2000-$4000 | $6K-$20K |
| IDOR P1 | 2-3 | $2000-$4000 | $4K-$12K |
| Race Conditions | 1-2 | $2000-$4000 | $2K-$8K |
| **TOTAL** | **6-10** | - | **$12K-$40K** |

#### **⚔️ Under Armour (Manual)**
| Vulnerabilidade | Quantidade | Valor | Total |
|-----------------|------------|-------|-------|
| BAC P1 | 2-4 | Alto | Variável |
| IDOR P1/P2 | 3-5 | Médio-Alto | Variável |
| Logic Flaws | 2-3 | Médio | Variável |
| **TOTAL** | **7-12** | - | **Variável** |

### **⏱️ Timeline Estimado**
- **Nubank**: 1-2 semanas (setup + testes)
- **Under Armour**: 2-3 semanas (manual + bypass)
- **Ambos**: 1 mês para domínio completo

---

## 🤝 **Contribuições e Comunidade**

### **Como Contribuir:**
1. 🍴 Fork o projeto
2. 🔧 Adicione melhorias ou novas empresas
3. 📚 Melhore documentação
4. 🐛 Reporte bugs ou sugira features
5. 🔀 Envie Pull Request

### **Áreas de Expansão:**
- 🏢 **Novas empresas**: Bancos, fintechs, e-commerce
- 🔧 **Novas técnicas**: Bypass, automação, evasão
- 📱 **Plataformas**: iOS específico, APIs GraphQL
- 🛡️ **Defesas**: WAF bypass, rate limiting

---

## ⚖️ **Disclaimer Legal**

### **✅ Uso Autorizado:**
- Bug bounty programs oficiais
- Pesquisa de segurança ética
- Fins educacionais
- Testes com permissão explícita

### **❌ Uso Proibido:**
- Atividades maliciosas ou ilegais
- Testes sem autorização
- Violação de termos de serviço
- Qualquer atividade prejudicial

---

## 📞 **Suporte e Contato**

### **🔗 Links Úteis**
- **GitHub**: [BugBountySetup](https://github.com/seu-usuario/BugBountySetup)
- **Documentação**: Cada projeto tem guias específicos
- **Issues**: Reporte problemas via GitHub Issues

### **📬 Comunicação**
- **Bugs**: Use GitHub Issues
- **Segurança**: Disclosure responsável via email privado
- **Contribuições**: Pull Requests bem-vindos

---

<div align="center">

**🎯 Desenvolvido para maximizar ROI em Bug Bounty Programs**

**🔒 Ethical Hacking • Responsible Disclosure • Security Research**

**💰 Foco em vulnerabilidades de alto valor e automação inteligente**

---

⭐ **Se este arsenal te ajudou, considere dar uma estrela no GitHub!** ⭐

</div>
