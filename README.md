## Documentação do código CurlDataFetcher (Markdown)

### Resumo

Este script Python define a classe `CurlDataFetcher` para buscar dados de uma URL usando o comando `curl` e formatar a saída em JSON ou tabela.

### Classes

**CurlDataFetcher:**

* **Objetivo:** Buscar dados de uma URL usando `curl` e formatar a saída.
* **Atributos:**
    * `url`: A URL da qual buscar dados.
    * `result`: Um dicionário Python contendo o resultado da busca ou um erro.
* **Métodos:**
    * `__init__(self, url)`: Construtor da classe que inicializa a URL e o dicionário de resultados.
    * `fetch_curl_data(self)`: Executa o comando `curl` com a URL e formato especificados no arquivo `curl_format.json`, armazenando a saída em `self.result`.
    * `get_result(self)`: Retorna o dicionário de resultados (`self.result`).

### Funções

* **print_help()**: Exibe a mensagem de ajuda com opções de uso e argumentos.
* **main()**: Função principal do script.
    * Valida os argumentos de entrada.
    * Processa opções de formato de saída (`--table` ou `--lld`).
    * Cria uma instância de `CurlDataFetcher` com a URL fornecida.
    * Busca os dados usando `fetch_curl_data`.
    * Exibe o resultado formatado de acordo com a opção escolhida (JSON, tabela ou LLD).

### Uso

1. Execute o script como:

```
python script_name.py [--table|--lld] <url>
```

2. Substitua `<url>` pela URL real da qual deseja buscar dados.
3. Use a opção `--table` para exibir o resultado em formato de tabela.
4. Use a opção `--lld` para exibir o resultado em formato LLD (Low-Level Discovery).
5. Se nenhuma opção de formato for fornecida, o resultado será exibido em JSON padrão.

### Dependências

O código depende das seguintes bibliotecas Python:

* `subprocess`
* `json`
* `sys`
* `tabulate` (para saída em tabela)

### Arquivo de Configuração

* `curl_format.json`: Este arquivo JSON define o formato de saída do comando `curl`. É utilizado para extrair dados específicos da saída do `curl`.

### Exemplo de `curl_format.json`

```json
{
  "time_total":{
    "regexp": "(\\d+\\.\\d{3}s)"
  }
}
```

Neste exemplo, o arquivo `curl_format.json` define uma extração usando expressão regular para capturar o tempo total da requisição (`time_total`) presente na saída do `curl`.

**Observação:** Este documento é um resumo em formato Markdown. Para uma compreensão mais detalhada, é recomendável analisar o código fonte e o conteúdo do arquivo `curl_format.json`.

