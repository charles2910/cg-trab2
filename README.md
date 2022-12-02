# Trabalho 2 - Computação Gráfica - SCC0650

## Alunos
- Carlos H. L. Melara  9805380
- Maíra Canal         11819403

## Descrição 
Esse repositório contém o código-fonte do segundo trabalho da
disciplina.

## Instalação
Para usar esse projeto, recomenda-se a utilização de um ambiente
virtual python (python venv). Para isso, basta criar um novo `venv`
após baixar o código:

```
bash python -m venv venv
```

Para o Debian:

```
bash python3 -m venv venv
```

Esse comando criará uma pasta `venv` na raiz do projeto contendo o ambiente
virtual. Para entrar no ambiente, execute:

```
bash source venv/bin/activate
```

A partir deste ambiente, instale as dependências com o `pip`:

```
bash pip install -r requirements.txt
```

A partir desse momento, seu computador estará pronto para desenvolver ou
executar a aplicação.

### Resolução de problemas
Eu tive um problema com a execução do opengl e mesa. Não estava sendo
carregado os drivers da minha placa de vídeo e o seguinte erro era
mostrado:

```bash
libGL error: MESA-LOADER: failed to open iris (search paths /usr/lib/x86_64-linux-gnu/dri:\$${ORIGIN}/dri:/usr/lib/dri)
```

A solução foi adicionar um link simbólico de `/usr/lib/dri` para
`/usr/lib/x86_64-linux-gnu/dri`, mas é possível tentar usar a seguinte 
solução antes de criar o link:

```bash
export LIBGL_DRIVERS_PATH=/usr/lib/x86_64-linux-gnu/dri
```

## Uso
Para executar a aplicação:

```
bash python src/main.py
```

### Comandos
- É possível mover o barco com as setas do teclado;
- É possível mover horizontalmente o Sol com as teclas `a` e `d`;
- É possível aumentar o Sol com a teclas `w` e diminui-lo com `s`;
- É possível rotacionar as pás do moinho com as teclas `q` e `e`;

## Licença
O código-fonte escrito por nós será licenciado com a licença MIT.
