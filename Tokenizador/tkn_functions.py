def decode(tkn_ids):
    return text

def encode(text):
    tokens = list(text.encode("UTF-8"))
    return tkn_ids

def map_ids(list_ids):
    top_id = max(list_ids)
    id_matrix = [[0 for _ in range(top_index)] for _ in range(top_index)] # cria uma matriz nxn com 0 para cada elemento
    top_repetition = 0

    for i in range(top_index - 1): # percorre a lista de ids sem iteragir com o ultimo id

        # cada id adjecente no texto terá um acesso direto na matriz de ids exemplo: 
        # id_text = [..., 108, 45, 67, ...] terão acessos id_matrix[108][45] e id_matrix[45][67]
        # e o valor de cada elemento será incrementado a cada repetição na lista de ids
                
        id_matrix[list_ids[i]][list_ids[i+1]] += 1

        # Se for o elemento que mais se repete na lista de ids, será salvo na variavel merge_target e depois retornado
        if id_matrix[list_ids[i]][list_ids[i+1]] > top_repetition:
            top_repetition = id_matrix[list_ids[i]][list_ids[i+1]]
            merge_target = [list_ids[i], list_ids[i+1]] 

    return merge_target


def merge(list_ids, merge_target):
    new_id = max(list_ids)+1 # o novo indice é o maior indice atual + 1
    new_list = [] 

    # explorei o uso de for porém o incremento duas vezes no i é mais facil como while, o que resulta no trecho de codigo do video
    while i < len(list_ids):
        if i < len(list_ids) - 1 and list_ids[i] == merge_target[0] and list_ids[i+1]:
            new_list.append(new_id)
            i += 2
        else:
            new_list.append(list_ids[i])
            i += 1

    return new_list

def train(list_ids, vocab_size):
    id_lista = list(list_ids)
    n_merges = vocab_size - 256
    top_id = max(list_ids)

    # a lista de adjecencia de ids serve para representar quais são os ids que vão sofrer merge com o id chave
    # isso tem objetivo de agilizar o processo de merge durante a execução da função encode
    # por exemplo, ao iterar sobre um certo id = 108, caso exista uma lista não vazia {108: [45, 56, 234]}
    # e o proximo id estiver contido na lista da chave 108 então o acesso será constante a merge_script para ter o novo id
    # id == 108 -> {108: [45, 56, 234]} -> [108, 45] == 270

    id_adj_list = {i: [] for i in range(top_index)} # cria uma lista de adjecencia vazia para cada id unico

    merge_script = {}
    for i in range(n_merges):
        merge_target = map_ids(id_lista) # encontra o par que mais se repete
        
        top_id += 1 # com a criação de mais um id pelo merge, aumenta o numero de id
        merge_script[merge_target] = top_id # o par recebe o maior id atual

        # o segundo id do par será adcionado a lista de adjecencia do primeiro id do par
        id_adj_list[merge_target[0]].append(merge_target[1]) 
        id_adj_list[top_id] = [] # um novo id é adicionado às chaves da lista de adjecencia
        
        id_lista = merge(id_lista, merge_target) # a lista é reescrita com o novo id

    return merge_script, id_adj_list

def encode(text, merge_script, id_adj_list):
    tokens = list(text.encode("UTF-8"))
    new_tokens = []
    while True:
        while i < len(tokens):
            if tokens[i+1] in id_adj_list[i]:
                new_tokens.append(merge_script)


    return tkn_ids