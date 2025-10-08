# High-Speed DataFrames with Polars

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Polars](https://img.shields.io/badge/DataFrames-Polars-FF4500?style=for-the-badge&logo=polars&logoColor=white)
![Mermaid](https://img.shields.io/badge/Diagrams-Mermaid-orange?style=for-the-badge&logo=mermaid&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)
![GitHub last commit](https://img.shields.io/github/last-commit/galafis/polars-high-speed-dataframes?style=for-the-badge)
![GitHub repo size](https://img.shields.io/github/repo-size/galafis/polars-high-speed-dataframes?style=for-the-badge)
![GitHub stars](https://img.shields.io/github/stars/galafis/polars-high-speed-dataframes?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/galafis/polars-high-speed-dataframes?style=for-the-badge)

---

## 🇧🇷 DataFrames de Alta Velocidade com Polars

Este repositório explora e demonstra o uso da biblioteca **Polars para processamento de dados de alta performance**, focando em operações com DataFrames. Polars é uma alternativa robusta e extremamente rápida ao Pandas, construída em Rust, que aproveita o paralelismo e a eficiência de memória para lidar com grandes volumes de dados de forma otimizada. É ideal para **análise exploratória de dados, engenharia de features e pipelines de ETL** que exigem velocidade e escalabilidade.

### 🎯 Objetivo

O principal objetivo deste projeto é **fornecer exemplos práticos, benchmarks e tutoriais detalhados** para profissionais de dados que desejam migrar ou integrar Polars em seus fluxos de trabalho. Serão abordados desde os conceitos fundamentais de DataFrames em Polars até técnicas avançadas de otimização, integração com outras bibliotecas e comparação de performance com outras ferramentas, com foco em **operacões de I/O eficientes, transformações complexas e avaliação lazy**.

### ✨ Destaques

- **I/O Otimizado**: Demonstrações de leitura e escrita eficientes de arquivos CSV e Parquet, aproveitando a performance do Polars para lidar com grandes volumes de dados.
- **Transformações Complexas e Expressões Avançadas**: Exemplos de como aplicar transformações de dados sofisticadas, incluindo agregação, filtragem e criação de novas colunas usando a poderosa sintaxe de expressões do Polars.
- **Avaliação Lazy (Lazy Evaluation)**: Exploração do paradigma de avaliação lazy do Polars, que permite a construção de planos de consulta otimizados, resultando em melhor performance e menor consumo de memória.
- **Operações de Join e Correlação**: Demonstrações de como realizar operações de join entre DataFrames e calcular correlações entre colunas, essenciais para análise de dados e engenharia de features.
- **Performance Excepcional**: Polars supera outras bibliotecas em velocidade e uso de memória para operações comuns de DataFrame, graças à sua implementação em Rust e paralelismo nativo.
- **API Intuitiva**: Exemplos que mostram a simplicidade e expressividade da API do Polars, facilitando a transição para usuários de Pandas.
- **Código Profissional**: Exemplos de código bem estruturados, seguindo as melhores práticas da indústria, com foco em modularidade, reusabilidade e manutenibilidade.
- **Documentação Completa**: Cada exemplo é acompanhado de documentação detalhada, benchmarks e casos de uso práticos para facilitar a compreensão e a aplicação.
- **Módulo de Exemplo Avançado**: Um novo módulo (`advanced_example.py`) foi adicionado para demonstrar funcionalidades mais complexas e cenários de uso real, incluindo geração de dados simulados, processamento de vendas e análise de clientes.

### 🚀 Benefícios do Polars em Ação

O Polars oferece uma série de vantagens que o tornam uma escolha superior para processamento de dados de alta performance. Este projeto ilustra como esses benefícios são explorados:

1.  **Velocidade Incomparável:** Construído em Rust, o Polars aproveita a segurança de memória e a performance nativa para executar operações de DataFrame em velocidades impressionantes, superando o Pandas em muitos cenários, especialmente em I/O e transformações complexas.

2.  **Processamento Paralelo:** Utiliza todos os núcleos da CPU disponíveis por padrão, permitindo o processamento paralelo de dados sem a necessidade de configuração manual complexa, o que é evidente em operações de agregação e transformação.

3.  **Avaliação Lazy (Lazy Evaluation):** Permite a construção de planos de consulta otimizados, onde as operações são executadas apenas quando os resultados são realmente necessários, economizando recursos e tempo, como demonstrado na função `complex_lazy_evaluation`.

4.  **Eficiência de Memória:** Projetado para ser eficiente no uso de memória, o Polars pode lidar com datasets maiores do que o Pandas em máquinas com recursos limitados, tornando-o ideal para grandes volumes de dados.

5.  **API Expressiva:** Oferece uma API intuitiva e poderosa, que combina a facilidade de uso do Pandas com a performance de ferramentas de processamento distribuído, facilitando a escrita de código limpo e eficiente.

6.  **Integração com Arrow:** Baseado no Apache Arrow, o Polars garante interoperabilidade eficiente com outras ferramentas do ecossistema de dados, minimizando a cópia de dados e otimizando o fluxo de trabalho.

---

## 🇬🇧 High-Speed DataFrames with Polars

This repository explores and demonstrates the use of the **Polars library for high-performance data processing**, focusing on DataFrame operations. Polars is a robust and extremely fast alternative to Pandas, built in Rust, which leverages parallelism and memory efficiency to handle large volumes of data optimally. It is ideal for **exploratory data analysis, feature engineering, and ETL pipelines** that require speed and scalability.

### 🎯 Objective

The main objective of this project is to **provide practical examples, benchmarks, and detailed tutorials** for data professionals who wish to migrate to or integrate Polars into their workflows. It will cover everything from the fundamental concepts of DataFrames in Polars to advanced optimization techniques, integration with other libraries, and performance comparison with other tools, with a focus on **efficient I/O operations, complex transformations, and lazy evaluation**.

### ✨ Highlights

- **Optimized I/O**: Demonstrations of efficient reading and writing of CSV and Parquet files, leveraging Polars' performance to handle large data volumes.
- **Complex Transformations and Advanced Expressions**: Examples of how to apply sophisticated data transformations, including aggregation, filtering, and creating new columns using Polars' powerful expression syntax.
- **Lazy Evaluation**: Exploration of Polars' lazy evaluation paradigm, which allows for the construction of optimized query plans, resulting in better performance and lower memory consumption.
- **Join and Correlation Operations**: Demonstrations of how to perform join operations between DataFrames and calculate correlations between columns, essential for data analysis and feature engineering.
- **Exceptional Performance**: Polars outperforms other libraries in speed and memory usage for common DataFrame operations, thanks to its Rust implementation and native parallelism.
- **Intuitive API**: Examples showcasing the simplicity and expressiveness of the Polars API, making it easy for Pandas users to transition.
- **Professional Code**: Well-structured code examples, following industry best practices, with a focus on modularity, reusability, and maintainability.
- **Complete Documentation**: Each example is accompanied by detailed documentation, benchmarks, and practical use cases to facilitate understanding and application.
- **Advanced Example Module**: A new module (`advanced_example.py`) has been added to demonstrate more complex functionalities and real-world use cases, including simulated data generation, sales processing, and customer analysis.

### 📊 Visualization

![Polars Data Processing Flow](diagrams/polars_data_processing_flow.png)

*Diagrama ilustrativo do fluxo de processamento de dados com Polars, destacando as etapas de ingestão, transformação e saída.*


---

## 🛠️ Tecnologias Utilizadas / Technologies Used

| Categoria         | Tecnologia      | Descrição                                                                 |
| :---------------- | :-------------- | :------------------------------------------------------------------------ |
| **Linguagem**     | Python          | Linguagem principal para desenvolvimento e interface com Polars.          |
| **DataFrames**    | Polars          | Biblioteca de DataFrames de alta performance, construída em Rust.         |
| **Serialização**  | CSV, Parquet    | Formatos de arquivo suportados para leitura e escrita otimizadas.         |
| **Testes**        | `pytest`        | Framework de testes para validação de funcionalidades e performance.      |
| **Diagramação**   | Mermaid         | Para criação de diagramas de arquitetura e fluxo de dados no README.      |

---

## 📁 Repository Structure

```
polars-high-speed-dataframes/
├── src/
│   ├── core/                      # Módulos principais com a lógica central do Polars
│   │   └── polars_demo.py
│   ├── examples/                  # Módulos de exemplo avançados e casos de uso
│   │   └── advanced_example.py
│   └── __init__.py                # Para permitir importações de módulos internos
├── data/                          # Dados de exemplo (CSV, Parquet) para benchmarks e testes
├── images/                        # Imagens e gráficos para o README e documentação
├── tests/                         # Testes unitários e de integração para as implementações
├── docs/                          # Documentação adicional, tutoriais e guias de performance
├── scripts/                       # Scripts utilitários para automação e execução de benchmarks
├── requirements.txt               # Dependências Python
└── README.md                      # Este arquivo
```

---

## 🚀 Getting Started

Para começar, clone o repositório e explore os diretórios `src/` e `docs/` para exemplos detalhados e instruções de uso. Certifique-se de ter as dependências necessárias instaladas.

### Pré-requisitos

- Python 3.9+
- `pip` (gerenciador de pacotes Python)

### Instalação

```bash
git clone https://github.com/GabrielDemetriosLafis/polars-high-speed-dataframes.git
cd polars-high-speed-dataframes

# Instalar dependências Python
pip install -r requirements.txt
```

### Exemplo de Uso Avançado (Python)

O exemplo abaixo demonstra a inicialização da classe `AdvancedPolarsProcessor`, a criação de DataFrames com dados simulados, operações de agrupamento e agregação, adição de novas colunas, operações encadeadas, avaliação lazy complexa, joins com outros DataFrames e cálculo de correlação. Este código ilustra a flexibilidade e o poder do Polars para manipulação de dados de alta performance.

```python
import polars as pl
from src.examples.advanced_example import AdvancedPolarsProcessor
import os

if __name__ == "__main__":
    print("=" * 60)
    print("Polars High-Speed DataFrames Advanced Demo")
    print("=" * 60)

    processor = AdvancedPolarsProcessor()

    # Gerar e carregar dados de exemplo
    sales_df, customer_df = processor.create_sample_data()

    # Processar os dados de vendas
    sales_summary, top_customers, daily_sales = processor.process_sales_data(sales_df, customer_df)

    print("\n==================================================")
    print("Demonstração Avançada Concluída.")
    print("==================================================")
```

---

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues, enviar pull requests ou sugerir melhorias. Por favor, siga as diretrizes de contribuição.

---

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

**Autor:** Gabriel Demetrios Lafis  \n**Ano:** 2025

