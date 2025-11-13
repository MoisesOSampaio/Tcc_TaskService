# TCC - Task Service (Microsserviço de Tarefas) 🤖

![Status do Projeto](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Linguagem](https://img.shields.io/badge/linguagem-Java-blue)
![Framework](https://img.shields.io/badge/framework-Spring%20Boot-green)

Este repositório contém o código-fonte do **Task Service**, um microsserviço fundamental para o nosso projeto de Gerenciamento de Equipes Ágeis.

## 🎯 Sobre o Projeto Geral

O projeto completo é uma plataforma de gerenciamento de equipes e projetos (similar ao Trello), com um diferencial inovador: a atribuição de tarefas é otimizada por uma Inteligência Artificial que analisa as habilidades (_skills_) de cada desenvolvedor.

Este microsserviço, o **Task Service**, é o cérebro por trás da gestão das tarefas e a principal ponte de comunicação com o serviço de IA.

## 🚀 O Papel do Task Service

A responsabilidade principal deste serviço é:
1.  **Gerenciar o ciclo de vida das tarefas:** Criar, ler, atualizar e deletar (CRUD) tarefas no sistema.
2.  **Orquestrar a Sugestão Inteligente:** Quando uma nova tarefa é criada ou precisa ser atribuída, este serviço se comunica com o microsserviço de IA.
3.  **Análise de Perfil:** Ele envia os requisitos da tarefa (como _skills_ necessárias) para a IA.
4.  **Receber Sugestões:** A IA analisa o perfil dos desenvolvedores cadastrados e retorna uma lista de sugestões dos mais aptos para aquela tarefa. O Task Service então disponibiliza essa sugestão para o gestor do projeto.

---

## ✨ Funcionalidades Principais

*   **Gestão Completa de Tarefas:** Endpoints para todas as operações CRUD de tarefas.
*   **Integração com IA:** Conexão direta com o serviço de IA para obter sugestões de desenvolvedores.
*   **Lógica de Atribuição:** Processa as sugestões da IA e as associa às tarefas correspondentes.
*   **Consulta de Sugestões:** Permite que a interface do usuário (frontend) consulte os desenvolvedores sugeridos para uma tarefa específica.

## 🛠️ Tecnologias Utilizadas

*   **Linguagem:** Java 17+
*   **Framework:** Spring Boot 3
*   **Gerenciador de Dependências:** Maven
*   **Arquitetura:** Microsserviços
*   **Comunicação:** API REST

---

## ☁️ Ambiente e Execução

**Este serviço foi projetado para rodar em um ambiente de nuvem e não requer instalação local para uso da plataforma final.**

Toda a infraestrutura, incluindo a comunicação entre os microsserviços, é gerenciada no ambiente de deploy. Para os desenvolvedores do projeto, a execução pode ser feita localmente através do Maven com o Spring Boot.

```bash
# Comando para executar localmente (para desenvolvedores)
./mvnw spring-boot:run```

Não há necessidade de configurações especiais (arquivos `.env`) para o usuário final, pois a plataforma será acessada via web.

##  API Endpoints (Exemplos)

> **Nota:** Estes são exemplos dos principais endpoints. Verifique o código-fonte para a lista completa e detalhes de request/response.

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `POST` | `/tasks` | Cria uma nova tarefa. |
| `GET` | `/tasks` | Retorna uma lista de todas as tarefas. |
| `GET` | `/tasks/{id}` | Busca os detalhes de uma tarefa específica. |
| `PUT` | `/tasks/{id}` | Atualiza uma tarefa existente. |
| `GET` | `/tasks/{id}/suggestions` | **[Principal]** Retorna a lista de desenvolvedores sugeridos pela IA para a tarefa. |

## 👥 Contribuidores

*   **[Moisés O. Sampaio](https://github.com/MoisesOSampaio)** - Dono do Repositório
*   _(Adicione outros membros da equipe aqui)_

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE.md) para mais detalhes.
