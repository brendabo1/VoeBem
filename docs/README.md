
<h1 align="center"><i>Voe Bem</i></h1>

<p align="center"> Sistema de Venda Compartilhada de Passagens Aéreas.</p>

## Introdução

A crescente demanda por viagens aéreas impulsionou uma revolução na indústria da aviação. O que antes era um setor restrito a um público seleto, hoje se tornou um dos principais meios de transporte, democratizando o acesso a diversas partes do mundo e impulsionando o desenvolvimento econômico

Com o aumento exponencial do número de passageiros, as companhias aéreas de baixo custo emergiram como protagonistas desse cenário, oferecendo tarifas mais competitivas e rotas para destinos antes considerados inacessiveis. No entanto, a complexidade da gestão de um sistema de vendas de passagens aéreas, especialmente para essas empresas com operações mais enxutas, exige soluções tecnológicas eficientes e escaláveis.

Neste contexto, o desenvolvimento de um sistema distribuído de venda de passagens aéreas surge como uma resposta às necessidades do mercado. Ao distribuir as funcionalidades do sistema em diversos servidores, é possível garantir maior disponibilidade, escalabilidade e desempenho, características essenciais para lidar com o volume de transações e a alta concorrência do setor.

Pensando nisso, foi proposto aos alunos do curso de Engenharia de Computação da Universidade Estadual de Feira de Santana (UEFS) o desenvolvimento de um sistema distribuido para venda de passagens aéreas. Este relatório visa descrever objetivamente o desenvolvimento de tal solução em que os clientes, através da internet, podem comprar passagens com várias conexões, podendo cada trecho pertencer a companhia diferentes. Para tal, a Voe Bem possui uma arquitetura descentralizada em que cada companhia mantém seu próprio servidor e banco de dados local, sendo a comunicação entre os servidores realizada através de APIs REST. Diante dos requisitos e funcionalidades do sistema, soluções para transações distrubídas, como *Three Phase Commit (3PC)*, e de consenso foram utilizados para garantir eficiência e confiabilidade na reserva de passagens. Ao final do desenvolvimento, a aplicação foi virtualizada por meio de contêineres Docker.

## Metodologia

Para solucionar o problema proposto, algoritmos de transação distribuída, consenso e a arquitetura da API REST foram analisados e adotados. A linguagem de programação Pyhton foi escolhida para implementação e os protocolos utilizados serão detalhadas nesta seção.

Além disso, o sistema é composto por rotas de tráfego aéreo nas principais cidades da Bahia e as siglas dos aeroportos utilizadas na busca de rotas é apresentada na lista abaixo. 

Legenda AEROPORTOS
- (SSA) Salvador - Aeroporto Deputado Luís Eduardo Magalhães
- (IOS) Ilhéus - Aeroporto de Ilhéus - Jorge Amado
- (BPS) Porto Seguro - Aeroporto de Porto Seguro
- (LEC) Lençóis - Aeroporto Horácio de Mattos
- (PAV) Paulo Afonso- Aeroporto de Paulo Afonso
- (BRA) Barreiras - Aeroporto de Barreiras
- (FEC) Feira de Santana - Aeroporto João Durval Carneiro
- (VAL) Valença - Aeroporto de Valença
- (GNM) Guanambi - Aeroporto de Guanambi
- (TXF) Teixeira de Freitas - Aeroporto de Teixeira de Freitas
- (VDC) Vitória da Conquista - Aeroporto Glauber de Andrade Rocha

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

**Figura 1** - Componentes e conexões na arquitetura do sistema
    </figcaption>
  </figure>
</div>

### Protocolo de Comunicação

A comunicação via API REST possui endpoints para o métodos remotos do sistema. As especificações da API são expostas na Tabela 1.

| Método   |  Endpoint  | Parâmetros |  Response | Descrição |
---------- |-----------|-------------|---------- |-----------|
|  POST    |   /login     |   user_id: str, senha: str | <details> <summary>200</summary> status: login bem-sucedido</details> <details> <summary>400</summary> status: ID ou senha não preenchidos</details> <details><summary>401</summary> status: ID ou senha incorretos</details>  | endpoint para autenticação do usuário e acesso ao sistema
|  GET     |   /grafo_rotas     | None    | <details> <summary>200</summary> status: sucesso </details> | Endpoint utilizado para acessar o grafo de rotas de uma companhia 
|  POST    |   /buscar_rotas     | origem: str, destino: str    | <details> <summary>200</summary> status: sucesso</details> <details> <summary>400</summary> status: Origem ou destino não preenchidos</details><details> <summary>500</summary> status: Erro interno na busca</details>  | endpoint para buscar todas as rotas possíveis da origem até o destino dados.
|  GET     |   /supergrafo     | None    | <details> <summary>200</summary> status: sucesso </details> <details> <summary>500</summary> status: erro interno ao construir o supergrafo </details> | endpoint para construção e acesso ao grafo de rotas de todas as companhias criado a partir das rotas locais em cada servidor
|  POST    |   /prepare      |  reserva_id: str, trechos: dict  |<details><summary>200</summary> status: sucesso</details> <details> <summary>409</summary> status: erro de conflito no status de um recurso</details>| Endpoint que verifica a disponibilidade dos trechos para iniciar uma transação distribuida 
|  POST    |   /pre-commit      |  reserva_id: str  |  <details> <summary>200</summary> status: sucesso</details> <details> <summary>409</summary> status: erro de conflito no status de um recurso</details>      | Endpoint para confirmação preliminar do servidor 
|  POST    |   /do_commit      |  reserva_id: str, user_id: str  |   <details> <summary>200</summary> status: sucesso</details> <details> <summary>409</summary> status: erro de conflito no status de um recurso</details>  | Endpoint utilizado pelo coordenador para autorizar a execução da transação
|  POST    |   /abort      |  reserva_id: str | <details> <summary>200</summary> status: sucesso</details> | Endpoint usado em qualquer ponto da transação distribuída para desfazer alterações temporárias 
|  POST    |   /comprar_passagem      |  user_id: str, trechos: dict  |  <details> <summary>200</summary> status: sucesso</details> <details> <summary>500</summary> status: erro interno na transação</details> <summary>500</summary> status: </details>    | Endpoint para comprar uma passagem usando o protocolo de transação distribuída Three Phase Commit
|  POST    |   /sincronizar_reserva     |  user_id: str, reserva: dict  |  <details> <summary>200</summary> status: Reserva sincronizada com sucesso</details> <details> <summary>400</summary> status: Dados de sincronização incompletos</details>  | Endpoint para sincronizar a reserva realizada em cada servidor 
|  GET    |   /pedidos/<user_id>      | user_id: str    |  <details> <summary>200</summary> status: sucesso</details> <details> <summary>404</summary> status: Usuário não encontrado</details>     | Endpoint para obter os pedidos de um usuário específico

Tabela 1: Endpoints da API


### Roteamento

Para possibilitar a busca e venda de rotas que combinam trechos de várias companhias aéreas, foi adotado um algoritmo inspirado no protocolo de roteamento de estado de enlace, também conhecido como  *Link State Routing*. Este protocolo é amplamente utilizado em redes para oferecer uma visão global da topologia, o que permite uma determinação eficiente e precisa das rotas (Tanenbaum & Wetherall, 2011). 

Assim sendo, cada nó ou servidor do sistema Voe Bem armazena temporariamente uma cópia completa da topologia da rede com o supergrafo de todos os voos das companhias. A cada operação de busca em um servidor, os grafos locais de cada nó são consultados e agrupados em uma única estrutura contendo todos os caminhos possíveis no sistema. Dessa maneira, ao buscar uma rota de uma origem A até um destino X, trajetos como A-B-C-X, A-B-D-E-X, A-X, A-C-X e todas as possíbilidades dentre as companhias da plataforma são entregues ao usuário.  

Portanto, através da execução do algoritmo, o sistema mantém uma visão unificada e atualizada das rotas disponíveis, assegurando que os usuários consultem sempre as informações mais recentes.

### Concorrência Distribuída

### Confiabilidade da Solução

## Resultados e Discussões

### Desempenho
### Docker

## Conclusão

## Referências

Almeida, R. & Costa, F. (2007). Arquitetura Peer-to-Peer para Computação Distribuída: Desafios e Oportunidades. Anais do Simpósio Brasileiro de Redes de Computadores, 35(1), 142-155.

Tanenbaum, A. S., & Van Steen, M. (2016). Distributed Systems: Principles and Paradigms. Prentice Hall.

Tanenbaum, A. S., & Wetherall, D. (2011). Computer Networks. Pearson.