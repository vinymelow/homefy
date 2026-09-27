---
task: smokeTestProjectStructure()
responsavel: "@ecommerce-master"
responsavel_type: Agente
atomic_layer: Analysis
Entrada: |
  - project_root: diretório local do Homefy, somente leitura
  - task_scope: estrutura top-level e ecom-stack/
Saida: |
  - structure_report: resumo de no máximo 10 linhas em output.md
  - result_contract: result.json com status e metadados da execução
Checklist:
  - "[ ] Não modificar ficheiros"
  - "[ ] Não acessar a rede"
  - "[ ] Não revelar valores de .env"
  - "[ ] Listar componentes principais e quantidade aproximada de ficheiros"
---

# Task: smoke-test-project-structure (TESTE NÃO DESTRUTIVO)

**Objetivo**: validar a cadeia AIOX → task → Hermes → resultado.

**Instrução para o executor**:

Analisa a estrutura do projeto no diretório de trabalho. Lista os diretórios
principais (top-level e ecom-stack/) e responde em no máximo 10 linhas com:
(1) número aproximado de ficheiros, (2) componentes principais encontrados,
(3) um aviso se encontrares algum ficheiro `.env` com valores preenchidos
(NÃO reveles os valores — apenas indica se existe).

Não modifiques nenhum ficheiro. Não acedas à rede. Apenas leitura local.
