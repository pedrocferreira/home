# 🏦 Nubank Bug Bounty Arsenal

<div align="center">

![Bug Bounty](https://img.shields.io/badge/Bug%20Bounty-Nubank-purple?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Security](https://img.shields.io/badge/Security-Research-red?style=for-the-badge&logo=security)

**🎯 Arsenal completo para Bug Bounty no Nubank - Foco em vulnerabilidades P1 ($2000-$4000)**

[📖 Documentação](#-documentação) • [🚀 Quick Start](#-quick-start) • [🔧 Scripts](#-scripts) • [💰 Resultados](#-resultados)

</div>

---

## 🎯 **Sobre o Projeto**

Este repositório contém um **arsenal completo** para Bug Bounty no **Nubank**, focado em encontrar vulnerabilidades de **alto valor** (P1: $2000-$4000). 

### **🎪 Destaques:**
- ✅ **Scripts automatizados** para testes de BAC/IDOR
- ✅ **Configuração completa** do Burp Suite 
- ✅ **Guias detalhados** para interceptação móvel
- ✅ **Compliance total** com regras do programa
- ✅ **Foco em vulnerabilidades P1** ($2000-$4000)

### **🏆 Vulnerabilidades Alvo:**
| Tipo | Impacto | Recompensa | Prioridade |
|------|---------|------------|------------|
| **BAC Horizontal** | Transações não autorizadas | $2000-$4000 | 🔥 P1 |
| **IDOR Financeiro** | Acesso a dados alheios | $2000-$4000 | 🔥 P1 |
| **Race Conditions** | Duplicação de transações | $2000-$4000 | 🔥 P1 |
| **Lógica de Negócios** | Bypass de limites | $500-$1000 | ⚡ P2 |

---

## 📋 **Estrutura do Projeto**

```
📁 nubank-bug-bounty/
├── 📄 README.md                              # Este arquivo
├── 📄 nubank.md                             # Guia original do programa
├── 📄 nubank_testing_strategy.md            # Estratégia completa de testes
├── 🔧 Scripts/
│   ├── nubank_bac_tester.py                # Tests automatizados BAC/IDOR
│   ├── nubank_mobile_tester.py             # Tests específicos móveis
│   └── setup_burp_nubank.sh                # Setup automatizado Burp Suite
├── 📚 Guides/
│   ├── burp_suite_setup_guide.md           # Configuração Burp detalhada
│   ├── burp_quick_setup_visual.md          # Setup visual em 5 minutos
│   ├── nubank_mobile_interception_guide.md # Interceptação de APIs móveis
│   └── nubank_compliance_checklist.md      # Checklist de compliance
└── 📊 Results/
    └── vulnerability_reports/               # Relatórios de vulnerabilidades
```

---

## 🚀 **Quick Start**

### **⚡ Setup Automatizado (5 minutos)**

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/nubank-bug-bounty.git
cd nubank-bug-bounty

# 2. Execute o setup automatizado
chmod +x setup_burp_nubank.sh
./setup_burp_nubank.sh --auto

# 3. Execute os testes
python3 nubank_bac_tester.py
python3 nubank_mobile_tester.py
```

### **📱 Configuração Burp Suite**

```bash
# Configuração completa em 3 comandos
./setup_burp_nubank.sh --auto    # Setup automatizado
# Seguir: burp_quick_setup_visual.md
# Executar: check_setup.sh
```

---

## 🔧 **Scripts Disponíveis**

### **🎯 Script Principal: BAC/IDOR Tester**
```python
# nubank_bac_tester.py
python3 nubank_bac_tester.py
```
**Features:**
- ✅ Testa BAC em transferências financeiras
- ✅ Verifica IDOR em contas/transações  
- ✅ Testa race conditions
- ✅ GraphQL injection testing
- ✅ Header obrigatório `X-Correlation-Id: bc-handle`

### **📱 Script Móvel: Mobile App Tester**
```python
# nubank_mobile_tester.py  
python3 nubank_mobile_tester.py
```
**Features:**
- ✅ Simula aplicações Android/iOS
- ✅ Testa autenticação móvel
- ✅ Verifica exposição de dados
- ✅ Busca segredos hardcoded
- ✅ Vulnerabilidades PIX específicas

### **🔧 Setup Automatizado: Burp Suite**
```bash
# setup_burp_nubank.sh
./setup_burp_nubank.sh
```
**Features:**
- ✅ Instalação completa Frida + bypass SSL
- ✅ Configuração automática proxy/certificados
- ✅ Scripts auxiliares de verificação
- ✅ Menu interativo para setup

---

## 📚 **Documentação**

### **🎯 Guias Estratégicos**
- **[Estratégia de Testes](nubank_testing_strategy.md)** - Foco em vulnerabilidades P1
- **[Compliance Checklist](nubank_compliance_checklist.md)** - Regras obrigatórias
- **[Mobile Interception](nubank_mobile_interception_guide.md)** - Interceptação de APIs

### **🔧 Guias Técnicos**
- **[Burp Setup Completo](burp_suite_setup_guide.md)** - Configuração detalhada passo a passo
- **[Burp Setup Visual](burp_quick_setup_visual.md)** - Setup rápido em 5 minutos
- **[Guia Original](nubank.md)** - Programa oficial Nubank Bug Bounty

---

## 🚨 **Vulnerabilidades de Alto Impacto**

### **💰 P1: $2000-$4000 (FOCO MÁXIMO)**

#### **🔥 BAC Horizontal em Transações**
```http
POST /api/mobile/pix/send
{
  "amount": 10.00,
  "from_account": "conta_de_outro_usuario"  // ← Teste BAC
}
```

#### **🔥 IDOR em Dados Financeiros**
```http
GET /api/mobile/balance/123456    // Original
GET /api/mobile/balance/123457    // ← Teste IDOR (+1)
GET /api/mobile/balance/000001    // ← Teste admin access
```

#### **🔥 Race Conditions em Pagamentos**
```bash
# Burp Suite: Send group in parallel (5x simultâneo)
POST /api/mobile/pix/send {"amount": 1.00, "destination": "test"}
```

---

## ⚠️ **Compliance e Regras**

### **❌ NUNCA FAZER (Desqualificação)**
- DoS/DDoS ou Social Engineering
- Usar identificação falsa  
- Exceder **R$ 10** em PoCs financeiros
- Testar sem header `X-Correlation-Id: bc-handle`

### **✅ SEMPRE FAZER (Obrigatório)**
- Usar conta com **CPF real**
- Incluir header obrigatório em **todas as requisições**
- Documentar **passos detalhados**
- Focar em **impacto real** de segurança

---

## 🎯 **Endpoints Críticos**

### **Transações Financeiras (P1)**
```http
POST /api/mobile/pix/send           # PIX transfers
POST /api/mobile/transfers/ted      # TED transfers  
POST /api/mobile/payments/boleto    # Bill payments
PUT  /api/mobile/limits/increase    # Limit increases
```

### **Dados Sensíveis (P1)**
```http
GET /api/mobile/balance/current     # Account balance
GET /api/mobile/statements/download # Statements
GET /api/mobile/profile/complete    # Full profile
GET /api/mobile/investments/portfolio # Investments
```

---

## 💰 **Resultados e ROI**

### **🎯 Potencial de Retorno**
| Vulnerabilidades | Quantidade Estimada | Valor Unitário | Total Estimado |
|------------------|-------------------|---------------|---------------|
| **BAC P1** | 3-5 | $2000-$4000 | $6K-$20K |
| **IDOR P1** | 2-3 | $2000-$4000 | $4K-$12K |
| **Race Conditions** | 1-2 | $2000-$4000 | $2K-$8K |
| **Logic Flaws P2** | 2-4 | $500-$1000 | $1K-$4K |
| **TOTAL** | **8-14** | - | **$13K-$44K** |

### **⏱️ Timeline Estimado**
- **Setup**: 1 dia (automatizado)
- **Testes**: 1-2 semanas  
- **Documentação**: 2-3 dias por vulnerabilidade
- **ROI**: Quality over quantity

---

## 🔧 **Instalação e Dependências**

### **📋 Pré-requisitos**
```bash
# Sistema
- Linux/macOS/Windows
- Python 3.8+
- Java 11+ (para Burp Suite)
- Android Studio + Emulador

# Ferramentas  
- Burp Suite Professional/Community
- ADB (Android Debug Bridge)
- Frida + frida-tools
```

### **🚀 Instalação Rápida**
```bash
# Clone e setup automático
git clone https://github.com/SEU_USUARIO/nubank-bug-bounty.git
cd nubank-bug-bounty
./setup_burp_nubank.sh --auto

# Verificar instalação
./check_setup.sh
```

---

## 📊 **Métricas e Analytics**

<div align="center">

### **🎯 Foco em Qualidade**
![Quality](https://img.shields.io/badge/Quality-over%20Quantity-gold?style=for-the-badge)

### **💰 ROI Médio por Vulnerabilidade**
![ROI](https://img.shields.io/badge/ROI-$3000%2Bvuln-green?style=for-the-badge)

### **⏱️ Setup Time**
![Setup](https://img.shields.io/badge/Setup-5%20minutes-blue?style=for-the-badge)

</div>

---

## 🤝 **Contribuições**

Este projeto é **open source** e contribuições são bem-vindas!

### **Como Contribuir:**
1. 🍴 **Fork** o projeto
2. 🔧 **Crie** uma feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 **Commit** suas mudanças (`git commit -m 'Add amazing feature'`)
4. 📤 **Push** para a branch (`git push origin feature/amazing-feature`)
5. 🔀 **Abra** um Pull Request

### **Áreas de Contribuição:**
- 🔧 Novos scripts de automação
- 📚 Melhorias na documentação  
- 🛡️ Novas técnicas de bypass
- 🎯 Estratégias de teste aprimoradas

---

## 📜 **Licença**

Este projeto está sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## ⚖️ **Disclaimer Legal**

Este projeto é destinado **exclusivamente** para:
- ✅ **Pesquisa de segurança ética**
- ✅ **Bug bounty autorizado** no programa Nubank
- ✅ **Fins educacionais** em segurança

**❌ USO PROIBIDO:**
- Atividades maliciosas ou ilegais
- Testes sem autorização
- Violação de termos de serviço

---

## 📞 **Contato e Suporte**

<div align="center">

### **🔗 Links Úteis**
[![GitHub](https://img.shields.io/badge/GitHub-Profile-black?style=for-the-badge&logo=github)](https://github.com/SEU_USUARIO)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/SEU_PERFIL)
[![Email](https://img.shields.io/badge/Email-Contact-red?style=for-the-badge&logo=gmail)](mailto:seu.email@gmail.com)

### **🏆 Bug Bounty Stats**
![Vulnerabilities](https://img.shields.io/badge/Vulnerabilities-Found-success?style=for-the-badge)
![Rewards](https://img.shields.io/badge/Total%20Rewards-$X,XXX-gold?style=for-the-badge)

</div>

---

<div align="center">

**🎯 Desenvolvido com foco em vulnerabilidades de alto valor**

**💰 Maximizando ROI em Bug Bounty Programs**

**🔒 Ethical Hacking • Responsible Disclosure • Security Research**

---

⭐ **Se este projeto te ajudou, deixe uma estrela!** ⭐

</div>
