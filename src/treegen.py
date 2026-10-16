"""TREES GEN FOR README"""
# Versão 1.0 alpha
# Autor: Yann Escobar
# Data: 16/10/2026
# Todos os direitos reservados
import os
# Importa o pacote de ferramentas para trabalhar com SO
from pathlib import Path
# Traz uma função específica do 'pathlib' que é a 'Path'

config = {
    'modo_salva': 'app',  # 'app', 'padrão', 'custom'
    'pasta_custom': None,
    'formato_selecionado': 'app',  # 'app', 'txt', 'md'
    'ultima_arvore': None
}


    #Função principal do programa
    # 'caminho' variável que recebe o caminho dãã
    #  'prefixo' espaços e conectores de cada elemento tipo aquele "| "
    #  'eh_ultimo' variável que define se um item é último ou não (booleano) 
def gerar_arvore_diretorios(caminho, prefixo="", eh_ultimo=True):
    """
    Gera uma representação em árvore de diretórios e arquivos.
    """

    """TESTE DE PERMIÇÃO"""
    try:
        items = sorted(os.listdir(caminho)) 
        # Lista os arquivos em um diretório com 'os.listdir(parâmetroONDEESTÁODIRETÓRIO)'
        # 'sorted' oredena alfabéticamente

    except PermissionError: # Erro de permição faça..
        return print("Erro de permição")

    """FILTRO DE ARQUIVOS SEM NOME"""
    # Filtra itens ocultos (opcional - remova se quiser incluir)
    items = [item for item in items if not item.startswith('.')]
    # 'if not item.startswith('.')' condição
    # 'item.startswith('.')' verifica se o item começa com um '.'
    # 'not' nega inverte o resultado exemplo:
    # exemplo.txt False
    # .git true
    # Depois disso cria uma lista(array) de items que passaram no filtro
    
    if not items:
        return "Pasta vazia"
    
    resultado = ""
    # Cria uma var para armazenar o  texto em árvore

    """LOOP PRINCIPAL"""

    for i, item in enumerate(items):
    # 'enumerate' enumera itens em uma lista
    # 'i' é um índice que vai percorrer a cada cilco de execução do loop
    # 'item' vai ser o arquivo

        caminho_completo = os.path.join(caminho, item)
        # 'os.path.join(parametro0, parametro1)' junta em uma variável
        # utilizando dois parâmetros

        eh_ultimo_item = (i == len(items) - 1)
        # 'len' significa length e retorna os itens na lista
        # o '-1' porque len retorna sem incluir o zero
        # 'i == len(items)' compara o valor do ciclo de execução com a posição do item
        # retorna true or false observe:
        # Iteração 2: i=1
        #i == len(items) - 1  # 1 == 2? → False
        # Iteração 3: i=2
        #i == len(items) - 1  # 2 == 2? → True ← É o último
        
        """CONECTOR VISUAL"""

        conector = "└── " if eh_ultimo_item else "├── "
        # Lógica se é último adicona o "└── " se não adiciona o  "├── "

        resultado += prefixo + conector + item + "\n"
        # Resultado é resultado + prefixo("| ") + conector("├──") + item (arquivo.exemplo)
        # output-> Resultado: "│   ├── arquivo.txt\n"
        
        # Se for diretório, recursivamente processa
        # Essa parte é uma recursão
        # Recursão = uma função chamando a si mesma
        if os.path.isdir(caminho_completo):
        # o 'isdir' retorna true se o nome do caminho se refere a um diretório existente
        # o parâmetro 'caminho_completo'
        # se for false então é um arquivo

            extensao = "    " if eh_ultimo_item else "│   "
            resultado += gerar_arvore_diretorios(
                caminho_completo, # '/projeto/pastafilha' (novapasta)
                prefixo + extensao, # aumenta o espaçamento "| "
                eh_ultimo_item # booleano
            ) # <- viu só ela chama a si mesma!
            # a cada ciclo de execução, se encontrar um diretório ela vai loopar denovo
    
    return resultado

def salvar_arquivo(arvore_texto, caminho_saida, formato):
    """
    Salva a árvore em arquivo.
    
    Args:
        arvore_texto: String com o conteúdo da árvore
        caminho_saida: Diretório onde salvar
        formato: 'txt' ou 'md'
    
    Returns:
        (bool, str): (sucesso, mensagem)
    """
    if formato == 'app':
        return True, "Árvore vai ficar plantada aqui até você fechar."

    extensao = '.md' if formato == 'md' else '.txt'
    nome_arquivo = f"PROJETO_ESTRUTURA{extensao}"
    caminho_completo = os.path.join(caminho_saida, nome_arquivo)

    try:
            # Abre o arquivo em modo escrita, com codificação UTF-8
        with open(caminho_completo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(arvore_texto)
            
        return True, f"✅ Arquivo salvo em:\n{caminho_completo}"
        
    except IOError as ie:
        return False, f"Erro de I/O, ao salvar arquivo: {str(ie)}"
    except Exception as e:
        return False, f"Erro desconhecido: {str(e)}"    

# Uso
if __name__ == "__main__":
    pasta = input("Digite o caminho da pasta: ") or "."
    
    # Obtém o nome da pasta
    nome_pasta = os.path.basename(os.path.abspath(pasta))
    
    # Gera a árvore
    arvore = nome_pasta + "/\n" + gerar_arvore_diretorios(pasta)
    
    print(arvore)
    
    # Salva em arquivo
    salvar = input("\nSalvar em arquivo? (s/n): ").lower() == 's'
    if salvar:
        with open("PROJETO_ESTRUTURA.md", "w", encoding="utf-8") as f:
            f.write(arvore)
        print("✓ Salvo em PROJETO_ESTRUTURA.md")