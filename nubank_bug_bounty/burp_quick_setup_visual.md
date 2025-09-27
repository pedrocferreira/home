# 🚀 Burp Suite Setup - Guia Rápido Visual

## ⚡ **CONFIGURAÇÃO EM 5 MINUTOS**

### **📋 CHECKLIST RÁPIDO**
```
□ Burp Suite instalado
□ Android Studio + Emulador
□ Java 11+ instalado
□ ADB funcionando
□ App Nubank baixado
```

---

## 🎯 **SETUP AUTOMATIZADO**

### **Execute o script:**
```bash
cd /home/nubank_bug_bounty
./setup_burp_nubank.sh --auto
```

### **Ou passo a passo:**
```bash
./setup_burp_nubank.sh
# Escolher opção 11 (Setup completo)
```

---

## 📱 **CONFIGURAÇÃO VISUAL - ANDROID EMULATOR**

### **1. Criar AVD no Android Studio**
```
Android Studio → Tools → AVD Manager → Create Virtual Device

┌─────────────────────────────────────┐
│ ✅ Device: Pixel 4                  │
│ ✅ Android: 10 (API 29)             │
│ ✅ RAM: 4GB                         │
│ ✅ Storage: 8GB                     │
│ ✅ Google Play: YES                 │
└─────────────────────────────────────┘
```

### **2. Configurar Proxy no Emulador**
```
Settings → Wi-Fi → AndroidWifi → Modify Network

┌─────────────────────────────────────┐
│ Proxy: Manual                       │
│ Hostname: [IP_DA_SUA_MAQUINA]      │
│ Port: 8080                          │
│ ✅ Save                             │
└─────────────────────────────────────┘
```

---

## 🔧 **CONFIGURAÇÃO VISUAL - BURP SUITE**

### **1. Configurar Proxy**
```
Proxy → Options → Proxy Listeners

┌─────────────────────────────────────┐
│ ✅ Running: YES                     │
│ Interface: All interfaces           │
│ Port: 8080                          │
│ ✅ Support invisible proxying       │
└─────────────────────────────────────┘
```

### **2. Exportar Certificado**
```
Proxy → Options → Import/Export CA Certificate

┌─────────────────────────────────────┐
│ ✅ Export                           │
│ ✅ Certificate in DER format        │
│ File: burp-ca-cert.der              │
│ ✅ Next                             │
└─────────────────────────────────────┘
```

### **3. Configurar Header Obrigatório**
```
Proxy → Options → Match and Replace → Add

┌─────────────────────────────────────┐
│ Type: Request header                │
│ Match: ^X-Correlation-Id.*          │
│ Replace: X-Correlation-Id: bc-handle│
│ ✅ OK                               │
└─────────────────────────────────────┘
```

### **4. Configurar Scope**
```
Target → Scope → Include in scope

┌─────────────────────────────────────┐
│ ✅ *.nubank.com.br                  │
│ ✅ *.nuinvest.com.br                │
│ ✅ prod-*.nubank.com.br             │
└─────────────────────────────────────┘
```

---

## 🛡️ **BYPASS SSL PINNING**

### **1. Instalar Frida Server**
```bash
# Executar no terminal
adb shell /data/local/tmp/frida-server &
```

### **2. Bypass SSL Pinning**
```bash
# Em outro terminal
frida -U -f com.nu.production -l ssl-kill-switch2.js --no-pause
```

### **Visual no Terminal:**
```
    _____
   (     )
   |  o  |  Frida
   | ___ |  Server
   '-----'  Running!

[+] SSL Kill Switch engaged
[+] App: com.nu.production
[+] Hooks installed successfully
```

---

## ✅ **TESTE DE VERIFICAÇÃO**

### **1. Verificar Conectividade**
```
No emulador → Browser → http://burp

┌─────────────────────────────────────┐
│     🎯 Burp Suite                   │
│                                     │
│  Professional / Community           │
│                                     │
│  ✅ Proxy is working!               │
└─────────────────────────────────────┘
```

### **2. Verificar App Nubank**
```
1. Abrir app Nubank
2. Fazer login
3. Verificar Burp → HTTP History

Deve aparecer:
┌─────────────────────────────────────┐
│ GET  api.nubank.com.br/login        │
│ POST api.nubank.com.br/auth         │
│ GET  api.nubank.com.br/balance      │
│ ✅ X-Correlation-Id: bc-handle      │
└─────────────────────────────────────┘
```

---

## 🚨 **TROUBLESHOOTING VISUAL**

### **Problema: App não carrega**
```
❌ SSL Error / Network Error

Solução:
┌─────────────────────────────────────┐
│ 1. ✅ Certificado instalado?        │
│ 2. ✅ Frida bypass ativo?           │
│ 3. ✅ Proxy configurado?            │
│ 4. ✅ Internet funcionando?         │
└─────────────────────────────────────┘
```

### **Problema: Burp não vê requisições**
```
❌ HTTP History vazio

Solução:
┌─────────────────────────────────────┐
│ 1. ✅ Proxy 8080 rodando?           │
│ 2. ✅ Emulador configurado?         │
│ 3. ✅ IP da máquina correto?        │
│ 4. ✅ Scope incluído?               │
└─────────────────────────────────────┘
```

---

## 🎯 **COMANDOS ESSENCIAIS**

### **Verificar Status**
```bash
# Dispositivos conectados
adb devices

# Proxy no emulador
adb shell settings get global http_proxy

# App Nubank instalado
adb shell pm list packages | grep com.nu.production

# Frida rodando
adb shell ps | grep frida-server
```

### **Obter IP da Máquina**
```bash
# Linux
ip route get 8.8.8.8 | awk '{print $7}'

# Ou
hostname -I | awk '{print $1}'

# Resultado esperado: 192.168.1.XXX
```

---

## 🔍 **ENDPOINTS PARA TESTAR**

### **Após configuração, interceptar:**
```http
┌─────────────────────────────────────┐
│ 🎯 PRIORITÁRIOS (P1: $2000-$4000)  │
│                                     │
│ POST /api/mobile/pix/send           │
│ POST /api/mobile/transfers/ted      │
│ GET  /api/mobile/balance/current    │
│ POST /api/mobile/auth/login         │
│ GET  /api/mobile/statements/123     │
│                                     │
│ ✅ Sempre com X-Correlation-Id     │
└─────────────────────────────────────┘
```

### **Testes BAC/IDOR:**
```http
Original: GET /api/mobile/balance/123456
Testar:   GET /api/mobile/balance/123457  ← BAC Horizontal
Testar:   GET /api/mobile/balance/123455  ← IDOR
Testar:   GET /api/mobile/balance/000001  ← Admin access
```

---

## 📋 **WORKFLOW COMPLETO**

```
1. 🔧 Execute: ./setup_burp_nubank.sh --auto
2. 📱 Inicie emulador Android
3. 🔗 Configure proxy no emulador
4. 📜 Instale certificado Burp
5. 🛡️ Execute Frida bypass
6. 📲 Instale app Nubank
7. 🔑 Faça login no app
8. 🎯 Intercepte com Burp
9. 🚨 Teste BAC/IDOR
10. 💰 Encontre P1 ($2000-$4000)
```

---

**⚠️ LEMBRE-SE:**
- **X-Correlation-Id: bc-handle** (OBRIGATÓRIO)
- **Máximo R$ 10** em PoCs financeiros
- **Foco em P1** ($2000-$4000)
- **Compliance total** com regras

**🎯 OBJETIVO: Vulnerabilidades de alto valor com setup perfeito!**
