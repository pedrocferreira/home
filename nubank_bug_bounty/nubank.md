Nubank Bug Bounty Hacking Guide (Financeiro)
Este guia serve como referência rápida e conjunto de instruções de foco para testes no programa de Bug Bounty do Nubank, com ênfase em ativos críticos, lógica de negócios e regras de compliance.

1. Foco Principal: Aplicações Móveis e Lógica de Negócios (Core Assets)
A maior recompensa e foco está nos Core Assets (P1: $2000 – $4000 base). Por ser uma plataforma bancária, a prioridade máxima é integridade financeira e controle de acesso.

Alvo	Tipo de Teste de Foco	Recompensa Base (P1)
Nubank Android / iOS	Broken Access Control (BAC): Tentar realizar ações financeiras (transferência, pagamento, ajuste de limite) em nome de outro usuário ou sem autenticação/autorização correta. Falhas de Lógica de Negócios (Bypass de limite, transação duplicada).	$2000 – $4000
prod-*.nubank.com.br	Injeções de Alto Impacto: SQLi, Code Injection, SSRF que possam comprometer dados ou fundos.	$2000 – $4000
*.nuinvest.com.br	Lógica de Investimento: Testar a integridade de cálculo de rendimentos, resgates, ou manipulação de cotas/ativos.	P1: $500 – $1000

Exportar para as Planilhas
2. Requisitos e Regras Cruciais (Compliance)
É MANDATÓRIO seguir estas regras para evitar bloqueios ou desqualificação:

Requisitos de Conta
Crie uma conta usando seu CPF/TIN real (se você tiver). Testar com uma conta autenticada é encorajado.

O uso de identificação falsa é explicitamente Fora do Escopo.

Regras de Teste
HEADER OBRIGATÓRIO: Use o header X-Correlation-Id: bc-handle em suas requisições.

Limite de PoC: Para PoCs envolvendo transações ou valores monetários, o valor máximo é de R$ 10 (ou o mínimo possível).

Foco em Impacto: Relatos devem incluir passos de replicação detalhados e um cenário de exploração real.

Não DoS/DDoS: Evite qualquer atividade que cause interrupção ou degradação do serviço. Se for bloqueado, notifique-os.

3. Vulnerabilidades-Chave e Oportunidades
Foque em vulnerabilidades que afetam diretamente o dinheiro, a privacidade e a segurança das contas.

Testes de Controle de Acesso e Autorização
BAC (Horizontal/Vertical) e IDOR: Tentar visualizar, modificar ou transferir dados/fundos de outra conta alterando IDs de conta/transação, tokens ou parâmetros de API.

Transações Não Autorizadas: Tentar iniciar, confirmar ou cancelar uma transação sem o token ou etapa de verificação de segurança (ex: senha de 4 dígitos, biometria).

Condições de Corrida (Race Condition): Tentar explorar o processamento simultâneo de transações para duplicar fundos, resgatar duas vezes, ou burlar limites.

Testes de Injeção
SSRF (Server-Side Request Forgery): Buscar funcionalidades que buscam dados de URLs externas.

Injeções em APIs: Focar nos endpoints prod-*. e nos wildcards (*.nubank.com.br), procurando por Injeção de SQL ou comandos.

Testes em Mobile Específicos
Intercepte todo o tráfego da API dos aplicativos Android e iOS.

Procure por hardcoding de chaves secretas, falhas no armazenamento de tokens ou dados sensíveis em logs do dispositivo.

4. Áreas Fora do Escopo (Out of Scope) - EVITAR
EVITE rigorosamente para não perder tempo e não ter o relatório desqualificado:

Subdomain Takeover: Explicitamente NÃO elegível para recompensa.

DOS/DDoS: Qualquer atividade que cause interrupção ou degradação do serviço.

Social Engineering.

CSRF em formulários não autenticados ou sem ações sensíveis.

Problemas de Configuração de Segurança Baixa (Ex: Missing HttpOnly/Secure flags, Missing CSP, Missing email best practices - SPF/DKIM/DMARC).

Open Redirect: A menos que você demonstre um impacto de segurança adicional (ex: roubo de token de sessão).

LLM Based Applications (temporariamente fora do escopo).

5. Instruções para o Cursor
Siga estas instruções ao analisar o código ou sugerir payloads:

Priorize: BAC, IDOR e Falhas Lógicas que resultem em perda/roubo de fundos ou dados.

NUNCA SUGIRA um PoC de transação que exceda R$ 10.

Lembre-se do header de correlação: X-Correlation-Id: bc-handle é essencial.

Ataques que exigem MITM ou acesso físico ao dispositivo do usuário são Fora do Escopo.

[FIM DO ARQUIVO]