# DevOps Lab - Flask + PostgreSQL + Docker

![CI Pipeline](https://github.com/Sanxpher/devops-lab/actions/workflows/ci.yml/badge.svg)

Este é o primeiro estágio do meu laboratório de DevOps, focado na containerização de uma aplicação web e banco de dados relacional.

## 🎯 O que este projeto faz
Uma API REST simples (To-Do List) escrita em Python/Flask, conectada a um banco PostgreSQL, totalmente orquestrada via Docker Compose.

## 🛠️ Tecnologias
- **Linguagem:** Python 3.12 (Flask, SQLAlchemy)
- **Banco de Dados:** PostgreSQL 16
- **Infraestrutura:** Docker, Docker Compose
- **Segurança:** Gestão de segredos via `.env` (excluído do Git)

## 🚀 Como rodar
1. Clone o repositório:
   \`\`\`bash
   git clone https://github.com/Sanxpher/devops-lab.git
   cd devops-lab
   \`\`\`
2. Crie o arquivo `.env` com as credenciais do banco (veja `.env.example`).
3. Suba os containers:
   \`\`\`bash
   docker compose up -d --build
   \`\`\`
4. Acesse a API: `http://localhost:5000/health`

## 🩺 Troubleshooting (Problemas Comuns e Soluções)
- **Erro de Driver no PostgreSQL:** Se a API falhar ao conectar, verifique se o `psycopg` está instalado corretamente. Migramos do `psycopg2` para o `psycopg` v3 para garantir compatibilidade.
- **Cache do Docker:** Se o Docker insistir em usar uma versão antiga da imagem, use `docker compose down --rmi all -v` para limpar as camadas de cache e volumes locais.
- **OneDrive interferindo no Docker:** Se o projeto estiver dentro de pastas sincronizadas do OneDrive, o Docker pode falhar ao ler arquivos. Recomenda-se mover o repositório para um diretório local fora da sincronização em nuvem.

## 🗺️ Roadmap
- [x] Fase 1: Containerização da API (Docker/Compose) e Banco de Dados.
- [x] Fase 2: CI/CD - Pipeline automatizado com GitHub Actions (Testes + Docker Build).
- [ ] Fase 3: Orquestração com Kubernetes e Infraestrutura como Código.
- [ ] Fase 4: DevSecOps (Segurança no Pipeline) e Monitoramento.
