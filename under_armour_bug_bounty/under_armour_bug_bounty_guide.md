Under Armour Bug Bounty Hacking Guide
Este guia serve como referência rápida e conjunto de instruções de foco para testes no programa de Bug Bounty da Under Armour, com base em sua documentação oficial.

1. Foco Principal: Dados do Atleta (High Priority)
A missão principal é proteger a Integridade, Disponibilidade e Confidencialidade dos dados do atleta.

Pilar	Testes de Foco	Recompensa Esperada
Confidencialidade	Broken Access Control (BAC) Horizontal/Vertical: Tentar acessar, modificar ou excluir dados (treinos, pedidos, fotos, dados de perfil) de outros usuários (mudando IDs/Parâmetros).	P1 / P2
Integridade	Injeção de Dados: Testar se é possível corromper ou modificar dados legítimos (ex: alterar preço de item, estatísticas de treino) através de requisições maliciosas.	P2 / P3
Privacidade	Testar rigorosamente a lógica de compartilhamento (ex: Dados marcados como "privado" devem ser inacessíveis a todos; "amigos" devem ser inacessíveis a não-amigos).	P2 / P3

Exportar para as Planilhas
2. Alvos em Escopo e Tecnologias-Chave
Priorizar testes nos seguintes domínios e tecnologias:

Targets (Alvos)
www.underarmour.com

www.underarmour.co.uk

https://api.shop.ua.com/graphql

developer.underarmour.com

Aplicativos Mobile: UA Shop iOS e UA Shop Android

Tecnologias Relevantes
GraphQL: Alvo específico (api.shop.ua.com/graphql). Procurar por injeções e ataques de lógica de query.

ReactJS / NextJS: Focar em ataques Client-Side (XSS) e Server-Side (SSRF, Injeções no backend do NextJS).

3. Vulnerabilidades-Chave e Pistas do Programa
As classificações da UA (VRT Amendments) fornecem pistas sobre o que eles se importam ou já mitigaram. Focar em P1 e P2 (UA Rating).

Vulnerabilidade	Tipo de Teste Recomendado	UA Rating
Injeção de Entidade Externa (XXE)	Buscar Endpoints que aceitam XML. Tentar ler /etc/passwd ou realizar SSRF.	P2
Cross-Site Scripting (XSS)	XSS Armazenado (Stored XSS): Injetar payloads em campos de perfil, comentários ou nomes de itens que são exibidos a outros usuários ou administradores.	P3
Subdomain Takeover	Verificar CNAMEs abandonados para subdomínios de alto impacto.	P3
Injeção de Arquivo (LFI)	Busque parâmetros de arquivo: (ex: file=, page=, include=) para tentar acessar arquivos do servidor.	P3
API Keys Privadas	Inspecionar código-fonte e tráfego de API em busca de chaves. Se com POC de uso indevido, a prioridade aumenta.	P5

Exportar para as Planilhas
4. Áreas Fora do Escopo (Out of Scope) - EVITAR
Para não perder tempo ou violar o Safe Harbor, EVITE rigorosamente:

DOS/DDOS de qualquer tipo.

Brute Force em login, esqueci a senha e account lockout.

Testar Infraestrutura ou provedores de cloud.

Faltas de SPF/DMARC ou outros registros de e-mail.

Ataques em portais administrativos ou domínios não listados (uabiz.com, investor.underarmour.com, etc.).

Bugs de baixo risco em Mobile (ex: Falta de Certificate Pinning, Falta de Obfuscation, Dados não criptografados em armazenamento externo).

5. Instruções para o Cursor
Siga estas instruções ao analisar o código ou sugerir payloads:

Priorize BAC e Injeções (XXE, SQL/GraphQL).

Sempre sugira XSS Armazenado (Stored) como prioridade sobre Refletido (Reflected), devido ao ranking da UA.

Ao analisar URLs ou parâmetros, sugira manipulações de ID para testar BAC Horizontal.

Lembre-se do foco principal: Proteger o athlete_data (dados do atleta).

NÃO sugira ataques DoS ou Brute Force.