## Curl Data Inspector

### Descrição

Curl Data Inspector é um programa Python que utiliza a ferramenta `curl` para buscar dados de uma URL e formatar a saída de acordo com a sua preferência.

### Uso

```
python app.py [opções] <url>
```

**Opções:**

* `--table`: Exibe a saída em formato de tabela.
* `--lld`: Exibe a saída em formato LLD (Low-Level Discovery).
* `<url>`: A URL da qual os dados serão obtidos.

**Exemplos:**

* Buscar dados da URL `http://example.com` e exibir em formato JSON:

```
python app.py http://example.com
```

* Buscar dados da URL `https://example.com` e exibir em formato de tabela:

```
python app.py --table https://example.com
```

* Buscar dados da URL `http://example.com` e exibir em formato LLD:

```
python app.py --lld http://example.com
```

### Formato Curl

O formato curl é definido no arquivo `curl_format.json`. Certifique-se de que este arquivo esteja presente no mesmo diretório do script `app.py` e contenha o formato desejado, conforme especificado na documentação do arquivo.

**Observação:** A documentação do formato curl provavelmente está em um arquivo separado ou dentro do próprio código `app.py`. Consulte esses recursos para obter mais detalhes sobre como especificar o formato de saída desejado.

