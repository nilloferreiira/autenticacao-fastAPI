from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import CONN, Pessoa, Tokens
from secrets import token_hex

app = FastAPI()

def conectaBanco():
    engine = create_engine(CONN, echo=True)
    Session = sessionmaker(bind=engine)
    return Session()

@app.post('/cadastro')
def cadastro(nome: str, user: str, senha: str):
    session = conectaBanco()

    usuario = session.query(Pessoa).filter_by(user=user, senha=senha).all()
    
    if len (usuario) == 0:
        if len(senha) < 6:
            return {"status": "senha muito fraca!"}
        
        x = Pessoa(nome=nome, user=user, senha=senha)
        session.add(x)
        session.commit()
        return {"status": "sucesso!"}

    elif len (usuario) > 0:
        return {"status": "erro"}
    
@app.post('/login')
def login(usuario: str, senha: str):
    session = conectaBanco()

    user = session.query(Pessoa).filter_by(user=usuario, senha=senha).all()

    if len(user) == 0:
        return {"status" : "erro! usuario ou senha incorretos"}
    while True:
        token = token_hex(50)
        tokenExiste = session.query(Tokens).filter_by(token=token).all()
        if len(tokenExiste) == 0:
            idExiste = session.query(Tokens).filter_by(id_pessoa=user[0].id).all()
            if len(idExiste) == 0:
                novoToken = Tokens(id_pessoa = user[0].id, token=token)
                session.add(novoToken)
            elif len(idExiste) > 0:
                idExiste[0].token = token
            
            session.commit()
            break
    return token

