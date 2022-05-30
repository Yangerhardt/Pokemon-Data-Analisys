import re
import pandas as pd
import numpy as np
from time import sleep

def contagem(df):
    '''
    Função utilizada para contagem de linhas de um dataframe
    :param df: data frame
    :return: número total de linhas
    '''
    df['contagem'] = 1
    total = df['contagem'].count()
    return total
def titulo(msg):
    print('\033[31m     ', end='')
    print(f'-'*100)
    print(f'    {msg:^100}')
    print('     ', end='')
    print('-'*100)
    print('\033[m')

tabela = pd.read_csv('pokemon_data.csv')
titulo('DATABASE GERAL DOS POKEMONS')
print(f'Na base de dados, temos um total de \033[31m{contagem(tabela)}\033[m pokemons cadastrados.\n')

#fogo = tabela.loc[tabela['Type 1'].str.contains('Fire')]
#print(fogo['contagem'].count())

agrupado_tipo = tabela.groupby(['Type 1']).sum().sort_values('contagem', ascending=False)

# Aqui criamos uma nova coluna de "Poder" para classificar os pokemons:
tabela['Power'] = tabela['HP'] + tabela['Attack'] + tabela['Defense'] + tabela['Sp. Atk'] + tabela['Sp. Def'] + tabela['Speed']
# Aqui retiramos algumas colunas sem uso e classificamos de acordo com o poder do maior para o menor
poder = tabela.drop(columns='contagem').loc[tabela['Legendary'] == True].sort_values('Power', ascending=False, ignore_index=True)
# Aqui classificamos de acordo com o tipo para obter uma média de poder de cada tipo:
media_poder = tabela.groupby(['Type 1'], as_index=False).mean()

# Aqui organizamos os dados para obter somente os pokemons lendários, classificados de maior poder para o menor
b = tabela.loc[tabela['Legendary'] == True].sort_values('Power', ascending=False, ignore_index=True)

# Assim que agrupamos os dados pelo seu tipo, o dado usado como "agrupador" (nesse caso o tipo), foi colocado como
# índice. Então, tive que pegar os dados de índices que eram o que me interessavam.
for cont, tipo in enumerate(agrupado_tipo.index):
    print(f'Temos um total de \033[33m{agrupado_tipo["contagem"][cont]}\033[m pokemons do tipo \033[33m{tipo}\033[m.')
    for c, v in enumerate(media_poder['Type 1']):
        if v == tipo:
            print(f'Os pokemons desse tipo tem uma média de poder de \033[35m{media_poder.iloc[c, 11]:.2f}\033[m.')

    if agrupado_tipo['Legendary'][cont] > 1:
        print(f'Deste total, temos \033[34m{agrupado_tipo["Legendary"][cont]}\033[m pokemons \033[31mlendários\033[m.')
        for c, v in enumerate(b['Type 1'] == tipo):
            if v == True:
                print(f'Deste elemento, o pokemon lendário mais forte é o \033[31m{b.iloc[c, 1]}\033[m, com um poder total de \033[32m{b.iloc[c, 13]}\033[m.\n')
                break
    else:
        print('\033[31mNão há\033[m pokemons lendários desse tipo.\n')

titulo('ANÁLISE DE POKEMONS')
while True:
    opcao = str(input('Agora é com você! Qual pokemon você deseja analisar mais detalhadamente?\n'
              'Caso não deseje ver nenhum, basta digitar "sair": ').strip().upper())
    try:
        if opcao == 'SAIR':
            break
        elif opcao.isnumeric():
            print('\033[31mOpção inválida.\033[m')
        else:
            print(f'Analisando o pokemon {opcao}', end='')
            sleep(0.5)
            for i in range(0,3):
                print('.', end='')
                sleep(0.5)
            print()

# Puxa o índice do pokemon
            teste = tabela.loc[tabela['Name'].str.contains(opcao, flags=re.IGNORECASE)].drop(columns='contagem')

# Pegamos o índice do primeiro pokemon procurado, PORÉM, o dado vem no formato "Int64Index". Para voltar ao formato de lista, usamos o comando .tolist() e pegamos o primeiro valor encontrado.
#       print(teste.index.tolist()[0])
# Como já havíamos filtrado anteriormente no loop, o primeiro pokemon já seria o pokemon filtrado, então não precisariamos do índice, mas caso precisássemos, o método acima resolveria.
            print()
            print('\033[36m-'*24)
            print(f'{teste.iloc[0]}')
            print('-' * 24)
            print('\033[m')

    except:
        print('\033[31mPokemon não encontrado :( Tente novamente!\033[m\n')

print('\033[33mDatabase encerrado.\033[m')

