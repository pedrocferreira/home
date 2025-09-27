#!/bin/bash
# Script automatizado para configurar Burp Suite para testes no Nubank
# Uso: ./setup_burp_nubank.sh

set -e

echo "🔧 Configurando Burp Suite para Nubank Bug Bounty..."
echo "=================================================="

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Funções auxiliares
print_step() {
    echo -e "${BLUE}[STEP]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar dependências
check_dependencies() {
    print_step "Verificando dependências..."
    
    # Java
    if command -v java &> /dev/null; then
        java_version=$(java -version 2>&1 | head -n 1 | awk -F '"' '{print $2}')
        print_success "Java encontrado: $java_version"
    else
        print_error "Java não encontrado. Instale Java 11+:"
        echo "  sudo apt install openjdk-11-jdk"
        exit 1
    fi
    
    # ADB
    if command -v adb &> /dev/null; then
        print_success "ADB encontrado"
    else
        print_warning "ADB não encontrado. Instalando..."
        sudo apt update && sudo apt install -y android-tools-adb
    fi
    
    # Python e pip
    if command -v python3 &> /dev/null && command -v pip3 &> /dev/null; then
        print_success "Python3 e pip3 encontrados"
    else
        print_error "Python3 ou pip3 não encontrados"
        exit 1
    fi
    
    # OpenSSL
    if command -v openssl &> /dev/null; then
        print_success "OpenSSL encontrado"
    else
        print_error "OpenSSL não encontrado. Instale com: sudo apt install openssl"
        exit 1
    fi
}

# Instalar Frida
install_frida() {
    print_step "Instalando Frida..."
    
    if pip3 show frida-tools &> /dev/null; then
        print_success "Frida já instalado"
    else
        print_step "Instalando frida-tools..."
        pip3 install frida-tools
        print_success "Frida instalado com sucesso"
    fi
}

# Baixar Frida Server
download_frida_server() {
    print_step "Baixando Frida Server..."
    
    FRIDA_VERSION="15.2.2"
    FRIDA_ARCH="x86_64"  # Para emulador
    FRIDA_FILE="frida-server-${FRIDA_VERSION}-android-${FRIDA_ARCH}"
    
    if [ ! -f "${FRIDA_FILE}" ]; then
        print_step "Baixando ${FRIDA_FILE}..."
        wget -q "https://github.com/frida/frida/releases/download/${FRIDA_VERSION}/${FRIDA_FILE}.xz"
        xz -d "${FRIDA_FILE}.xz"
        chmod +x "${FRIDA_FILE}"
        print_success "Frida Server baixado"
    else
        print_success "Frida Server já existe"
    fi
}

# Baixar script SSL Kill Switch
download_ssl_bypass() {
    print_step "Baixando script SSL bypass..."
    
    if [ ! -f "ssl-kill-switch2.js" ]; then
        wget -q -O ssl-kill-switch2.js "https://raw.githubusercontent.com/frida/frida/main/src/android/lib/ssl-kill-switch2.js"
        print_success "Script SSL bypass baixado"
    else
        print_success "Script SSL bypass já existe"
    fi
}

# Configurar certificado Burp
setup_burp_certificate() {
    print_step "Configurando certificado Burp..."
    
    if [ ! -f "burp-ca-cert.der" ]; then
        print_warning "Certificado Burp não encontrado!"
        echo "Para configurar o certificado:"
        echo "1. Abra Burp Suite"
        echo "2. Proxy → Options → Import/Export CA Certificate"
        echo "3. Export → Certificate in DER format"
        echo "4. Salve como 'burp-ca-cert.der' neste diretório"
        echo "5. Execute este script novamente"
        return 1
    fi
    
    # Converter DER para PEM
    if [ ! -f "burp-ca-cert.pem" ]; then
        print_step "Convertendo certificado DER para PEM..."
        openssl x509 -inform DER -in burp-ca-cert.der -out burp-ca-cert.pem
    fi
    
    # Obter hash do certificado
    CERT_HASH=$(openssl x509 -inform PEM -subject_hash_old -in burp-ca-cert.pem | head -1)
    CERT_FILE="${CERT_HASH}.0"
    
    if [ ! -f "${CERT_FILE}" ]; then
        print_step "Criando arquivo de certificado com hash: ${CERT_HASH}"
        cp burp-ca-cert.pem "${CERT_FILE}"
        print_success "Certificado preparado: ${CERT_FILE}"
    fi
    
    echo "Para instalar no Android:"
    echo "  adb root"
    echo "  adb remount"
    echo "  adb push ${CERT_FILE} /system/etc/security/cacerts/"
    echo "  adb shell chmod 644 /system/etc/security/cacerts/${CERT_FILE}"
    echo "  adb reboot"
}

# Verificar emulador Android
check_emulator() {
    print_step "Verificando emulador Android..."
    
    if adb devices | grep -q "emulator"; then
        print_success "Emulador Android detectado"
        
        # Verificar versão Android
        android_version=$(adb shell getprop ro.build.version.release)
        print_success "Android versão: $android_version"
        
        return 0
    else
        print_warning "Nenhum emulador Android detectado"
        echo "Para configurar emulador:"
        echo "1. Abra Android Studio"
        echo "2. Tools → AVD Manager"
        echo "3. Create Virtual Device"
        echo "4. Escolha Pixel 4/5 com Android 10+"
        echo "5. Inicie o emulador"
        return 1
    fi
}

# Configurar proxy no emulador
setup_emulator_proxy() {
    print_step "Configurando proxy no emulador..."
    
    if ! adb devices | grep -q "emulator"; then
        print_error "Emulador não detectado"
        return 1
    fi
    
    # Obter IP da máquina
    LOCAL_IP=$(ip route get 8.8.8.8 | awk -F"src " 'NR==1{split($2,a," ");print a[1]}')
    PROXY_PORT="8080"
    
    print_step "Configurando proxy para ${LOCAL_IP}:${PROXY_PORT}"
    
    # Configurar proxy via ADB
    adb shell settings put global http_proxy "${LOCAL_IP}:${PROXY_PORT}"
    
    print_success "Proxy configurado no emulador"
    print_warning "Teste abrindo navegador e indo para: http://burp"
}

# Instalar Frida Server no dispositivo
install_frida_server_device() {
    print_step "Instalando Frida Server no dispositivo..."
    
    if ! adb devices | grep -q "emulator"; then
        print_error "Emulador não detectado"
        return 1
    fi
    
    FRIDA_VERSION="15.2.2"
    FRIDA_ARCH="x86_64"
    FRIDA_FILE="frida-server-${FRIDA_VERSION}-android-${FRIDA_ARCH}"
    
    if [ ! -f "${FRIDA_FILE}" ]; then
        print_error "Frida Server não encontrado. Execute download_frida_server primeiro"
        return 1
    fi
    
    # Upload para dispositivo
    adb push "${FRIDA_FILE}" /data/local/tmp/frida-server
    adb shell chmod 755 /data/local/tmp/frida-server
    
    print_success "Frida Server instalado no dispositivo"
    
    # Instruções para executar
    echo "Para executar Frida Server:"
    echo "  adb shell /data/local/tmp/frida-server &"
    echo ""
    echo "Para usar bypass SSL:"
    echo "  frida -U -f com.nu.production -l ssl-kill-switch2.js --no-pause"
}

# Criar arquivo de configuração Burp
create_burp_config() {
    print_step "Criando configuração Burp..."
    
    cat > burp_nubank_config.json << 'EOF'
{
  "proxy": {
    "http_listeners": [
      {
        "enabled": true,
        "interface": "all_interfaces",
        "port": 8080,
        "invisible_proxying": true
      }
    ]
  },
  "match_replace_rules": [
    {
      "enabled": true,
      "rule_type": "request_header",
      "match": "^X-Correlation-Id.*",
      "replace": "X-Correlation-Id: bc-handle",
      "comment": "Nubank required header"
    }
  ],
  "scope": {
    "include": [
      "*.nubank.com.br",
      "*.nuinvest.com.br",
      "prod-*.nubank.com.br"
    ]
  }
}
EOF
    
    print_success "Configuração Burp criada: burp_nubank_config.json"
}

# Criar script helper
create_helper_scripts() {
    print_step "Criando scripts auxiliares..."
    
    # Script para iniciar Frida
    cat > start_frida.sh << 'EOF'
#!/bin/bash
echo "🔧 Iniciando Frida Server..."
adb shell /data/local/tmp/frida-server &
sleep 3

echo "🛡️ Iniciando bypass SSL Pinning..."
frida -U -f com.nu.production -l ssl-kill-switch2.js --no-pause
EOF
    chmod +x start_frida.sh
    
    # Script para verificar setup
    cat > check_setup.sh << 'EOF'
#!/bin/bash
echo "🔍 Verificando setup Burp + Android..."
echo "=================================="

echo "1. Verificando ADB devices:"
adb devices

echo -e "\n2. Verificando proxy no emulador:"
adb shell settings get global http_proxy

echo -e "\n3. Verificando Frida Server:"
if adb shell ps | grep frida-server; then
    echo "✅ Frida Server rodando"
else
    echo "❌ Frida Server não está rodando"
fi

echo -e "\n4. Verificando app Nubank:"
if adb shell pm list packages | grep com.nu.production; then
    echo "✅ App Nubank instalado"
else
    echo "❌ App Nubank não encontrado"
fi

echo -e "\n5. Teste de conectividade:"
echo "Abra o navegador no emulador e vá para: http://burp"
EOF
    chmod +x check_setup.sh
    
    print_success "Scripts auxiliares criados"
}

# Menu principal
main_menu() {
    echo ""
    echo "🎯 Setup Burp Suite para Nubank - Menu Principal"
    echo "=============================================="
    echo "1. Verificar dependências"
    echo "2. Instalar Frida"
    echo "3. Baixar Frida Server"
    echo "4. Baixar script SSL bypass"
    echo "5. Configurar certificado Burp"
    echo "6. Verificar emulador Android"
    echo "7. Configurar proxy no emulador"
    echo "8. Instalar Frida Server no dispositivo"
    echo "9. Criar configuração Burp"
    echo "10. Criar scripts auxiliares"
    echo "11. Setup completo automatizado"
    echo "12. Verificar setup"
    echo "0. Sair"
    echo ""
    read -p "Escolha uma opção [0-12]: " choice
    
    case $choice in
        1) check_dependencies ;;
        2) install_frida ;;
        3) download_frida_server ;;
        4) download_ssl_bypass ;;
        5) setup_burp_certificate ;;
        6) check_emulator ;;
        7) setup_emulator_proxy ;;
        8) install_frida_server_device ;;
        9) create_burp_config ;;
        10) create_helper_scripts ;;
        11) run_full_setup ;;
        12) ./check_setup.sh 2>/dev/null || echo "Execute opção 10 primeiro" ;;
        0) exit 0 ;;
        *) echo "Opção inválida" ;;
    esac
}

# Setup completo
run_full_setup() {
    print_step "Executando setup completo..."
    
    check_dependencies
    install_frida
    download_frida_server
    download_ssl_bypass
    create_burp_config
    create_helper_scripts
    
    print_success "Setup básico concluído!"
    print_warning "Próximos passos manuais:"
    echo "1. Configurar certificado Burp (opção 5)"
    echo "2. Iniciar emulador Android"
    echo "3. Configurar proxy no emulador (opção 7)"
    echo "4. Instalar Frida Server no dispositivo (opção 8)"
    echo "5. Instalar app Nubank"
    echo "6. Executar ./check_setup.sh para verificar"
}

# Main
if [ "$1" = "--auto" ]; then
    run_full_setup
else
    while true; do
        main_menu
        echo ""
        read -p "Pressione Enter para continuar..."
    done
fi
