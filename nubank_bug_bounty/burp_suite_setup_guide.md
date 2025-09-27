# 🔧 Burp Suite Setup - Configuração Completa para Nubank

## 📋 **PRÉ-REQUISITOS**

### **Software Necessário**
- Burp Suite Professional (recomendado) ou Community
- Android Studio + Emulador Android
- ADB (Android Debug Bridge)
- Java 11+ instalado

### **Downloads**
```bash
# Burp Suite
# https://portswigger.net/burp/communitydownload
# ou Professional: https://portswigger.net/burp/pro

# Android Studio
# https://developer.android.com/studio

# Frida (para bypass certificate pinning)
pip install frida-tools
```

---

## 🚀 **PASSO 1: Configuração Inicial do Burp Suite**

### **1.1 Iniciar Burp Suite**
```bash
# Executar Burp Suite
java -jar burpsuite_community.jar
# ou se Professional:
java -jar burpsuite_pro.jar
```

### **1.2 Configurar Proxy**
1. Ir em **Proxy → Options**
2. **Proxy Listeners:**
   - Porta: `8080`
   - IP: `All interfaces` (ou específico da sua rede)
   - Marcar: `Support invisible proxying`

### **1.3 Interceptação**
1. **Proxy → Intercept**
2. Deixar **Intercept is off** inicialmente
3. Ativar quando necessário para análise

---

## 📱 **PASSO 2: Configuração do Emulador Android**

### **2.1 Criar AVD (Android Virtual Device)**
```bash
# Abrir Android Studio
# Tools → AVD Manager → Create Virtual Device

# Configurações recomendadas:
- Device: Pixel 4 ou 5
- Android 10 (API 29) ou 11 (API 30)
- RAM: 4GB+
- Storage: 8GB+
- Google Play Store: SIM
```

### **2.2 Configurar Proxy no Emulador**
```bash
# Método 1: Via Interface
Settings → Wi-Fi → Long press WiFi → Modify Network
→ Advanced Options → Proxy → Manual
→ Hostname: [IP_DA_SUA_MAQUINA]
→ Port: 8080

# Método 2: Via ADB
adb shell settings put global http_proxy [IP]:[PORTA]
```

### **2.3 Verificar IP da Máquina**
```bash
# Linux/Mac
ip addr show | grep inet
# ou
ifconfig | grep inet

# Windows
ipconfig | findstr IPv4
```

---

## 🔐 **PASSO 3: Instalação do Certificado CA**

### **3.1 Exportar Certificado do Burp**
1. **Proxy → Options → Import/Export CA Certificate**
2. **Export → Certificate in DER format**
3. Salvar como `burp-ca-cert.der`

### **3.2 Converter para formato Android**
```bash
# Converter DER para PEM
openssl x509 -inform DER -in burp-ca-cert.der -out burp-ca-cert.pem

# Obter hash do certificado
openssl x509 -inform PEM -subject_hash_old -in burp-ca-cert.pem | head -1

# Renomear arquivo (exemplo com hash 9a5ba575)
cp burp-ca-cert.pem 9a5ba575.0
```

### **3.3 Instalar Certificado no Android**
```bash
# Método 1: Via ADB (Root necessário)
adb root
adb remount
adb push 9a5ba575.0 /system/etc/security/cacerts/
adb shell chmod 644 /system/etc/security/cacerts/9a5ba575.0
adb reboot

# Método 2: Via Interface (Menos efetivo)
Settings → Security → Install from storage → burp-ca-cert.der
```

---

## 🛡️ **PASSO 4: Bypass Certificate Pinning**

### **4.1 Instalar Frida**
```bash
# No computador
pip install frida-tools

# No dispositivo Android (via GitHub releases)
# https://github.com/frida/frida/releases
# Baixar frida-server para arquitetura do device
```

### **4.2 Configurar Frida Server**
```bash
# Fazer upload do frida-server
adb push frida-server-15.2.2-android-x86_64 /data/local/tmp/frida-server
adb shell chmod 755 /data/local/tmp/frida-server

# Executar frida-server
adb shell /data/local/tmp/frida-server &
```

### **4.3 Script de Bypass SSL Pinning**
```bash
# Baixar script universal
wget https://raw.githubusercontent.com/frida/frida/main/scripts/ssl-kill-switch2.js

# Usar com app Nubank
frida -U -f com.nu.production -l ssl-kill-switch2.js --no-pause
```

---

## 📱 **PASSO 5: Instalação do App Nubank**

### **5.1 Baixar Nubank**
```bash
# Via Google Play Store no emulador
# ou via APK Mirror (versão específica)
# https://www.apkmirror.com/apk/nu-pagamentos-s-a/nubank/
```

### **5.2 Configurar Conta**
```bash
# IMPORTANTE: Usar CPF real (conforme compliance)
# Email: [seu_email_real]
# CPF: [seu_cpf_real]
# Senha: [senha_segura]
```

---

## 🔍 **PASSO 6: Configuração Específica para Nubank**

### **6.1 Headers Obrigatórios no Burp**
1. **Proxy → Options → Match and Replace**
2. **Add rule:**
   ```
   Type: Request header
   Match: ^X-Correlation-Id.*
   Replace: X-Correlation-Id: bc-handle
   ```

### **6.2 Configurar User-Agent Móvel**
```http
User-Agent: Nubank/8.45.0 (Android 10; SM-G975F)
X-Platform: android
X-App-Version: 8.45.0
X-Device-Model: SM-G975F
X-OS-Version: 10
```

### **6.3 Scope Configuration**
1. **Target → Scope → Add**
2. Incluir:
   ```
   *.nubank.com.br
   *.nuinvest.com.br
   prod-*.nubank.com.br
   ```

---

## 🎯 **PASSO 7: Teste de Conectividade**

### **7.1 Verificar Proxy**
```bash
# No emulador, abrir navegador
# Ir para: http://burp
# Deve mostrar página do Burp Suite
```

### **7.2 Teste com App Nubank**
```bash
# Abrir app Nubank
# Fazer login
# Verificar no Burp → HTTP History
# Deve aparecer requisições para *.nubank.com.br
```

### **7.3 Verificar Header Obrigatório**
```http
# Todas as requisições devem ter:
X-Correlation-Id: bc-handle
```

---

## 🔧 **PASSO 8: Configurações Avançadas**

### **8.1 Session Handling**
1. **Project Options → Sessions**
2. **Add macro** para capturar tokens
3. **Configure scope** para aplicar em *.nubank.com.br

### **8.2 Extensions Úteis**
```
- Autorize (para teste de autorização)
- Logger++ (logging avançado)
- JSON Beautifier
- Request Timer
- Turbo Intruder (para race conditions)
```

### **8.3 Configurar Intruder para Race Conditions**
1. **Intruder → Positions**
2. **Attack type: Pitchfork**
3. **Resource pool: Create new resource pool**
4. **Concurrent requests: 5-10**

---

## 📊 **PASSO 9: Organização do Workspace**

### **9.1 Criar Projeto Específico**
```
File → New project on disk
Nome: nubank_bug_bounty
Salvar em: /home/burp_projects/
```

### **9.2 Configurar Target Sitemap**
1. **Target → Site map**
2. **Add scope** para organizar endpoints
3. **Filter by MIME type: JSON, HTML**

### **9.3 Organizar Requisições**
```bash
# Criar pastas no sitemap:
- Authentication
- Transactions
- PIX
- Investments
- Profile_Data
```

---

## 🚨 **PASSO 10: Verificação Final**

### **10.1 Checklist de Configuração**
- [ ] Proxy 8080 funcionando
- [ ] Certificado CA instalado no Android
- [ ] Frida bypass SSL pinning ativo
- [ ] App Nubank instalado e funcionando
- [ ] Header X-Correlation-Id configurado
- [ ] Scope definido para domínios Nubank
- [ ] Extensions úteis instaladas

### **10.2 Teste de Interceptação**
```bash
# No app Nubank:
1. Fazer login
2. Verificar saldo
3. Tentar transferência (sem executar)

# No Burp deve aparecer:
- Requisições de autenticação
- Consultas de saldo
- APIs de transferência
```

---

## 🔍 **TROUBLESHOOTING**

### **Problema: Certificado não aceito**
```bash
# Solução:
1. Verificar se está em /system/etc/security/cacerts/
2. Verificar permissões (644)
3. Tentar MagiskTrustUserCerts module
```

### **Problema: SSL Pinning não contornado**
```bash
# Solução:
1. Verificar se frida-server está rodando
2. Tentar diferentes scripts de bypass
3. Usar Xposed Framework como alternativa
```

### **Problema: App não conecta via proxy**
```bash
# Solução:
1. Verificar IP e porta do proxy
2. Testar conectividade: ping [IP_MAQUINA]
3. Verificar firewall/iptables
4. Usar "Support invisible proxying"
```

### **Problema: Header X-Correlation-Id não aparece**
```bash
# Solução:
1. Verificar Match and Replace rules
2. Adicionar manualmente em cada request
3. Usar macro para injeção automática
```

---

## 💡 **DICAS AVANÇADAS**

### **Performance**
```bash
# Aumentar memory para Java
java -Xmx4g -jar burpsuite_pro.jar

# Configurar thread pool
Project Options → HTTP → Thread pool size: 20
```

### **Backup e Restore**
```bash
# Backup regular do projeto
Burp → Project → Save copy
Nome: nubank_backup_YYYY-MM-DD.burp
```

### **Logging Detalhado**
```bash
# Enable logging
Extender → Extensions → Logger++
Configure → Enable auto logging
Filter: *.nubank.com.br
```

---

## 🎯 **PRÓXIMOS PASSOS**

Após configuração completa:

1. **Executar**: `nubank_bac_tester.py`
2. **Interceptar**: Transações reais no app
3. **Testar**: Manipulação de IDs sistematicamente
4. **Documentar**: Vulnerabilidades encontradas
5. **Submeter**: Relatórios P1 ($2000-$4000)

---

**⚠️ CRITICAL: Sempre incluir X-Correlation-Id: bc-handle**
**💰 LIMIT: Máximo R$ 10 em PoCs financeiros**
**🎯 FOCUS: Vulnerabilidades P1 ($2000-$4000)**
