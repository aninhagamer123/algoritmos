import os 

# sem aspas é variavel, com aspas é string, a procura do arquivo é sem aspas
arquivo_usuarios = "usuarios.txt"
arquivo_videos = "videos.txt"
arquivo_curtidas = "curtidas.txt"
arquivo_favoritos = "favoritos.txt"

#ler linhas = le todas as linhas de um arquivo e retorna uma lista
#w = write; r = read; f = arquivo aberto para leitura read; a = append, adicionar
#strip = remove espaços em branco
def ler_linhas(caminho):
    if not os.path.exists(caminho):
        open (caminho, "w").close()
    with open(caminho, "r", encoding="utf-8") as f:
        return [linha.strip() for linha in f if linha.strip()]

#salvar linhas novas no arquivo, quando houver movimentação do user
def salvar_linhas(caminho, linhas):
    with open (caminho, "w", encoding="utf-8") as f:
        for linha in linhas:
            f.write(linha + "\n")

#cadastrar o user
#split = divide uma string em uma lista usando um separador | ou pode usar , etc tal
#partes é o parametro para separar string com o split
def cadastrar_usuario():
    nome = input("Digite seu nome: ")
    senha = input("Digite sua senha: ")
    
    if not nome:
        print("Nome não pode ser vazio!")
        return
    for linha in ler_linhas(arquivo_usuarios):
        partes = linha.split("|")
        if partes[0] == nome:
            print("Já existe")
            return
    with open (arquivo_usuarios, "a", encoding="utf-8") as f:
        f.write(f"{nome}|{senha}\n")
    print("Usuário cadastrado com sucesso!")

#login
# [0] e [1] são os indices
def login_usuario():
    nome = input("Digite seu nome: ")
    senha = input("Digite sua senha: ")

    for linha in ler_linhas(arquivo_usuarios):
        partes = linha.split("|")
        if partes[0] == nome and partes[1] == senha:
            print("Bem Vindo")
            return nome
            
    print("Usuário ou senha incorretos")
    return None

#videos no banco
#if not é se nao existir
def popular_videos():
    if not ler_linhas(arquivo_videos):
        with open (arquivo_videos, "a", encoding="utf-8") as f:
            f.write("1|Pretendente Surpresa|Romance|2024|Uma jovem se inscreve em um programa de TV para encontrar o amor verdadeiro.\n")
            f.write("2|Vincenzo|Suspense|2021|Um advogado mafioso italiano-coreano retorna à Coreia e enfrenta uma corporação corrupta.\n")
            f.write("3|Startup|Drama|2020|Jovens empreendedores lutam para construir suas empresas no mundo das startups sul-coreanas.\n")
            f.write("4|O Jogo da Imitação|Guerra|2015|Um matemático brilhante lidera uma equipe secreta para decifrar os códigos nazistas na Segunda Guerra.\n")
            f.write("5|Holo Meu Amor|Romance|2020|Uma jovem desenvolvedora se apaixona por um holograma de inteligência artificial.\n")

#buscar videos
def buscar_videos():
    nome = input("Digite o nome do vídeo: ")
    resultados = [] #lista chamada resultados

    for linha in ler_linhas(arquivo_videos):
        partes = linha.split("|")
        if nome.lower() in partes[1].lower():
            resultados.append(linha) # append para adicionar linha na lista de resultados

    if not resultados:
        print("Não encontrado")
        return
        
    for linha in resultados:
        partes = linha.split("|")
        print("Título: " + partes[1])
        print("Gênero: " + partes[2])
        print("Ano: " + partes[3])
        print("Sinopse: " + partes[4])
        print(f"Curtidas: {contar_curtidas(partes[0])}") # mostra o total de curtidas do video
        print()  # linha em branco para separar

#curtir os videos
#lower = transforma TUDO em letra MINUSCULA, e não importa o jeito que digitar vc encontrará a informação mais próxima
def curtir_videos(usuario):
    nome = input("Digite o nome do vídeo a ser curtido ou que deseja descurtir: ")
    resultados = [] #buscar video para curtir

    for linha in ler_linhas(arquivo_videos):
        partes = linha.split("|")
        if nome.lower() in partes[1].lower():
            resultados.append(linha)

    if not resultados:
        print("Nenhum vídeo encontrado") 
        return #fechamento do buscar video, é o codigo acima

    #i = numero e video = conteudo
    #por exemplo, dps que buscou o video com a palavra AMOR, vai aparecer mais de um ID video com a palavra AMOR, o user precisa escolher.    
    for i, video in enumerate(resultados, 1):
        partes = video.split("|")
        print(f"[{i}] {partes[1]}")

    escolha = input("Número do vídeo: ")
    id_video = resultados[int(escolha) - 1].split("|")[0]

    #string ENTRADA vai mostra como esta o nome do USER  e O ID do video que ele curtiu
    entrada = f"{usuario}|{id_video}"
    linhas = ler_linhas(arquivo_curtidas) #linhas é uma LISTA

    if entrada in linhas: #se o usuario ja curtiu, remove e salva de novo, ou seja, descurtiu
        linhas.remove(entrada)
        salvar_linhas(arquivo_curtidas, linhas)
        print("Vídeo descurtido")

    else:
        with open (arquivo_curtidas, "a", encoding="utf-8") as f:
             f.write(entrada + "\n")
        print("Vídeo curtido")

#mostrar a quantidade de curtidas que o video tem
def contar_curtidas(id_video):
    contador = 0

    for linha in ler_linhas(arquivo_curtidas):
        partes = linha.split("|")
        if partes[1] == id_video:
            contador += 1

    return contador

#user vai ver os videos que ja curtiu
#v = arquivo video
# 0 é o indice do ID e o 1 é o indice do TITULO = para cada video, verifica se o ID dele bate com o ID curtido pelo usuário
def ver_curtidas(usuario):
    for linha in ler_linhas(arquivo_curtidas):
        partes = linha.split("|")
        if partes[0] == usuario:
           for v in ler_linhas(arquivo_videos):
                if v.split("|")[0] == partes[1]:
                   print(f"Título: {v.split('|')[1]}")

#Favoritos
#Criar lista
def criar_lista(usuario):
    nome_lista = (input("Digite o nome da lista que deseja criar: "))

    for linha in ler_linhas(arquivo_favoritos):
        partes = linha.split("|")
        if partes[0] == usuario and partes[1] == nome_lista:
            print("Já existe")
            return
            
    with open (arquivo_favoritos, "a", encoding="utf-8") as f:
        f.write(f"{usuario}|{nome_lista}|\n")
    print("Lista Criada!")

#ver listas do user
def ver_listas(usuario):

    for linha in ler_linhas(arquivo_favoritos):
        partes = linha.split("|")
        if partes[0] == usuario:
            print(f"Lista: {partes[1]}")
            for id_video in partes[2].split(","):
                for v in ler_linhas(arquivo_videos):
                    if v.split("|")[0] == id_video:
                        print(f" - {v.split('|')[1]}")

#adicionar video
def adicionar_video(usuario):
    ver_listas(usuario)
    nome_lista = (input("Digite o nome da lista que deseja adicionar o vídeo: "))
    resultados = [] #lista chamada resultados

    for linha_favorito in ler_linhas(arquivo_favoritos): # linha_favorito para nao confundir com o for de videos
        partes = linha_favorito.split("|") #procura a lista no arquivo favoritos
        if partes[0] == usuario and partes[1] == nome_lista: #verifica se linha pertence ao user e se o nome bate

            #buscar o video
            nome = input("Digite o nome do vídeo: ")

            for linha in ler_linhas(arquivo_videos):
                partes_video = linha.split("|") #procura todos os videos e logo abaixo add na lista os que batem com o termo digitado
                if nome.lower() in partes_video[1].lower():
                   resultados.append(linha) # append para adicionar linha na lista de resultados

            if not resultados:
               print("Não encontrado")
               return
        
            for i, video in enumerate(resultados, 1):
               partes_video = video.split("|")
               print(f"[{i}] {partes_video[1]}") #mostra os videos encontrados com o numero de ordem na frente, NAO É INDICE
        
            #adicionando o video
            escolha = (input("Digite o número do vídeo que deseja adicionar: "))
            id_video = resultados[int(escolha) - 1].split("|")[0] #pega o id do video escolhido

            ids = partes[2].split(",") if partes[2] else [] #pega os ids salvos na lista
            if id_video in ids: #se o id ja estiver na lista, o sistema avisa e para.
               print("Vídeo já está na lista")
               return
        
            ids.append(id_video) #add um novo id
            partes[2] = ",".join(ids) #saida "1,2,3"

            todas = ler_linhas(arquivo_favoritos) #le todas as linhas
            todas[todas.index(linha_favorito)] = "|".join(partes) #substitui a linha antiga pela atual
            salvar_linhas(arquivo_favoritos, todas) #salva
            print("Vídeo adicionado com sucesso!")
            return
    
    print("Lista não encontrada")

#remover video
def remover_video(usuario):
    ver_listas(usuario)
    nome_lista = (input("Digite o nome da lista que deseja remover o vídeo: "))

    for linhas in ler_linhas(arquivo_favoritos):
        partes = linhas.split("|")
        if partes[0] == usuario and partes[1] == nome_lista: # pega os IDs dos videos que estao na lista
            ids = partes[2].split(",") if partes[2] else [] # se estiver vazio, cria lista vazia

            if not ids:
                print("Lista vazia!") 
                return
        
            for i, id_video in enumerate(ids, 1): #mostra o NOME dos vídeos com NUMERO DA FRENTE para o user escolher qual remover
                for v in ler_linhas(arquivo_videos):
                    if v.split("|")[0] == id_video:
                        print(f"[{i}] {v.split('|')[1]}") #mostra o titulo do video pelo ID

            escolha = (input("Digite o número do vídeo que deseja remover: "))

            ids.pop(int(escolha) - 1) #o POP REMOVE o item da lista naquela posicao
            partes[2] = ",".join(ids) #junta os IDs restantes de volta com ","
            todas = ler_linhas(arquivo_favoritos) #substitui a linha antiga pela atualizada e salva no arquivo.
            todas[todas.index(linhas)] = "|".join(partes)
            salvar_linhas(arquivo_favoritos, todas)
            print("Vídeo removido!")
            return

    print("Lista não encontrada!")

#editar lista - renomear uma lista
def editar_lista(usuario):
    ver_listas(usuario)
    nome_antigo = (input("Digite o nome da lista que gostaria de renomear: "))
    nome_novo = (input("Digite o novo nome da lista: "))

    todas = ler_linhas(arquivo_favoritos)

    for i, linha in enumerate(todas): #mostra o NOME dos vídeos com NUMERO DA FRENTE para o user escolher qual renomear
        partes = linha.split("|")
        if partes[0] == usuario and partes[1] == nome_antigo:
           partes[1] = nome_novo
           todas[i] = "|".join(partes)
           salvar_linhas(arquivo_favoritos, todas)
           print("Nome da lista Renomeada com sucesso!")
           return
        
    print("Lista não encontrada!")

#excluir lista
def excluir_lista(usuario):
    ver_listas(usuario)
    nome = (input("Digite o nome da lista que gostaria de excluir: "))

    todas = ler_linhas(arquivo_favoritos)

    for linha in todas:
        partes = linha.split("|")
        if partes[0] == usuario and partes[1] == nome:
            todas.remove(linha)
            salvar_linhas(arquivo_favoritos, todas)
            print("Lista excluída com sucesso!")
            return
    print("Lista não encontrada!")

#menu_favoritos
#menu principal do usuario com servidor para aba "Favoritos"
def menu_favoritos(usuario):
    while True: #cria loop, onde o MENU fica aparecendo ATÉ o user escolher 0 VOLTAR
        print("\n--- FAVORITOS ---") #mostra as opcoes para o user
        print("1. Criar lista")
        print("2. Ver listas")
        print("3. Adicionar vídeo")
        print("4. Remover vídeo")
        print("5. Renomear lista")
        print("6. Excluir lista")
        print("0. Voltar")
        opcao = input("Escolha: ") #o user digita a opcao que ele quer

        if opcao == "1": #o numero da opcao 
            criar_lista(usuario)
        elif opcao == "2":
            ver_listas(usuario)
        elif opcao == "3":
            adicionar_video(usuario)
        elif opcao == "4":
            remover_video(usuario)
        elif opcao == "5":
            editar_lista(usuario)
        elif opcao == "6":
            excluir_lista(usuario)
        elif opcao == "0":
            break #quebra o loop e volta para o menu anterior
        else:
            print("Opção inválida!")

#menu do usuario logado para o menu principal
def menu_usuario(usuario):
    while True: #loop do menu fica aparecendo ate o user escolher 0 para sair do MENU
        print(f"\n FEItv | Seja bem vindo (a), {usuario}! O que deseja fazer?")
        print("1. Buscar vídeo")
        print("2. Curtir/Descurtir vídeo")
        print("3. Favoritos")
        print("4. Ver vídeos curtidos")
        print("0. Sair")
        opcao = input("Escolha: ") #user escolhe oq ele deseja fazer

        if opcao == "1": #chama a funcao de BUSCAR VIDEOS
            buscar_videos() 
        elif opcao == "2": #se nao, chama a funcao CURTIR VIDEOS
            curtir_videos(usuario)
        elif opcao == "3":# se nao, abre o MENU FAVORITOS
            menu_favoritos(usuario)
        elif opcao == "4":
            ver_curtidas(usuario)
        elif opcao == "0": #sai do loop, LOGOUT
            break
        else:
            print("Opção inválida!") #se nao, opcao invalida

#menu principal ANTES DE LOGAR
def menu_principal(): #funcao NAO RECEBE NADA pq é a PORTA DE ENTRADA
    popular_videos() #popula videos de ex caso o arquivo estiver vazio
    while True: #loop o MENU fica aparecendo até o user escolher 0 para sair
        print("\n Bem vindo ao FEItv") #mostra as opcoes abaixo
        print("1. Cadastrar usuário")
        print("2. Login")
        print("0. Sair")
        opcao = input("Escolha: ") #user escolhe

        if opcao == "1": # se o user escolher 1, vai para a funcao CADASTRAR USUARIO
            cadastrar_usuario()
        elif opcao == "2": #se nao, ele escolher 2, VAI PARA FUNCAO LOGIN
            usuario = login_usuario()
            if usuario: #se ele nao tiver login, retorna NONE e aparece o MENU PRINCIPAL
                menu_usuario(usuario)
        elif opcao == "0": #ENCERRA O PROGRAMA
            print("Até mais!")
            break
        else:
            print("Opção inválida!")
 
menu_principal() #INICIA O PROGRAMA