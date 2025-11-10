# 🏡 Orçamento de Aluguel R.M. - Calculadora Simples
Este projeto é uma aplicação desktop desenvolvida em Python que utiliza Programação Orientada a Objetos (POO) e a biblioteca Tkinter para gerar orçamentos de aluguel de forma automatizada, aplicando regras de negócio específicas para diferentes tipos de imóveis.

Ele atende aos requisitos do Desafio R.M. Imobiliária, demonstrando a integração de lógica de back-end (cálculo) e front-end (interface gráfica).

✨ Funcionalidades Principais
Cálculo por Tipo de Imóvel: Suporta orçamentos para Apartamento, Casa e Estúdio, cada um com suas regras de cálculo específicas.

Aplicação de Regras de Negócio: Aplica adicionais e descontos com base em parâmetros como número de quartos, vagas de garagem, e a presença de crianças (desconto de 5% em Apartamentos).

Parcelamento de Contrato: Inclui um valor fixo de R$ 2000,00 de contrato parcelado automaticamente nas 5 primeiras mensalidades.

Interface Gráfica (GUI): Utiliza Tkinter para uma interação amigável, permitindo que o usuário configure os parâmetros sem usar o terminal.

Relatório Detalhado: Gera uma visualização do orçamento mensal completo para os 12 meses, incluindo a discriminação das parcelas de aluguel e contrato.

💻 Estrutura do Código e Pensamento Algorítmico
O projeto é estruturado utilizando o paradigma Programação Orientada a Objetos (POO) em Python para garantir modularidade e reusabilidade.


1. Algoritmo de Geração de Parcelas
A classe OrcamentoGenerator implementa o pensamento algorítmico ao traduzir a regra de negócio do parcelamento em uma estrutura lógica iterativa.

O método _gerar_parcelas() itera sobre 12 meses (for mes in range(1, 13)), adicionando a parcela do contrato (R$ 400,00) apenas se o mês for menor ou igual a 5.


🚀 Como Executar o Projeto
Pré-requisitos:

Certifique-se de ter o Python 3 instalado em sua máquina.

O projeto utiliza apenas a biblioteca padrão tkinter, que geralmente já está incluída na instalação do Python.

Execução:

Salve o código-fonte (Projeto de orçamento (1).py) em um arquivo chamado, por exemplo, calculadora_aluguel.py.

Abra o terminal ou prompt de comando na pasta onde o arquivo foi salvo.

Execute o comando:

Bash

python calculadora_aluguel.py
Utilização:

Selecione o Tipo de Locação (Apartamento, Casa ou Estúdio).

As Opções Dinâmicas (Quartos, Garagem, Crianças, Vagas) serão atualizadas conforme o tipo selecionado.

Clique em Calcular Orçamento.

O resumo da primeira parcela será exibido.

Clique em Ver Orçamento Detalhado (12 Meses) para ver a tabela completa de pagamentos.
