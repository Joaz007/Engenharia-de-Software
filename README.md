# Trabalho 1 e 2 — Engenharia de Requisitos e Modelagem/Desenvolvimento

**Universidade Tecnológica Federal do Paraná (UTFPR)**
**Apucarana - Paraná · 2025**

---

## Equipe

* **Millena S. de Oliveira** 
* **Maria E. Mafra**
* **João A. S. Martins**

---

## Resumo do projeto

**Lu Mafra Personal Trainer** é uma academia voltada ao público feminino cujo gerenciamento atual é manual (planilhas, cadernos e livro-caixa). O projeto propõe um sistema para **automatizar e centralizar** o gerenciamento financeiro e operacional: mensalidades, contas a pagar, cadastro de alunas e horários, substituindo o uso parcial do TecnoFit.

---

## Objetivo

**Descrição do problema:** A empresa Lu Mafra Personal Trainer é uma academia voltada para o público feminino. Nela, o gerenciamento é feito de maneira manual, isto é, a análise de despesas, controle de mensalidades, cadastro de alunas e gerenciamento de horários são todos controlados pelas funcionárias sem o auxílio de softwares; exceto pela geração de comprovantes, realizada pelo aplicativo TecnoFit. 
 
**Justificativa da aplicação proposta:** Com a implementação de um software, é possível automatizar as tarefas (o trabalho se torna mais rápido) e aumentar o nível de confiabilidade (as chances de erro humano são menores).

Assim, o objetivo é desenvolver um protótipo funcional e a documentação de requisitos para um sistema interno que permita à proprietária:
* Controlar mensalidades (recebimentos e cobranças);
* Gerenciar contas a pagar/receber;
* Fazer cadastro digital de alunas;
* Administrar horários de aulas e evitar conflitos;
* Receber notificações apenas para a administradora sobre pagamentos atrasados (após 3 dias).
---

## Levantamento de Requisitos

Método: entrevista com a proprietária (Lu Mafra).

Principais pontos:
* Processos financeiros manuais com alta chance de erro.
* Necessidade de centralizar geração de comprovantes (substituir o aplicativo TecnoFit).
* Preferência por muitas funcionalidades (prioridade funcional sobre visual).
* Notificações apenas para administradora após 3 dias de atraso.

---------------------------------------------
## PARTE 2 DO TRABALHO
---------------------------------------------

## Objetivos de Gerenciamento de Qualidade

Nessa etapa, o objetivo é maximizar as melhorias do código passando por diversas versões até chegar a uma versão final, de modo que precise de poucas modificações e seja de fácil entendimento o código como um todo. Dentre os principais pontos perceptíveis para um gerenciamento de qualidade foram:

* Correção de Valores: Na criação do CPF ele verifica se é válido, caso a pessoa tenha digitado errado ou passado informação falsa.
* Manutenibilidade: Código permite alterações e restaurações ao longo do processo.
* Testabilidade: Funções com responsabilidade de garantir funcionamento do código como a validar_cpf.
---

## Decisões arquiteturais e suas respectivas justificativas:

Para o desenvolvimento do projeto, foi escolhida a arquitetura MVC (Modelo-Visão-Controlador). Nela, o sistema é dividido em três componentes - modelo, responsável por gerenciar os dados e como são operados; visão, que gerencia como os dados serão expostos ao usuário; controlador, define como é feita a interação. 
Dada as características principais do projeto, tal descrição se adequa às necessidades exprimidas pela cliente. O modelo representa o sistema desenvolvido, acoplado ao banco de dados: juntos, recebem as informações de cadastro e as gerenciam. A visão é referente à interface: como o cliente deseja um programa intuitivo e de fácil acesso, a solução lógica é promover a criação de uma interface de maneira que o ambiente se torne amigável ao usuário. Por fim, o controlador refere-se aos comandos ditados pelo usuário a fim que o programa realize os comandos, que serão feitos juntamente com a interface. 
---

## Decisões sobre padrões de projeto e suas respectivas justificativas

Para o desenvolvimento do projeto, foram utilizados três padrões diferentes - singleton, strategy e builder. 

* Singleton: Faz com que haja apenas uma instância da classe em todo o programa. Como o banco de dados contendo as informações referentes às alunas deve ser único e as operações de cadastro e consulta compartilham o mesmo acesso, este padrão se aplica às necessidades. Dessa forma, múltiplas conexões ao banco de dados são evitadas, além de centralizar o gerenciamento de dados. 
* Strategy: Aqui, o padrão tem como objetivo definir diferentes estratégias que podem ser trocadas estrategicamente em tempo de execução, de forma que não há necessidade de modificar a parte principal do código. No código, o padrão foi aplicado para realizar o cálculo da mensalidade: como as alunas podem escolher a quantidade de aulas por semana, o valor não é fixo e, dessa forma, o programa aplica a melhor estratégia de acordo com cada caso. 
* Builder: Este é utilizado para a construção de objetos complexos passo a passo, garantindo todas as validações e inicializações necessárias. Assim, foi tomada a decisão de aplicá-lo para a criação da classe Aluna, permitindo que seja reduzido o número de construtores necessários (dada a grande quantidade de parâmetros) e que haja encadeamento de chamadas. 
---

## Diagrama de arquitetura e Diagramas dos padrões de projeto de acordo com o código desenvolvido

*OS DIAGRAMAS FORAM COLOCADOS NA PASTA "Trabalho 2" PARA EVITAR POLUIÇÃO VISUAL DO README

## Código desenvolvido

Para a aplicação em si do projeto, foi utilizada a linguagem Python e a bibliteca de interface TKinter, muito utilizada por usuários da linguagem e muito similiar com a estrutura de formatação de HTML e CSS

Para que seja possível a compilação, é necessário ter baixado as bibliotecas
* tk
* customtkinter
* pillow

Muitas vezes já vem baixada na própria biblioteca do Python3 mas caso não esteja, é possível baixar com o comando pip install {biblioteca}, por exemplo "pip install tk".
É recomendada também a atualização com o comando -m pip install --upgrade pip na pasta aonde estiver o executável python.exe
Caso não seja viável a instalação ou caso não tenha obtido sucesso na instalação, terá um PDF com um link de um vídeo mostrando o resultado do código inicial

O projeto em si falta muitos detalhes a serem analisados, mas as principais funcionalidades foram apresentadas e estão funcionais.