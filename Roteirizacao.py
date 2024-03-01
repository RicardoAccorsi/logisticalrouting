import pandas as pd


def main():
    hierarquizacao = pd.read_excel(r"C:\Users\User\Downloads\Trabalho 1 - Deadline 24_05 (2) (1).xlsx", sheet_name="Página7")
    infos = pd.read_excel(r"C:\Users\User\Downloads\Trabalho 1 - Deadline 24_05 (2) (1).xlsx", sheet_name="Página8")

    #display(hierarquizacao)

    #display(infos)

    roteiros = {}
    roteiro = []
    ja_foi = []

    CAP = 2800
    TEMPO = 8 * 60
    KM_H = 60

    cont = 0

    resposta = criar_roteiro(hierarquizacao, infos, roteiros, roteiro, CAP, TEMPO, KM_H, cont, ja_foi)

    infos = infos[["Número", "Endereço do Cliente"]]
    
    convertido = resposta.copy()

    roteiro_convertido = []
    for rot5 in convertido:
        for item in convertido[rot5]:
            if item == 0:
                roteiro_convertido.append("Depósito")
            else:
                lugar = infos.loc[infos["Número"] == int(item), "Endereço do Cliente"].item()
                roteiro_convertido.append(lugar)
        convertido[rot5] = roteiro_convertido.copy()
        roteiro_convertido.clear()

    print(resposta)
    print(convertido)


def ajustar_df(lista, df):
    for i in lista:
        try:
            df = df.drop(i)
        except KeyError:
            pass

    return df


def criar_roteiro(hierarquizacao, infos, roteiros, roteiro, CAP, TEMPO, KM_H, cont, ja_foi):

    """
    Função que cria os roteiros de percurso a partir do Método de Clark e Wright

    Args:
        hierarquizacao (df): dataframe que contém uma coluna com a nomenclatura (S_i_j) e o seu
        respectivo ganho. Deve estar em ordem decrescente.
        infos (df): dataframe contendo os endereços e seus índices, assim como o tempo de descarga,
        KG de produto, e distância entre os demais pontos.
        roteiros (dict): dicionário vazio que será preenchido com listas de roteiros
        roteiro (list): lista auxiliar, inicialmente vazia, que armazenará roteiros individuais e depois irá compor os itens
        do dicionário roteiros
        CAP (float): representa a retrição de KG por caminhão
        TEMPO (float): representa a restrição de tempo diário por caminhão
        KM_H (float): representa a velocidade média percorrida pelo caminhão
        cont (int): contador, inicializado em 0, que irá contar quantos dos endereços já estão no roteiro
        analisado, podendo variar de 0 a 2.
        ja_foi (list): lista auxiliar, inicialmente vazia, que será utilizada para armazenar os endereços
        que já foram abarcados por algum roteiro

    Return:
        roteiros(dict): a função retorna um dicionário contendo várias listas, sendo cada lista um roteiro
        distinto, após serem avaliadas as restrições de capacidade.

    """


    # teste
    todos_itens = len(infos.index)
    atual = 0
    while atual != todos_itens:

        # fim do teste

        for linha in hierarquizacao.index:

            # isolar números da nomenclatura
            nome = hierarquizacao.loc[linha, "nomenclatura"]
            nome = nome.replace("S_", "")
            nums = nome.split("_")

            # percorrer dicionário previamente para ver se valores já existem em algum roteiro
            tem_um = tem_outro = tem_dois = False

            for rot in roteiros:

                if nums[0] in roteiros[rot]:
                    tem_um = True

                if nums[1] in roteiros[rot]:
                    tem_outro = True

            if tem_outro and tem_um:
                tem_dois = True

            if tem_um is False and tem_outro is False and tem_dois is False:
                cont += 1

                roteiro.append(0)

                # pegar carga total do percurso
                carga = 0
                for n in nums:
                    carga += infos.loc[infos["Número"] == int(n), "Kg de produto/semana"].item()

                # checar restrições
                if carga <= CAP:

                    # pegar distâncias entre os pontos
                    dist_0_num = infos.loc[infos["Número"] == int(nums[0]), 0].item()
                    dist_num_outro = infos.loc[infos["Número"] == int(nums[0]), int(nums[1])].item()
                    dist_outro_0 = infos.loc[infos["Número"] == int(nums[1]), 0].item()

                    dist = dist_0_num + dist_num_outro + dist_outro_0

                    temp_desloc = (dist / KM_H) * 60
                    temp_desc = infos.loc[infos["Número"] == int(nums[0]), "Tempo de Descarga (min.)"].item() + infos.loc[
                        infos["Número"] == int(nums[1]), "Tempo de Descarga (min.)"].item()
                    tempo = temp_desloc + temp_desc

                    if tempo <= TEMPO:
                        ja_foi.append(linha)
                        roteiro.append(nums[0])
                        roteiro.append(nums[1])
                        roteiro.append(0)
                        roteiros[cont] = roteiro.copy()
                        roteiro.clear()
                else:
                    continue

            # se for o caso de adicionar um novo
            else:

                for rot2 in roteiros:
                    rot_atual = roteiros[rot2]

                    # se já tiver os dois, pular
                    if tem_dois:
                        ja_foi.append(linha)
                        break

                    # se apenas um dos dois estiver na lista
                    if nums[0] in rot_atual and tem_outro is False:

                        # verificar se há existência de 0 à esquerda ou à direita
                        if rot_atual[rot_atual.index(nums[0]) - 1] == 0:
                            roteiros[rot2].insert(1, nums[1])

                            # verificar restrições
                            pontos_meio = rot_atual[1:-1]

                            carga = 0
                            for m in pontos_meio:
                                carga += infos.loc[infos["Número"] == int(m), "Kg de produto/semana"].item()

                            if carga <= CAP:

                                # distância do depósito para o ponto inicial e para o ponto final
                                dist_0_num = infos.loc[infos["Número"] == int(rot_atual[1]), 0].item()
                                dist_outro_0 = infos.loc[infos["Número"] == int(rot_atual[-2]), 0].item()

                                dist_entre = 0
                                for i in range(len(pontos_meio) - 1):
                                    dist_entre += infos.loc[
                                        infos["Número"] == int(pontos_meio[i]), int(pontos_meio[i + 1])].item()

                                dist = dist_0_num + dist_outro_0 + dist_entre

                                temp_desloc = (dist / KM_H) * 60

                                temp_desc = 0
                                for desc in pontos_meio:
                                    temp_desc += infos.loc[infos["Número"] == int(desc), "Tempo de Descarga (min.)"].item()

                                tempo = temp_desloc + temp_desc

                                if tempo <= TEMPO:
                                    ja_foi.append(linha)
                                    break

                                else:
                                    roteiros[rot2].pop(1)
                                    break
                            else:
                                roteiros[rot2].pop(1)
                                break

                        elif rot_atual[rot_atual.index(nums[0]) + 1] == 0:
                            roteiros[rot2].insert(-2, nums[1])

                            # verificar restrições
                            pontos_meio = rot_atual[1:-1]

                            carga = 0
                            for m in pontos_meio:
                                carga += infos.loc[infos["Número"] == int(m), "Kg de produto/semana"].item()

                            if carga <= CAP:

                                # distância do depósito para o ponto inicial e para o ponto final
                                dist_0_num = infos.loc[infos["Número"] == int(rot_atual[1]), 0].item()
                                dist_outro_0 = infos.loc[infos["Número"] == int(rot_atual[-2]), 0].item()

                                dist_entre = 0
                                for i in range(len(pontos_meio) - 1):
                                    dist_entre += infos.loc[
                                        infos["Número"] == int(pontos_meio[i]), int(pontos_meio[i + 1])].item()

                                dist = dist_0_num + dist_outro_0 + dist_entre

                                temp_desloc = (dist / KM_H) * 60

                                temp_desc = 0
                                for desc in pontos_meio:
                                    temp_desc += infos.loc[infos["Número"] == int(desc), "Tempo de Descarga (min.)"].item()

                                tempo = temp_desloc + temp_desc

                                if tempo <= TEMPO:
                                    ja_foi.append(linha)
                                    break

                                else:
                                    roteiros[rot2].pop(-2)
                                    break
                            else:
                                roteiros[rot2].pop(-2)
                                break


                    # se apenas um dos dois estiver na lista
                    elif nums[1] in rot_atual and tem_um is False:

                        # verificar se há existência de 0 à esquerda ou à direita
                        if rot_atual[rot_atual.index(nums[1]) - 1] == 0:
                            roteiros[rot2].insert(1, nums[0])

                            # verificar restrições
                            pontos_meio = rot_atual[1:-1]

                            carga = 0
                            for m in pontos_meio:
                                carga += infos.loc[infos["Número"] == int(m), "Kg de produto/semana"].item()

                            if carga <= CAP:

                                # distância do depósito para o ponto inicial e para o ponto final
                                dist_0_num = infos.loc[infos["Número"] == int(rot_atual[1]), 0].item()
                                dist_outro_0 = infos.loc[infos["Número"] == int(rot_atual[-2]), 0].item()

                                dist_entre = 0
                                for i in range(len(pontos_meio) - 1):
                                    dist_entre += infos.loc[
                                        infos["Número"] == int(pontos_meio[i]), int(pontos_meio[i + 1])].item()

                                dist = dist_0_num + dist_outro_0 + dist_entre

                                temp_desloc = (dist / KM_H) * 60

                                temp_desc = 0
                                for desc in pontos_meio:
                                    temp_desc += infos.loc[infos["Número"] == int(desc), "Tempo de Descarga (min.)"].item()

                                tempo = temp_desloc + temp_desc

                                if tempo <= TEMPO:
                                    ja_foi.append(linha)
                                    break

                                else:
                                    roteiros[rot2].pop(1)
                                    break
                            else:
                                roteiros[rot2].pop(1)
                                break

                        elif rot_atual[rot_atual.index(nums[1]) + 1] == 0:
                            roteiros[rot2].insert(-1, nums[0])

                            # verificar restrições
                            pontos_meio = rot_atual[1:-1]

                            carga = 0
                            for m in pontos_meio:
                                carga += infos.loc[infos["Número"] == int(m), "Kg de produto/semana"].item()

                            if carga <= CAP:

                                # distância do depósito para o ponto inicial e para o ponto final
                                dist_0_num = infos.loc[infos["Número"] == int(rot_atual[1]), 0].item()
                                dist_outro_0 = infos.loc[infos["Número"] == int(rot_atual[-2]), 0].item()

                                dist_entre = 0
                                for i in range(len(pontos_meio) - 1):
                                    dist_entre += infos.loc[
                                        infos["Número"] == int(pontos_meio[i]), int(pontos_meio[i + 1])].item()

                                dist = dist_0_num + dist_outro_0 + dist_entre

                                temp_desloc = (dist / KM_H) * 60

                                temp_desc = 0
                                for desc in pontos_meio:
                                    temp_desc += infos.loc[infos["Número"] == int(desc), "Tempo de Descarga (min.)"].item()

                                tempo = temp_desloc + temp_desc

                                if tempo <= TEMPO:
                                    ja_foi.append(linha)
                                    break

                                else:
                                    roteiros[rot2].pop(-2)
                                    break
                            else:
                                roteiros[rot2].pop(-2)
                                break
                    else:
                        continue

        lista_todos_itens = []
        for rot3 in roteiros:
            lista_todos_itens += roteiros[rot3]

        itens = list(filter(lambda a: a != 0, lista_todos_itens))
        atual = len(itens)

    return roteiros


if __name__ == "__main__":
    main()
