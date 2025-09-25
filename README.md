# Trabalho 1 — Engenharia de Requisitos 🚀

**Universidade Tecnológica Federal do Paraná (UTFPR)**
**Apucarana - Paraná · 2025**

---

## 👥 Equipe

* **Millena Sartori de Oliveira** — RA: 2553147
* **Maria Eduarda Mafra** — RA: 2553120
* **João Antônio Sitta Martins** — RA: 2553058

---

## 📝 Resumo do projeto

**Lu Mafra Personal Trainer** é uma academia voltada ao público feminino cujo gerenciamento atual é manual (planilhas, cadernos e livro-caixa). O projeto propõe um sistema para **automatizar e centralizar** o gerenciamento financeiro e operacional: mensalidades, contas a pagar, cadastro de alunas e horários, substituindo o uso parcial do TecnoFit. 💪✨

---

## 🎯 Objetivo

Desenvolver um **protótipo funcional** e a documentação de requisitos para um sistema interno que permita à proprietária:

* Controlar mensalidades (recebimentos e cobranças) 💸
* Gerenciar contas a pagar/receber 🧾
* Fazer cadastro digital de alunas 🧑‍🤝‍🧑
* Administrar horários de aulas e evitar conflitos 🗓️
* Receber notificações apenas para a administradora sobre pagamentos atrasados (após 3 dias) 🔔

O sistema deve ser acessível via **computador e celular** (versão sucinta) 📱💻.

---

## 🔍 Levantamento de Requisitos

Método: **entrevista** com a proprietária (Lu Mafra).
Principais pontos:

* Processos financeiros manuais com alta chance de erro ❌
* Necessidade de centralizar geração de comprovantes (substituir TecnoFit) 🧾➡️📲
* Preferência por muitas funcionalidades (prioridade funcional sobre visual) ✅
* Notificações apenas para administradora após 3 dias de atraso 🔔
* Relatórios detalhados não são prioritários no momento 📉 (podem vir depois)

---

## 🗣️ Histórias de Usuário (seleção)

**Proprietária / Administradora**

* *Como proprietária*, quero controlar mensalidades para não perder pagamentos.
* *Como proprietária*, quero um cadastro digital de alunas para substituir papéis.
* *Como proprietária*, quero gerenciar horários para evitar conflitos.
* *Como proprietária*, quero notificações só para mim sobre atrasos (após 3 dias).

**Desenvolvimento / Equipe**

* *Como desenvolvedor*, quero usar Scrum, Trello e GitHub para organizar o projeto. 🛠️
* *Como desenvolvedor*, quero contato direto com o cliente para aprimorar o sistema. 🤝

---

## ✅ Funcionalidades mínimas (MVP)

1. Autenticação (admin). 🔒
2. Dashboard financeiro (lista de mensalidades: pago / pendente / atrasado). 📊
3. Formulário de cadastro de aluna (dados pessoais e plano). 📝
4. Agenda de horários (criação/edição e checagem de conflitos). 🗓️
5. Geração/envio de comprovantes integrado ao sistema (substitui TecnoFit). 📤
6. Notificações internas para a proprietária sobre pagamentos atrasados (regra: 3 dias). 🔔

---

## 🧩 Protótipo & Diagramas

Protótipos sugeridos (implementar em `/docs`):

* `imagem1_interna_app.png` — demonstração da parte interna do app 🖼️
* `imagem2_home_page.png` — possível página inicial 🏠
* `diagrama_sequencia.png` — fluxos: cadastro → cobrança → envio de comprovante → notificação 🔁

Prototipar telas mínimas:

* Tela de login (admin) 🔐
* Dashboard financeiro (lista de mensalidades) 💳
* Formulário de cadastro de aluna 🧾
* Agenda de horários 📆
* Tela de notificações/alertas 🔔

---

## ⚙️ Requisitos não-funcionais (resumo)

* Responsividade (desktop + mobile). 📱💻
* Backup/persistência dos dados (preferência por solução em nuvem). ☁️
* Interface simples e direta (fácil uso para o cliente). 🎯

---

## 🛠️ Ferramentas e processo

* Metodologia: **Scrum**. 🏃‍♀️
* Gestão: **Trello** e **GitHub** (repositório do projeto). 📋🔗
* Comunicação constante com o cliente para validação das entregas. 💬

---

## 📂 Estrutura sugerida do repositório

```
/docs
  ├─ imagem1_interna_app
  ├─ imagem2_home_page
  └─ diagrama_sequencia
/src
  └─ (código do protótipo)
README.md
