#!/bin/bash
# Script para criar repositório GitHub do projeto Nubank Bug Bounty
# Uso: ./create_github_repo.sh

set -e

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
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

print_info() {
    echo -e "${PURPLE}[INFO]${NC} $1"
}

# Banner
show_banner() {
    echo -e "${PURPLE}"
    echo "=================================================="
    echo "🏦  NUBANK BUG BOUNTY ARSENAL - GITHUB SETUP  🏦"
    echo "=================================================="
    echo -e "${NC}"
    echo ""
}

# Verificar se está no diretório correto
check_directory() {
    if [ ! -f "README_GITHUB.md" ]; then
        print_error "Execute este script do diretório /home/nubank_bug_bounty/"
        exit 1
    fi
}

# Verificar dependências
check_dependencies() {
    print_step "Verificando dependências..."
    
    # Git
    if ! command -v git &> /dev/null; then
        print_error "Git não encontrado. Instale com: sudo apt install git"
        exit 1
    fi
    
    # GitHub CLI (opcional mas recomendado)
    if command -v gh &> /dev/null; then
        print_success "GitHub CLI encontrado"
        GH_CLI=true
    else
        print_warning "GitHub CLI não encontrado"
        print_info "Para instalação automática: https://cli.github.com/"
        GH_CLI=false
    fi
}

# Configurar Git
setup_git() {
    print_step "Configurando Git..."
    
    # Verificar configuração básica
    if [ -z "$(git config --global user.name)" ]; then
        read -p "Digite seu nome para Git: " git_name
        git config --global user.name "$git_name"
    fi
    
    if [ -z "$(git config --global user.email)" ]; then
        read -p "Digite seu email para Git: " git_email
        git config --global user.email "$git_email"
    fi
    
    print_success "Git configurado"
    print_info "Nome: $(git config --global user.name)"
    print_info "Email: $(git config --global user.email)"
}

# Preparar arquivos para GitHub
prepare_files() {
    print_step "Preparando arquivos para GitHub..."
    
    # Usar README específico do GitHub
    cp README_GITHUB.md README.md
    
    # Criar estrutura de diretórios
    mkdir -p Scripts Guides Results/vulnerability_reports
    
    # Mover scripts
    mv nubank_bac_tester.py Scripts/
    mv nubank_mobile_tester.py Scripts/
    mv setup_burp_nubank.sh Scripts/
    
    # Mover guias
    mv burp_suite_setup_guide.md Guides/
    mv burp_quick_setup_visual.md Guides/
    mv nubank_mobile_interception_guide.md Guides/
    mv nubank_compliance_checklist.md Guides/
    
    # Criar arquivo de exemplo para Results
    echo "# Vulnerability Reports" > Results/README.md
    echo "" >> Results/README.md
    echo "This directory contains vulnerability reports and findings." >> Results/README.md
    echo "**Note**: Only sanitized, non-sensitive reports should be stored here." >> Results/README.md
    
    print_success "Estrutura de arquivos organizada"
}

# Inicializar repositório Git
init_git_repo() {
    print_step "Inicializando repositório Git..."
    
    if [ ! -d ".git" ]; then
        git init
        print_success "Repositório Git inicializado"
    else
        print_info "Repositório Git já existe"
    fi
    
    # Adicionar arquivos
    git add .
    git commit -m "Initial commit: Nubank Bug Bounty Arsenal v1.0.0

🎯 Features:
- Complete BAC/IDOR testing automation
- Mobile app security testing framework
- Burp Suite setup automation
- Comprehensive documentation and guides
- Compliance checklist and validation

🔧 Tools:
- Python scripts for vulnerability testing
- Bash scripts for environment setup
- Visual guides for quick configuration
- Professional documentation structure

💰 Focus: P1 vulnerabilities ($2000-$4000 rewards)
🔒 Compliance: Full adherence to Nubank Bug Bounty rules"
    
    print_success "Commit inicial criado"
}

# Criar repositório no GitHub (com GitHub CLI)
create_github_repo_cli() {
    print_step "Criando repositório no GitHub com GitHub CLI..."
    
    read -p "Nome do repositório [nubank-bug-bounty]: " repo_name
    repo_name=${repo_name:-nubank-bug-bounty}
    
    read -p "Descrição: " repo_description
    repo_description=${repo_description:-"🏦 Complete arsenal for Nubank Bug Bounty - Focus on P1 vulnerabilities ($2000-$4000)"}
    
    # Criar repositório público
    gh repo create "$repo_name" \
        --description "$repo_description" \
        --public \
        --source=. \
        --remote=origin \
        --push
    
    if [ $? -eq 0 ]; then
        print_success "Repositório criado com sucesso!"
        print_info "URL: https://github.com/$(gh api user --jq .login)/$repo_name"
    else
        print_error "Erro ao criar repositório"
        return 1
    fi
}

# Instruções para criação manual
manual_instructions() {
    print_step "Instruções para criação manual do repositório:"
    echo ""
    echo -e "${YELLOW}1. Acesse: https://github.com/new${NC}"
    echo -e "${YELLOW}2. Nome do repositório: ${BLUE}nubank-bug-bounty${NC}"
    echo -e "${YELLOW}3. Descrição: ${BLUE}🏦 Complete arsenal for Nubank Bug Bounty - Focus on P1 vulnerabilities (\$2000-\$4000)${NC}"
    echo -e "${YELLOW}4. Marque como: ${BLUE}Public${NC}"
    echo -e "${YELLOW}5. ${RED}NÃO${NC} marque 'Add a README file'${NC}"
    echo -e "${YELLOW}6. ${RED}NÃO${NC} marque 'Add .gitignore'${NC}"
    echo -e "${YELLOW}7. Escolha licença: ${BLUE}MIT License${NC}"
    echo -e "${YELLOW}8. Clique em 'Create repository'${NC}"
    echo ""
    
    read -p "Pressione Enter quando criar o repositório no GitHub..."
    
    read -p "Digite seu nome de usuário GitHub: " github_username
    read -p "Digite o nome do repositório [nubank-bug-bounty]: " repo_name
    repo_name=${repo_name:-nubank-bug-bounty}
    
    # Adicionar origin e fazer push
    git remote add origin "https://github.com/$github_username/$repo_name.git"
    git branch -M main
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        print_success "Repositório enviado com sucesso!"
        print_info "URL: https://github.com/$github_username/$repo_name"
    else
        print_error "Erro ao enviar repositório"
        return 1
    fi
}

# Configurar repositório após criação
setup_github_features() {
    print_step "Configurando features do GitHub..."
    
    if [ "$GH_CLI" = true ]; then
        # Configurar topics/tags
        print_info "Configurando topics..."
        gh repo edit --add-topic "bug-bounty,security,nubank,penetration-testing,ethical-hacking,cybersecurity,fintech,mobile-security,api-testing,burp-suite"
        
        # Configurar branch protection (se Professional)
        print_info "Para configurar branch protection, acesse:"
        print_info "Repository → Settings → Branches → Add rule"
    fi
    
    print_success "Configuração básica concluída"
}

# Finalizar e mostrar próximos passos
show_next_steps() {
    echo ""
    echo -e "${GREEN}🎉 REPOSITÓRIO CRIADO COM SUCESSO! 🎉${NC}"
    echo ""
    echo -e "${BLUE}📋 PRÓXIMOS PASSOS:${NC}"
    echo ""
    echo -e "${YELLOW}1. Customize o README.md:${NC}"
    echo "   - Adicione seu nome de usuário GitHub"
    echo "   - Atualize links de contato"
    echo "   - Adicione suas estatísticas de bug bounty"
    echo ""
    echo -e "${YELLOW}2. Configure o repositório:${NC}"
    echo "   - Settings → General → Features → Issues ✅"
    echo "   - Settings → General → Features → Wiki ✅"
    echo "   - Settings → Security → Dependency graph ✅"
    echo "   - Settings → Security → Dependabot alerts ✅"
    echo ""
    echo -e "${YELLOW}3. Adicione conteúdo adicional:${NC}"
    echo "   - Screenshots dos resultados em Results/"
    echo "   - Exemplos de uso em Scripts/"
    echo "   - Tutoriais avançados em Guides/"
    echo ""
    echo -e "${YELLOW}4. Promova o projeto:${NC}"
    echo "   - Compartilhe em comunidades de segurança"
    echo "   - Adicione em seu perfil LinkedIn"
    echo "   - Tweet sobre o projeto"
    echo ""
    echo -e "${YELLOW}5. Mantenha atualizado:${NC}"
    echo "   - Documente novos achados"
    echo "   - Atualize scripts regularmente"
    echo "   - Responda issues da comunidade"
    echo ""
    echo -e "${GREEN}🔗 LINKS ÚTEIS:${NC}"
    echo -e "📊 GitHub Analytics: ${BLUE}Repository → Insights${NC}"
    echo -e "⭐ Estrelas: ${BLUE}Promova para ganhar visibilidade${NC}"
    echo -e "🍴 Forks: ${BLUE}Facilite contribuições${NC}"
    echo -e "📝 Issues: ${BLUE}Interaja com a comunidade${NC}"
}

# Menu principal
main_menu() {
    echo ""
    echo -e "${BLUE}🎯 GitHub Repository Setup - Menu${NC}"
    echo "================================="
    echo "1. Setup completo automatizado"
    echo "2. Verificar dependências"
    echo "3. Configurar Git"
    echo "4. Preparar arquivos"
    echo "5. Inicializar repositório local"
    echo "6. Criar repositório GitHub (CLI)"
    echo "7. Instruções para criação manual"
    echo "8. Configurar features GitHub"
    echo "9. Mostrar próximos passos"
    echo "0. Sair"
    echo ""
    read -p "Escolha uma opção [0-9]: " choice
    
    case $choice in
        1) run_full_setup ;;
        2) check_dependencies ;;
        3) setup_git ;;
        4) prepare_files ;;
        5) init_git_repo ;;
        6) 
            if [ "$GH_CLI" = true ]; then
                create_github_repo_cli
            else
                print_error "GitHub CLI não disponível. Use opção 7 para criação manual."
            fi
            ;;
        7) manual_instructions ;;
        8) setup_github_features ;;
        9) show_next_steps ;;
        0) exit 0 ;;
        *) print_error "Opção inválida" ;;
    esac
}

# Setup completo
run_full_setup() {
    print_step "Executando setup completo do GitHub..."
    
    check_dependencies
    setup_git
    prepare_files
    init_git_repo
    
    if [ "$GH_CLI" = true ]; then
        echo ""
        read -p "Criar repositório automaticamente com GitHub CLI? [Y/n]: " create_auto
        if [[ $create_auto =~ ^[Yy]$ ]] || [[ -z $create_auto ]]; then
            create_github_repo_cli
            setup_github_features
        else
            manual_instructions
        fi
    else
        manual_instructions
    fi
    
    show_next_steps
}

# Main
show_banner
check_directory

if [ "$1" = "--auto" ]; then
    run_full_setup
else
    while true; do
        main_menu
        echo ""
        read -p "Pressione Enter para continuar..."
    done
fi
