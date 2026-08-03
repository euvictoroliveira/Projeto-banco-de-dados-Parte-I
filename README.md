# Projeto Sistema de Gestão Hospitalar Dra. Yuska - (Parte 1)
Repositório voltado para as implementações relacionadas à primeira parte do projeto final da disciplina de Banco de dados I, na UFPB.

## Estrutura do Projeto 

```
Projeto-banco-de-dados-Parte-I/
├── app.py                                # Arquivo principal da aplicação Flask (registro dos blueprints)
├── database.py                           # Instância do SQLAlchemy usada em toda a aplicação
├── models.py                             # Modelos SQLAlchemy (mapeamento das tabelas do banco)
├── concorrencia.py                       # Simulação de concorrência (lock) ao escalar um residente
├── requirements.txt                      # Dependências do projeto
├── README.md                             # Este arquivo
├── .gitignore
├── static/
│   └── style.css                         # Estilos compartilhados por todos os templates
├── templates/                            # Pasta com os templates HTML
│   ├── base.html                         # Layout base, herdado pelos demais templates
│   ├── index.html                        # Dashboard inicial (contadores e ranking)
│   ├── atendimento.html                  # Registrar, listar e remover atendimentos/procedimentos
│   ├── paciente.html                     # Atualizar paciente e listas relacionadas a pacientes
│   ├── escala.html                       # Listagem e reajuste de escalas
│   ├── estatisticas.html                 # Ranking, plantões e percentuais por residente/preceptor
│   ├── tempo_medio_residentes.html       # Tempo médio de duração dos atendimentos por residente
│   ├── preceptores_flamengo.html         # Preceptores de pacientes flamenguistas
│   ├── tempo_medio_espera.html           # Não usado por nenhuma rota (dado já exibido dentro de estatisticas.html)
│   ├── views.html                        # Menu das views do banco
│   ├── vw_pacientes_internados.html      # View: pacientes internados no momento
│   ├── vw_residentes_sem_supervisor.html # View: residentes sem preceptor com titulação de Doutor
│   ├── vw_estatisticas_mensais.html      # View: estatísticas de atendimentos por mês/unidade
│   ├── triggers.html                     # Menu das triggers do banco
│   ├── auditoria.html                    # Histórico de INSERT/UPDATE/DELETE em atendimento
│   └── media_procedimentos.html          # Tempo médio por procedimento (atualizado por trigger)
├── routes/                               # Pasta com as rotas (blueprints) da aplicação
│   ├── home.py                           # Blueprint do dashboard inicial ('/')
│   ├── atendimento.py                    # Blueprint de atendimentos (registrar, listar, remover procedimento)
│   ├── paciente.py                       # Blueprint de paciente (atualizar dados, listas)
│   ├── escala.py                         # Blueprint de escala (listar e reajustar)
│   ├── estatisticas.py                   # Blueprint das consultas analíticas/estatísticas
│   ├── views.py                          # Blueprint das views do banco
│   └── triggers.py                       # Blueprint das triggers do banco (auditoria e médias)
├── include/
│   └── verify.py                         # Validação de CPF e CRM, usada pelas rotas
├── sql/                                  # Scripts de criação e população do banco (executados em ordem)
│   ├── init.sql                          # Orquestra a execução dos scripts abaixo, em ordem
│   ├── 1_tables.sql                      # Criação das tabelas e relacionamentos
│   ├── 2_testdata.sql                    # População do banco com dados de teste
│   ├── 3_functions_procedures.sql        # Functions e procedures (escala, atendimento, tempo de espera)
│   ├── 4_views.sql                       # Views de consulta (internados, sem supervisor, estatísticas)
│   └── 5_triggers.sql                    # Triggers (auditoria, sobreposição de escala, média de procedimento)
└── docs/                                 # Documentação de modelagem entregue na Etapa 1
    ├── diagrama entidade-relacionamento/
    │   ├── Diagrama ER.pdf
    │   └── RELATÓRIO ER.pdf
    └── diagrama relacional/
        ├── Diagrama relacional.pdf
        └── Relatorio Normalização.pdf
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
psql -U postgres -d projeto_hospital < ./sql/init.sql
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
| `/` | GET | Dashboard inicial: contadores gerais e ranking de residentes |
| `/atendimento` | GET, POST | Registrar atendimento, listar atendimentos (busca por CPF) e remover procedimento realizado |
| `/paciente` | GET, POST | Atualizar dados/convênio do paciente, listar pacientes sem procedimento de risco ALTO e última consulta de cada paciente |
| `/escala` | GET, POST | Listar escalas e reajustar dia/turno de um residente |
| `/estatisticas` | GET | Ranking de residentes, preceptores com mais de 5 atendimentos no mês, plantões por unidade e percentual de procedimentos de alto risco |
| `/tempo_medio_residentes` | GET | Tempo médio de duração dos atendimentos, por residente |
| `/preceptores_flamengo` | GET | Lista os preceptores que atenderam pacientes flamenguistas |
| `/views` | GET | Menu com as views disponíveis do banco |
| `/vw_pacientes_internados` | GET | View: pacientes atualmente internados |
| `/vw_residentes_sem_supervisor` | GET | View: residentes escalados sem um preceptor com titulação de Doutor |
| `/vw_estatisticas_mensais` | GET | View: total de atendimentos, duração média e procedimentos mais comuns por mês/unidade |
| `/triggers` | GET | Menu com as triggers disponíveis do banco |
| `/triggers/auditoria` | GET | Histórico de INSERT/UPDATE/DELETE registrado na tabela `atendimento` |
| `/triggers/media_procedimentos` | GET | Tempo médio de cada procedimento, recalculado automaticamente por trigger |
| `/simular-concorrencia` | GET | Simula duas threads tentando escalar o mesmo residente ao mesmo tempo |

---

> **Banco de Dados I | Projeto Final | UFPB — CI**
>
> Professor: Marcelo Iury
>
> Grupo: Vitória, Antônio Justino, João Victor, Gutemberg
