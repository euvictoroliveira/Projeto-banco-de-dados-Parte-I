# Projeto Sistema de Gestão Hospitalar Dra. Yuska - (Parte 1)
Repositório voltado para as implementações relacionadas à primeira parte do projeto final da disciplina de Banco de dados I, na UFPB.

## Estrutura do Projeto 

```
Projeto-banco-de-dados-Parte-I/
├── app.py                                # Arquivo principal da aplicação Flask (rota '/' e registro dos blueprints)
├── database.py                           # Configuração e conexão com o banco de dados
├── requirements.txt                      # Dependências do projeto
├── init.sql                              # Script de criação e população do banco de dados
├── README.md                             # Este arquivo
├── .gitignore
├── static/
│   └── style.css                         # Estilos compartilhados por todos os templates
├── templates/                            # Pasta com os templates HTML
│   ├── index.html                        # Página inicial com menu principal
│   ├── listar_atendimento.html           # Listagem de atendimentos (com busca por CPF)
│   ├── novo_atendimento.html             # Cadastro de novo atendimento
│   ├── listar_procedimentos.html         # Procedimentos realizados em um atendimento
│   ├── remover_procedimento.html         # Remoção de procedimento realizado
│   ├── atualizar_paciente.html           # Atualização de dados/endereço do paciente
│   ├── pacientes_sem_alto.html           # Pacientes sem procedimentos de risco ALTO
│   ├── estatisticas.html                 # Ranking de residentes, preceptores e plantões
│   └── tempo_medio_residentes.html       # Tempo médio de duração dos atendimentos por residente
├── routes/                               # Pasta com as rotas (blueprints) da aplicação
│   ├── atendimento.py                    # Blueprints de atendimentos, novo atendimento e procedimentos
│   ├── paciente.py                       # Blueprints de atualização de paciente e pacientes sem alto risco
│   ├── remover_Procedimento.py           # Blueprint de remoção de procedimento realizado
│   └── estatisticas.py                   # Blueprint das consultas analíticas/estatísticas
├── include/
│   └── verify.py                         # Validação de CPF, usada pelas rotas
└── docs/                                 # Documentação de modelagem entregue na Etapa 1
    ├── modelo entidade-relacionamento/
    │   └── Relatorio MER.pdf
    └── diagrama entidade-relacionamento/
        ├── diagrama ER.pdf
        └── Relatorio ER.pdf
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

## Rotas e Funcionalidades disponíveis

| Rota | Método | Descrição |
|---|---|---|
| `/` | GET | Menu principal |
| `/listar_atendimentos` | GET | Lista atendimentos, com busca por CPF do paciente |
| `/novo_atendimento` | GET, POST | Cadastra um novo atendimento |
| `/listar_procedimentos` | GET | Lista os procedimentos realizados em um atendimento |
| `/remover_procedimento` | GET, POST | Remove um procedimento realizado |
| `/atualizar_paciente` | GET, POST | Atualiza endereço e número de convênio do paciente |
| `/pacientes_sem_alto` | GET | Lista pacientes que nunca realizaram procedimento de risco ALTO |
| `/estatisticas` | GET | Ranking de residentes, preceptores com mais de 5 atendimentos no mês e plantões escalados por unidade |
| `/tempo_medio_residentes` | GET | Tempo médio de duração dos atendimentos, por residente |

---

> **Banco de Dados I | Projeto Final (Parte 1) | UFPB — CI**  
> Professor: Marcelo Iury

> Grupo: Vitória, Antônio Justino, João Victor, Gutemberg
