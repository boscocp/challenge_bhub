# Desafop Bhub

Olá,
Desafio BHUB. Este projeto consiste em aplicar conhecimentos de back-end ao criar uma API CRUD simples. Escoli como linguagem Python, e o framework Django. Usei como base boas práticas PEP0-8 na medida do possível e para aprimorar meus conhecimentos do framework usei o livro Two Scoops of Django 3.x (2020 - Daniel Audrey Feldroy ).

Principais tecnologias usadas:
- MongoDB
- Docker
- Docker-compose
- Django
- Swagger
- Postman
- Pytest

O projeto foi ajustado para rodar com uma versão local do mongoDB em um container. O Docker-compose realiza as etapas de subir o banco e fazer as migrações do banco caso necessário. 

Como rodar o projeto:
Precisa ter o docker instalado para poder rodar com docker-compose.
Na pasta raiz do programa execute o seguinte comando:
```
docker-compose build
docker-compose up -d
```

para verificar se o projeto está online:
```
docker-compose ps
```

Primeiramente recomendo verificar se o banco foi criado na interface mongo-express pelo link http://localhost:8081/ : 
![mongo-express](https://github.com/boscocp/challenge_bhub/blob/master/images/mongodb-ui.png)

Caso por algum motivo o banco não tenha sido criado, crie digitando bhub_project e clicando em create database na interface.

Para rodar os testes unitários neste projeto é necessário o banco de dados estar online para poder a biblioteca de mocking utilizada mocar com as respectivas configurações. O comando para executar os testes unitários:
python manage.py test --settings=config.settings.test

OBS.: O projeto usa um settings de teste para rodar os testes, e para rodar local usa o settings.local.

Para acessar a documentação da API usando a biblioteca padrão do Django:
http://localhost:1024/clientes/api_doc/


Para acessar a documentação da API usando a biblioteca padrão do Swagger:
http://localhost:1024/clientes/swagger-ui/

Payload exemplo para método POST criar cliente:
url: http://localhost:1024/clientes/
```
{
   "cliente": {
               "razao_social": "CPF",
               "telefone": "222222",
               "endereco": "Rua Api2",
               "faturamento_declarado": "1110.10"
           }
}
```

GET clientes: 
URL: http://localhost:1024/clientes/
ou com id
URL: http://localhost:1024/clientes/<uuid>/

PUT atualizar clientes: 
url: http://localhost:1024/clientes/<uuid>/
Payload:
```
{
   "cliente": {
               "razao_social": "CPF",
               "telefone": "2312312312",
               "endereco": "Rua Api22,
               "faturamento_declarado": "1555.10"
           }
}
```

DELETE deletar cliente:
URL: http://localhost:1024/clientes/<uuid>/


POST cadastrar dados bancários: 
URL: http://localhost:1024/clientes/<uuid>/dadosbancarios/
payload:
```
{
   "dadosbancarios": {
               "agencia": 3,
               "conta": 34,
               "banco": "Banco12"
           }
}
```


GET dados bancários:
URL: http://localhost:1024/clientes/<uuid>/dadosbancarios/
ou por uuid:
URL: http://localhost:1024/clientes/<uuid>/dadosbancarios/<uuid>/

Atualizar PUT: 
URL: http://localhost:1024/clientes/<uuid>/dadosbancarios/<uuid>/
payload:
```
{
   "dadosbancarios": {
               "agencia": 33,
               "conta": 344,
               "banco": "Banco13"
           }
}
```

DELETE deletar conta bancaria de um cliente:
URL: http://localhost:1024/clientes/<uuid>/dadosbancarios/<uuid>/