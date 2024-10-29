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
        merge_script[tuple(merge_target)] = top_id # o par como chave recebe o maior id atual como valor

        # o segundo id do par será adcionado a lista de adjecencia do primeiro id do par
        id_adj_list[merge_target[0]].append(merge_target[1]) 
        id_adj_list[top_id] = [] # um novo id é adicionado às chaves da lista de adjecencia
        
        id_lista = merge(id_lista, merge_target) # a lista é reescrita com o novo id

    # cria um mapeamente entre os ids e seu byte correspondente já utilizando o novos id do merge, será usado no decode
    vocab = {index: bytes([index]) for index in range(256)}
    for (i, j), index in merge_script.items():
        vocab[index] = vocab[i] + vocab[j]

    return merge_script, id_adj_list, vocab

def encode(text, merge_script, id_adj_list):
    tokens = list(text.encode("UTF-8")) # encodamento inicial em utf-8
    total_merges = -1 # recebe -1 para forçar a entrada no while externo
    itr_merges = 0

    # o while externo será True sempre que tiver acontecido algum merge na iteração anterior
    while itr_merges != total_merges: 
        total_merges = itr_merges # caso itr_merges não incremente, ou seja não ocorra novos merges, satisfará a condição de parada
        new_tokens = []

        while i < len(tokens): # interage com todos exceto o ultimo valor, para não fugir do escopo
            if tokens[i+1] in id_adj_list[i]: # verifica se o id atual possui um possivel merge com o proximo id usando a lista de adjecencia
                new_tokens.append(merge_script[(tokens[i], tokens[i+1])]) # utilizando a chave de par do dicionario, é adcionado o novo id
                itr_merges += 1 # ocorreu um merge, itr_merge != total_merge, logo haverá mais uma iteração no while externo
                i += 2 # pula o par
            else:
                # repete o id da lista e prossegue
                new_tokens.append(tokens[i])
                i += 1

        tokens = list(new_tokens) # como new_tokens será zerado, tokens recebe a copia do new_tokens atual
        
    return tokens

def decode(tkn_ids, vocab):
    tokens = b"".join(vocab[index] for index in tkn_ids) # concatenação dos ids
    text = tkn_ids.decode("UTF-8", errors="replace")
    return text