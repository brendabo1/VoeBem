
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

O modelo P2P, no qual o sistema se baseia, permite que cada nó funcione como cliente e servidor ao mesmo tempo, facilitando o compartilhamento de recursos e serviços (Almeida e Costa, 2007). Essa arquitetura  promove a autonomia de cada nó, distribui o armazenamento de forma descentralizada e elimina a dependência de um único ponto, resultando em uma alta disponibilidade de dados e serviços (Santos e Amaral, 2006).

Cada companhia do sistema corresponde a um servidor com seu conjunto de dados independentes, dentre eles as rotas ofertadas pela empresa e os usuários e pedidos na plataforma. 
A partir das interações com o usuário, o dispositivo atuando como cliente processa as entradas e gera requisições de dados ou serviços ao servidor. Dessa maneira, cada solicitação será processada no lado do servidor de uma companhia que, com acesso aos dados de voos, assentos, clientes e pedidos, enviará a resposta a ser exibida no lado do cliente. Alguns serviços, como a obtenção de rotas disponíveis, demandam dados de voos distribuídos no servidor de cada companhia. Assim, requisições são disparadas para os demais nós do sistema, processadas e formatadas para o retorno ao cliente.   

Para facilitar a comunicação entre os nós, o sistema utiliza APIs REST, uma interface padronizada que permite que os nós P2P troquem informações e solicitem recursos de forma eficiente e escalável. A arquitetura REST, amplamente adotada para sistemas distribuídos, permite que os nós se comuniquem de maneira independente da plataforma e da linguagem de programação, utilizando protocolos HTTP para envio de requisições. Os componentes e conexões desta arquitetura são explicitados na Figura 1.


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

| Método   |  Endpoint  | Parâmetros |  Response | Descrição |
---------- |-----------|-------------|---------- |-----------|
|  POST    |   /login     |    | <details> <summary>200</summary> status: sucesso</details>      |
|  POST    |   /buscar_rotas     | origem, destino    |      |
|  GET     |   /grafo_rotas     | None    |      |
|  GET     |   /supergrafo     | None    |      |
|  POST    |   /comprar_passagem      |  user_id, trechos  |      |
|  GET    |   /pedidos/<user_id>      | user_id    |      |


### Roteamento

### Concorrência Distribuída

### Confiabilidade da Solução

## Resultados e Discussões

### Desempenho
### Docker

## Conclusão

## Referências

Almeida, R. & Costa, F. (2007). Arquitetura Peer-to-Peer para Computação Distribuída: Desafios e Oportunidades. Anais do Simpósio Brasileiro de Redes de Computadores, 35(1), 142-155.