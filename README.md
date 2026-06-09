# aurora

> CLI de gerenciamento de tarefas pessoais — minimalista, rápido e feito para o terminal.

## Sobre

**aurora** é uma ferramenta de linha de comando para criar, visualizar, atualizar e deletar tarefas diretamente do terminal. Construída com [Typer](https://typer.tiangolo.com/) e [Rich](https://rich.readthedocs.io/), combina uma interface simples com uma saída visualmente agradável.

## Tecnologias

- **Python** 3.11+
- **Typer** — interface de linha de comando
- **Rich** — tabelas e output colorido no terminal
- **uv** — gerenciador de pacotes e ambiente virtual
- **pytest** — testes automatizados

## Instalação

Pré-requisito: ter o [uv](https://docs.astral.sh/uv/) instalado.

```bash
git clone https://github.com/Klein-Lucas/aurora_root.git
cd aurora_root

uv venv
uv sync
```

## Uso

Todos os comandos são executados com `uv run aurora <comando>`.

### Criar uma tarefa

```bash
uv run aurora create "Estudar Python" --description "Revisar capítulo 5" --category study --end-date 2026-06-15
```

### Listar tarefas

```bash
uv run aurora show
```

```
         Tasks
┌───────┬───────────────┬────────────┐
│ Index │ Title         │ Status     │
├───────┼───────────────┼────────────┤
│ 1     │ Estudar Python│ new        │
└───────┴───────────────┴────────────┘
```

### Atualizar uma tarefa

```bash
uv run aurora update 1 --status in_progress
```

### Deletar uma tarefa

```bash
uv run aurora delete 1
```

## Campos disponíveis

| Campo         | Tipo       | Descrição                                      |
|---------------|------------|------------------------------------------------|
| `title`       | obrigatório | Nome da tarefa                                |
| `description` | opcional   | Detalhes adicionais                            |
| `start-date`  | opcional   | Data de início (`YYYY-MM-DD`)                  |
| `end-date`    | opcional   | Prazo (`YYYY-MM-DD`)                           |
| `category`    | opcional   | `work`, `study`, `health`, `hobby`             |
| `status`      | opcional   | `new`, `in_progress`, `done`, `deleted`        |

## Estrutura do projeto

```
src/aurora/
├── cli.py        # Comandos da CLI (Typer)
├── crud.py       # Operações de create, read, update, delete
├── storage.py    # Persistência em JSON
├── task.py       # Modelo de dados (dataclass + enums)
└── exceptions.py # Erros customizados
tests/
└── crud_test.py  # Testes automatizados
```

## Testes

```bash
uv run pytest
```

## Licença

MIT