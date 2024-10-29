def train(text, vocab_size):
    merges = vocab_size - 256 # 
    return

def decode(tkn_ids):
    return text

def encode(text):
    tokens = list(text.encode("UTF-8"))
    return tkn_ids

def map_ids(list_ids):
    top_index = max(list_ids)
    id_matrix = [[0 for _ in range(top_index)] for _ in range(top_index)] # cria uma matriz nxn com 0 para cada elemento
    id_adj_list = {i: [] for i in range(top_index)} # cria uma lista de adjecencia vazia para cada id unico
    top_repetition = 0


    for i in range(top_index - 1): # percorre a lista de ids sem iteragir com o ultimo id

        # cada id adjecente no texto terá um acesso direto na matriz de ids exemplo: 
        # id_text = [..., 108, 45, 67, ...] terão acessos id_matrix[108][45] e id_matrix[45][67]
        # e o valor de cada elemento será incrementado a cada repetição na lista de ids
        
        #Se é a primeira vez que é incrementado, então a lista de adjecencia associado ao id recebe uma nova entrada
        # exemplo: [..., 108, 45, ...] será representado dessa forma: {108 : [45]} 

        if id_matrix[list_ids[i]][list_ids[i+1]] == 0:
            id_adj_list[list_ids[i]].append(list_ids[i+1])
                
        id_matrix[list_ids[i]][list_ids[i+1]] += 1

        # Se for o elemento que mais se repete na lista de ids, será salvo na variavel merge_target e depois retornado
        if id_matrix[list_ids[i]][list_ids[i+1]] > top_repetition:
            top_repetition = id_matrix[list_ids[i]][list_ids[i+1]]
            merge_target = [list_ids[i], list_ids[i+1]] 

    return id_matrix, id_adj_list, merge_target


def merge(list_ids, merge_target):
    new_idx = max(list_ids)+1
    
    return