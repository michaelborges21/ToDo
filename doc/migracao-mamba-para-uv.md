# Migração de mamba para uv — Ubuntu 26 (zsh)

---

## 2. Instalar o uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Comentário:** o instalador baixa o binário para `~/.local/bin/uv` e já ajusta o `~/.zshrc` para incluir esse caminho no PATH.

Recarregar a shell:

```bash
source ~/.zshrc
uv --version
```

---

## 3. Autocomplete no zsh

```bash
echo 'eval "$(uv generate-shell-completion zsh)"' >> ~/.zshrc
source ~/.zshrc
```

**Comentário:** opcional, mas melhora a experiência de digitação de comandos `uv`.

---

## 4. Instalar versões de Python via uv

```bash
uv python install 3.11 3.12
uv python list
```

**Comentário:** o uv baixa builds standalone do Python — não depende do Python do sistema operacional.

---

## 5. Criar ambientes "nomeados", estilo mamba

**Comentário:** o uv não tem um registro central de ambientes por nome como `mamba create -n nome`. A forma de emular isso é centralizar os venvs em um diretório próprio:

```bash
mkdir -p ~/.venvs
uv venv ~/.venvs/ml-projeto --python 3.11
uv venv ~/.venvs/telecom --python 3.12
```

Cada `uv venv` já baixa a versão de Python pedida automaticamente, se ainda não estiver instalada.

---

## 6. Ativar / desativar

```bash
source ~/.venvs/ml-projeto/bin/activate
deactivate
```

---

## 7. Funções no `.zshrc` para ativar por nome (tipo `mamba activate <nome>`)

```bash
uva() {
  if [[ -z "$1" ]]; then
    echo "Uso: uva <nome_do_ambiente>"
    ls ~/.venvs 2>/dev/null
    return 1
  fi
  source ~/.venvs/"$1"/bin/activate
}

uvc() {
  # uvc <nome> <versao_python> — cria e ativa
  uv venv ~/.venvs/"$1" --python "${2:-3.12}"
  source ~/.venvs/"$1"/bin/activate
}
```

Uso, após `source ~/.zshrc`:

```bash
uvc ml-projeto 3.11    # cria e ativa
uva ml-projeto         # só ativa
deactivate
```

---

## 8. Instalar pacotes dentro do ambiente ativo

```bash
uv pip install numpy pandas scikit-learn
```

Ou, no espírito do uv, gerenciando via `pyproject.toml` do projeto:

```bash
cd meu-projeto
uv init
uv add numpy pandas
uv run python script.py
```

---

## 9. Erro: `No interpreter found for Python 3.12`

Comando que disparou o erro:

```bash
uv venv ~/.venvs/ToDo --python 3.12
```

```
error: No interpreter found for Python 3.12 in search path
hint: A managed Python download is available for Python 3.12, but the Python preference is set to 'only system'
```

**Comentário:** a causa era a variável `UV_PYTHON_PREFERENCE=only-system`, resquício da configuração antiga (uv + miniforge), que forçava o uv a nunca baixar Python próprio — só usar o do mamba. Isso não fazia mais sentido no novo fluxo.

### Correção pontual (sessão atual)

```bash
unset UV_PYTHON_PREFERENCE
uv venv ~/.venvs/ToDo --python 3.12
```

### Correção permanente

Localizar e remover a variável dos arquivos de configuração:

```bash
grep -rn "UV_PYTHON_PREFERENCE" ~/.zshrc ~/.zshenv ~/.profile 2>/dev/null
```

Apagar a linha encontrada e recarregar:

```bash
source ~/.zshrc
```

Alternativa: deixar explícito o comportamento desejado, em vez de simplesmente remover a variável:

```bash
export UV_PYTHON_PREFERENCE=only-managed
```

**Comentário:** isso garante que o uv nunca tente usar o Python do sistema operacional por engano — só os builds que ele mesmo gerencia, que é o comportamento "estilo mamba" pretendido.

---

## 10. Remover interpretador Python gerenciado pelo uv

Path de exemplo apresentado:

```
cpython-3.12.14-linux-x86_64-gnu   .local/share/uv/python/cpython-3.12-linux-x86_64-gnu/bin/python3.12
```

**Comentário:** existe uma distinção entre o **interpretador Python gerenciado** (em `~/.local/share/uv/python/`) e um **venv nomeado** (em `~/.venvs/`). O path colado se referia ao interpretador.

### Remover o interpretador

```bash
uv python list                # confirma o que está instalado
uv python uninstall 3.12.14   # ou "3.12" para pegar a versão ativa
```

⚠️ **Atenção:** se algum venv (ex.: `~/.venvs/ToDo`) foi criado apontando para esse interpretador, ele quebra após a remoção — o venv referencia o binário por caminho, não copia o Python inteiro.

### Remover apenas o ambiente (venv), sem mexer no interpretador

```bash
rm -rf ~/.venvs/ToDo
```

Recriação posterior:

```bash
uv venv ~/.venvs/ToDo --python 3.12
```

### Inspecionar espaço ocupado

```bash
uv python dir
du -sh ~/.local/share/uv/python/*

uv cache dir
du -sh $(uv cache dir)
```

### Limpar cache de pacotes (não afeta interpretadores nem venvs)

```bash
uv cache clean
```

---

## 11. Desinstalar e limpar o uv por completo do sistema

**Comentário:** isso remove o binário, todos os interpretadores Python gerenciados, o cache de pacotes e as configurações — deixa o sistema como se o uv nunca tivesse sido instalado. Útil se quiser recomeçar do zero ou trocar de ferramenta.

### Passo 1 — remover os venvs criados (opcional, mas eles ficam órfãos depois)

```bash
rm -rf ~/.venvs
```

### Passo 2 — remover todos os interpretadores Python gerenciados pelo uv

```bash
uv python list                       # conferir o que existe
rm -rf "$(uv python dir)"
```

### Passo 3 — limpar o cache de pacotes

```bash
rm -rf "$(uv cache dir)"
```

### Passo 4 — remover dados e configuração do uv

```bash
rm -rf ~/.local/share/uv
rm -rf ~/.config/uv
rm -rf ~/.cache/uv
```

### Passo 5 — remover o binário

```bash
rm -f ~/.local/bin/uv ~/.local/bin/uvx
```

### Passo 6 — limpar o `~/.zshrc`

Remover as linhas adicionadas pelo instalador e pelas configurações feitas nesta conversa:

```bash
grep -n "uv\b\|UV_PYTHON_PREFERENCE\|uva()\|uvc()" ~/.zshrc
```

Apagar manualmente as linhas relacionadas a:
- PATH do uv (`~/.local/bin`, se não usado por outra coisa)
- `eval "$(uv generate-shell-completion zsh)"`
- `export UV_PYTHON_PREFERENCE=...`
- As funções `uva()` e `uvc()`

Depois:

```bash
source ~/.zshrc
```

### Passo 7 — confirmar que sumiu

```bash
which uv        # não deve retornar nada
uv --version    # deve dar "command not found"
```

## 12. Conflito de Ambiente Virtual Local vs Global (uv run com warning)

**O Problema (Como estava antes):**
Ao executar `uv run main.py` (ou qualquer script `uv run`), o terminal exibia o seguinte aviso:
`warning: VIRTUAL_ENV=/home/mborges/.venvs/ToDo does not match the project environment path /mnt/LWH/learning/proj/personal_proj/ToDo/.venv and will be ignored...`

**Motivo de estar assim:** 
Os arquivos de configuração do projeto (`pyproject.toml` e `.python-version`) estavam definidos para exigir a versão do Python `>=3.13`. Quando o `uv` foi executado na pasta, ele detectou essa exigência e criou automaticamente um diretório `.venv` local com o Python 3.13 para o projeto. No entanto, o usuário já tinha o ambiente virtual `~/.venvs/ToDo` (com Python 3.12) ativado no terminal. O `uv` é programado para priorizar o `.venv` local do projeto, ignorando o ambiente ativado externamente. Isso gerava o conflito de versões e caminhos, emitindo o aviso.

**A Solução Proposta:**
A melhor forma de integrar o `uv` a um fluxo que utiliza ambientes centralizados (como `~/.venvs/ToDo`), mantendo o projeto na versão correta (Python 3.12) e sem precisar digitar a flag `--active` a cada comando, é através de um **link simbólico** (atalho).
A ideia é:
1. Ajustar o projeto para exigir o Python 3.12.
2. Apagar o `.venv` local incorreto (3.13).
3. Criar um atalho chamado `.venv` na raiz do projeto que aponte diretamente para `~/.venvs/ToDo`. 
Desta forma, quando o `uv` buscar pelo ambiente local na pasta `.venv`, ele será redirecionado de forma totalmente transparente para o ambiente centralizado correto.

**Passo a passo da execução:**

1. **Alterar a versão do Python nos arquivos do projeto:**
   - Edite o arquivo `pyproject.toml` e altere a linha `requires-python = ">=3.13"` para `requires-python = ">=3.12"`.
   - Edite o arquivo `.python-version` e altere o conteúdo de `3.13` para `3.12`.

2. **Remover o ambiente virtual conflitante do projeto:**
   ```bash
   rm -rf .venv
   ```

3. **Criar o link simbólico para o ambiente desejado:**
   Estando na raiz do projeto, execute o comando abaixo para apontar o `.venv` do projeto para o seu ambiente centralizado:
   ```bash
   ln -s ~/.venvs/ToDo .venv
   ```

Com essas alterações, execuções de comandos `uv` (como `uv run`, `uv add`, etc.) rodarão perfeitamente e diretamente dentro de `~/.venvs/ToDo` utilizando o Python 3.12, sem nenhum conflito ou aviso no terminal.
