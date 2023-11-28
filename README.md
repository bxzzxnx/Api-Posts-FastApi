API de criação e votação de **postagens** utilizando autenticação de usuários utilizando **JWT**
### Criando venv

```shell
python -m venv .venv
```

Ativando 
```shell
.venv\Scripts\Activate
```

Instalando as dependências
```shell
pip install -r requirements.txt
```


#### Documentação

Rodando a Api
```shell
uvicorn app.main:app --reload
```

Iniciará o servidor na porta padrão **8000**
A documentação ficará disponível em **http://127.0.0.1:8000/docs**

Para acessar as rotas de **post** o usuário precisa fazer login e estar autenticado


Rodando os testes
```shell
pytest
```

### Env

Crie um arquivo **.env** 
Por padrão a porta do postgres vai ser 5432
```env
DATABASE_URL=postgres://username:password@hostname:port/database
SECRET_KEY =
ALGORITHM = 
ACCESS_TOKEN_EXPIRE_MINUTES =
```


#### Docker

Arrume o **docker-compose.yml** conforme seu url de database e usuário e senha do **postgres**
Em vez de apontar o o **hostname** para localhost aponte para o serviço de db **postgres**

```yaml
version: "3"
services:
  api:
    build: .
    ports:
      - 8000:8000
    environment:
      - DATABASE_URL=postgresql://username:password@postgres:port/database
    depends_on:
      - postgres

  postgres:
    image: postgres
    environment:
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=database
    volumes:
      - postgres_db:/var/lib/postgresql/data
volumes:
  postgres_db:
```

