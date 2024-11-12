
<h1 align="center"><i>Voe Bem</i></h1>

<p align="center"> Sistema de Venda Compartilhada de Passagens Aéreas.</p>

## Introdução

A crescente demanda por viagens aéreas impulsionou uma revolução na indústria da aviação. O que antes era um setor restrito a um público seleto, hoje se tornou um dos principais meios de transporte, democratizando o acesso a diversas partes do mundo e impulsionando o desenvolvimento econômico

Com o aumento exponencial do número de passageiros, as companhias aéreas de baixo custo emergiram como protagonistas desse cenário, oferecendo tarifas mais competitivas e rotas para destinos antes considerados inacessiveis. No entanto, a complexidade da gestão de um sistema de vendas de passagens aéreas, especialmente para essas empresas com operações mais enxutas, exige soluções tecnológicas eficientes e escaláveis.

Neste contexto, o desenvolvimento de um sistema distribuído de venda de passagens aéreas surge como uma resposta às necessidades do mercado. Ao distribuir as funcionalidades do sistema em diversos servidores, é possível garantir maior disponibilidade, escalabilidade e desempenho, características essenciais para lidar com o volume de transações e a alta concorrência do setor.

Pensando nisso, foi proposto aos alunos do curso de Engenharia de Computação da Universidade Estadual de Feira de Santana (UEFS) o desenvolvimento de um sistema distribuido para venda de passagens aéreas. Este relatório visa descrever objetivamente o desenvolvimento de tal solução em que os clientes, através da internet, podem comprar passagens com várias conexões, podendo cada trecho pertencer a companhia diferentes. Para tal, a Voe Bem possui uma arquitetura descentralizada em que cada companhia mantém seu próprio servidor e banco de dados local, sendo a comunicação entre os servidores realizada através de APIs REST.

Diante dos requisitos e funcionalidades do sistema, soluções para transações distrubídas, como *Three Phase Commit (3PC)*, e de consenso foram utilizados para garantir eficiência e confiabilidade na reserva de passagens. Ao final do desenvolvimento, a aplicação foi virtualizada por meio de contêineres Docker.

## Metodologia

### Arquitetura da Solução

<div align="center">
  <figure>  
    <img src="images/arquitetura.jpg" width="600px">
    <figcaption>
      <p align="center"> 

**Figura 1** - 
    </figcaption>
  </figure>
</div>

### Protocolo de Comunicação

### Roteamento

### Concorrência Distribuída

### Confiabilidade da Solução

## Resultados e Discussões

### Desempenho
### Docker

## Conclusão