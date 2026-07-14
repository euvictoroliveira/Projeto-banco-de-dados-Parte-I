# Projeto Sistema de Gestão Hospitalar Dra. Yuska - (Parte 1)
Repositório voltado para as implementações relacionadas à primeira parte do projeto final da disciplina de Banco de dados I, na UFPB.

## Estrutura do Projeto 

```
Projeto-banco-de-dados-Parte-I/
├── app.py                # Arquivo principal da aplicação Flask
├── database.py           # Configuração e conexão com o banco de dados
├── requirements.txt      # Dependências do projeto
├── init.sql            # Script de criação e população do banco de dados
├── README.md             # Este arquivo
├── templates/            # Pasta com os templates HTML
│   ├── index.html        # Página inicial com menu principal
│   └── atendimento.html  # Página de listagem de atendimentos
└── routes/               # Pasta com as rotas da aplicação
    └── atendimento.py    # Blueprint para rotas de atendimento
```

## Instruções para instalação e execução dos scripts

### 1. CLone o repositório
```bash
git clone [URL_DO_REPOSITORIO]
cd Projeto-banco-de-dados-Parte-I
```

### 2. Crie e ative um ambiente virtual no python
```bash
python -m venv venv

# para ativar no windows
venv\Scripts\activate
# para ativar no linux/mac
source venv/bin/activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configuração do Banco de Dados PostgreSQL
4.1 Acesse o PostgreSQL e crie a database 'projeto_hospital'
```bash
createdb -U postgres projeto_hospital
```

4.2 Execute o script SQL para criar as tabelas e popular com dados
```bash
psql -U postgres -d projeto_hospital < init.sql
```
Em "Senha para o usuário postgres:" apenas confirme, não precisa inserir senha

### 5. Execute a aplicação
```bash
python app.py
```

### 6. Para acessar no navegador, copie o endereço IP exibido no terminal e cole no seu navegador.

---

> **Banco de Dados I | Projeto Final (Parte 1) | UFPB — CI**  
> Professor: Marcelo Iury
> Grupo: Vitória, Antônio Justino, João Victor, Gutemberg
