# API Desenvolvida como resolução para o Teste Técnico <i>igma</i>.

## Autor: Marcelo Eduardo Rodrigues da Silva Filho

### Tecnologias utilizadas: 

    A API foi desenvolvida utilizando a linguagem Python na versão 3.10 e o framework Flask na versão 2.2.2.

    O banco de dados utilizado foi o SQlite.

    Todo o frontend foi feito utilizando apenas HTML e CSS.

    E utilizei também o Docker/Docker Compose, para facilitar a posterior execução do código.

    A escolha dessas tecnologias se baseou principalmente na agilidade e simplicidade das ferramentas.


### Como subir e utilizar a aplicação:

#### Utilizando Docker (recomendado):

1. Vá até a raiz do projeto (onde fica o arquivo compose.yml).
   
2. Use `docker compose-up` para rodar os containers
    - O container da aplicação irá rodar primeiro, para acessá-la basta ir no endereço `localhost:8080` ou no endereço do servidor, caso tenha sido subida em um, o importante é a porta `8080`.
    - Em segundo irá rodar o container de testes, que basicamente fará o trabalho de executar o script em `src/tests.py`.

#### Utilizando virtual environment:
1. Caso por algum motivo seja inviável o uso do Docker.
2. Crie um virtual environment do python 3.10 na sua máquina (pode utilizar utilitários como `venv` ou `pyenv`).
3. Ative seu ambiente virtual e instale as depêndencias que estão no arquivo requirements.txt com: `pip install -r requirements.txt`
4. Execute a aplicação rodando o script `src/app.py` com algo parecido com `python app.py`.
5. Caso queira também executar os testes, vá em outra janela do seu terminal, ative o seu virtual environment novamente e execute o script em `src/tests.py` com `python tests.py`.

A partir desse ponto a aplicação estará rodando, abaixo alguns pontos sobre ela:

1. Acessando a rota `/` você verá uma lista de links para acessar todas as rotas, mas caso queira acessá-las manualmente, elas estão descritas abaixo:
    - `/add` - Endpoint para adicionar um novo cliente
      - Será exibido um form para que você o preencha e adicione o novo cliente.
    - `/search` - Endpoint para procurar um cliente através do CPF.
      - Será exibido um campo de pesquisa, onde você deve entrar o CPF do cliente.
    - `/show` - Endpoint que exibe todos os dados de todos os   clientes já cadastrados.
      - Será exibida uma tabela com os dados de 10 clientes, e logo abaixo um menu de paginação para ver os próximos.
2. A API pode ser utilizada tanto via UI, quanto pelo padrão REST enviando requisições com body no formato JSON:
    - `/add` - POST com json no formato: `{'customer_cpf': '11111111111', 'customer_name': 'Jorge', 'customer_birthdate' '1990-1'}`
    - `/search` - POST json no formato: `{'customer_cpf': '11111111111'}` - Receberá uma resposta com um JSON no formato: `{'customer_cpf': '11111111111', 'customer_name': 'Jorge', 'customer_birthdate' '1990-1'}`
    - `/show` - GET request com params LIMIT (Quantidade de Clientes) e OFFSET (a partir de qual registro) irá te retornar um JSON com a quantidade indicada de Clientes (ex: `http://0.0.0.0:8080/show?limit=10&offset=5`). Caso os parâmetros não sejam passados, a versão gráfica será dada como resposta.


### Documentação:

Abaixo a explicação dos arquivos de script da aplicação e suas principais funções

### app.py

Arquivo que contém as views (funções que vão tratar das requests para cada endpoint).
Dentro desse arquivo, temos views para os quatro endpoints já citados:
   - `/` - para esse endpoint, a view correspondente apenas aceita `GET` requests, e tem o papel de renderizar o template da home page (`homepage.html`) e devolve no corpo da resposta.
   - `/add` - já a view desse endpoint aceita tanto `POST` quanto `GET` requests:
     - `GET` - apenas renderiza o template da página de cadastro de cliente (`add_customer.html`) e devolve na resposta.
     - `POST` - nesse caso, quando um formulário é submetido através da página de cadastro, a view faz o papel de: 
       - criar o objeto `Customer` com os dados do novo cliente;
       - chamar a verificação para ver se o CPF passado é válido;
       - verificar se já existe algum cadastro com esse CPF;
       - caso passe em todas as verificações, é criado um novo registro no banco de dados utilizando os dados do novo objeto `Customer`.
       - Em caso de falha, é exibida uma página de `FAIL` (`add_customer_fail.html`) para o usuário.
       - Em caso de sucesso, é exibida uma página de `SUCCESS` (`add_customer_success.html`) para o usuário.
   - `/search` - a view que cuida desse endpoint também aceita ambos os métodos `GET` e `POST`:
     - `GET` - apenas renderiza o template da página de busca de cliente via CPF (`search_customer.html`) e devolve na resposta.
     - `POST` - nesse caso, quando o formulário de busca é submetido, a view tem o papel de:
       - chamar o static method da classe `Customer` que realiza a busca de Clientes utilizando o CPF
       - renderizar o template `search_customer.html` porém agora com os dados do cliente encontrado (caso exista). 
   - `/show` - a view nesse caso, trabalha apenas com `GET` requests, fazendo a recuperação de todos os Clientes, dividindo a quantidade de registros em páginas de 10 clientes e dependendo do GET param `page` exibe uma dessas páginas.

### customer.py

Esse arquivo contém a lógica relacionada à entidade `Cliente` chamada no código de `Costumer`.

Aqui vai toda a lógica do que seria o `Model` da nossa aplicação.

A principal estrutura do arquivo é a classe `Costumer` que contém:

  - Atributos:
    - `name` : string que representa o nome do cliente;
    - `birthdate`: date que representa a data de nascimento do cliente;
    - cpf: string que representa o CPF do cliente.
  - Métodos:
    - `__init__(name, cpf, birthdate)`: método construtor, cuida da criação do objeto dessa classe
    - `__str__()`: uma definição do que seria o objeto em formato de string
    - `is_cpf_valid()`: o método mais importante, verifica se o CPF do objeto é válido de acordo com as regras em https://www.macoratti.net/alg_cpf.htm#:~:text=O.
      - A ideia principal para reproduzir o algoritmo no link acima, foi, além de transformar o CPF de string para inteiro e vice-versa, inverter o CPF para realizar as multiplicações necessárias, isso facilitou o desenvolvimento da solução. Então o algoritmo faz:
        - Pega os 9 primeiros dígitos do CPF e inverte a ordem deles ("123456789" viraria "987654321")
        - Cria uma lista, onde cada posição é um caracter dessa string.
        - Converte todas as posições da lista para inteiro. Teriamos: `CPF_INV = [9, 8, 7, 6, 5, 4, 3, 2, 1]`
        - Percorre `i` no intervalo [2, 11] e multiplica cada `i` com o dígito em sua respectiva posição no CPF invertido (`i*CPF_INV[i-2]`) e vai somando numa variável acumulativa. Ex: soma = 2*9 + 3*8 + 4*7 ... + 10*1
        - Pega a soma acumulada e tira o resto da divisão dela por 11 (resto = soma%11).
          - Se o resto for menor que 2, digito = 0.
          - Se o resto for maior ou igual a 2, digito = 11 - resto.
        - Adiciona o dígito no início do CPF invertido. Ex: supondo digito = 3, teriamos CPF_INV = `[3, 9, 8, 7, 6, 5, 4, 3, 2, 1]`
        - Percorrer um `i` no intervalo [2, 12], multiplicando cada `i` com o dígito em sua respectiva posição no CPF invertido (`i*CPF_INV[i-2]`) e soma numa variável acumulativa.
        - Pega a soma acumulada e tira o resto da divisão dela por 11 e tira o segundo dígito:
          - Se o resto for menor que 2, digito = 0.
          - Se o resto for maior ou igual a 2, digito = 11 - resto.
        - Tendo o segundo dígito adiciona novamente no inicio do CPF invertido. Ex: digito2 = 5, teriamos CPF_INV = `[5, 3, 9, 8, 7, 6, 5, 4, 3, 2, 1]`
        - Agora basta inverter novamente essa lista, ficando com: CPF_INV = `[1, 2, 3, 4, 5, 6, 7, 8, 9, 3, 5]`
        - Converte tudo em string e concatena, tendo como resultado: CPF_INV = `"12345678935"`
        - Por fim, verifica se o CPF calculado é igual ao dado como entrada:
          - Se for, CPF de entrada é válido.
          - Se não, inválido.
  

  - Métodos estáticos: métodos que não dependem do objeto e nem da classe
    - `create_database_table()` - responsável por executar a query de criação da tabela `CUSTOMER` no banco de dados.
    - `add_customer(customer_object)` - responsável por executar a query de `INSERT` de um novo cliente no banco de dados, utilizando os dados contidos em um objeto `Customer`.
    - `get_customers(limit, offset)` - realiza a query `SELECT * FROM CUSTOMERS`, recuperando todos os clientes existentes no banco. Caso sejam passados os parâmetros `limit` e `offset`, será feita uma query com paginação.
    - `get_customer_by_cpf(cpf)` - realiza uma query `SELECT` com a condição dos usuários resgatados terem o campo CPF igual ao passado como parâmetro, devolve apenas 1.
    - `normalize_cpf(cpf)` - tira a máscara do CPF, removendo pontos e hífens da string.

### populate_db.py

Um script simples pra popular o banco de dados com alguns registros.

### tests.py 

Aqui estão os testes escritos para cada um dos endpoints.