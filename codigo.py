#1) Quantos artistas temos no catálogo? Quantos álbuns lançados?

import pandas as pd
import numpy as np

artista = artists_df.shape[0] #shape numero de linhas e colunas
album = albums_df.shape[0] #shape numero de linhas e colunas
artista = artists_df.count() #count conta o numero de itens
album = albums_df.count() #count conta o numero de itens
artista = artists_df['id'].count() #count conta o numero de itens
album = albums_df['id'].count() #count conta o numero de itens
artista = artists_df['id'].nunique() #nunique conta valores longe de colunas e unique conta elementos unicos
album = albums_df['id'].nunique() #nunique conta valores longe de colunas e unique conta elementos unicos

print(artista)
print(album)

#2) Quantas nacionalidades? Qual o país com a maior concentração de artistas?

import pandas as pd
import numpy as np

artists_df = pd.read_csv('artists.csv')

df_nacionalidade = artists_df.groupby(['country']).aggregate({'id':'count'}).sort_values(by='id')

print(df_nacionalidade)

#groupby divide o dataframe em grupos nesse caso pais.
#aggregate agrega colunas e linhas

#3 Quantos artistas foram adicionados ao catálogo nos último 3 anos?

df_adicionados = artists_df.copy()
artistas_recentes = df_adicionados.loc[df_adicionados['first_release'] >= 2019]['id'].nunique()
print(artistas_recentes)


#4) Quais os 5 tipos de artista mais presentes no catálogo?

df = artists_df.groupby(['role']).aggregate({'id':'count'}).sort_values(by='id', ascending=False)

df.head(5)

#5) Qual faixa de idade mais comum entre os artistas do catálogo?

import pandas as pd
import numpy as np

artists_df = pd.read_csv('artists.csv')

df = artists_df.copy()
df.loc[:, 'age'] = np.floor((2021 - df['year_of_birth'])/10)*10
df.groupby(['age']).agg({'id':'count'}).sort_values(by='id', ascending=False)

#6) Quantos álbuns foram lançados nos últimos 5 anos?

import pandas as pd
import numpy as np

albums_df = pd.read_csv('albums.csv')

df = albums_df.loc[albums_df['year_of_pub'] >= 2017]
albums_recentes = df.shape[0]
print(f'Álbuns desde 2017: {albums_recentes}')


#7) Quais os 10 gêneros musicais mais presentes no catálogo? Quanto cada um representa do total de vendas?

import pandas as pd
import numpy as np

#8) Quais os gêneros com as melhores avaliações pela Rolling Stone? E quais os piores?

import pandas as pd
import numpy as np

albums_df = pd.read_csv('albums.csv')

df = albums_df.groupby(['genre']).agg({'rolling_stone_critic':'mean'})
top = df.sort_values(by=['rolling_stone_critic']).head(5)
bottom = df.sort_values(by=['rolling_stone_critic'], ascending=False).head(5)
print(f'Piores: {top}\n')
print(f'Melhores: {bottom}')

#9) Quais os artistas de maior sucesso comercial? E de sucesso da crítica especializada?

import pandas as pd
import numpy as np

albums_df = pd.read_csv('albums.csv')

df = albums_df.groupby(['artist_id']).agg({'num_of_sales': 'sum', 'rolling_stone_critic':'mean'})

df_artistas = artists_df.set_index('id').loc[:, ['real_name', 'art_name']]

df_artistas.loc[: ,'artista'] = df_artistas['art_name'].fillna(df_artistas['real_name'])

df_artistas = df.join(df_artistas.loc[:,['artista']])
top_vendas = df_artistas.sort_values(by=['num_of_sales'], ascending=False).head(5)
print('Maiores vendas:')
display(top_vendas)

top_critica = df_artistas.sort_values(by=['rolling_stone_critic'], ascending=False).head(5)
print('Favoritos da crítica')
display(top_critica)

#10) Se tivéssemos que não renovar o contrato dos 20% artistas com pior desempenho na crítica, quanto estaríamos arriscando de vendas 

import pandas as pd
import numpy as np

albums_df = pd.read_csv('albums.csv')

df = albums_df.groupby(['artist_id']).agg({'num_of_sales':'mean', 'rolling_stone_critic':'mean'})

df.loc[:, 'cumulative_rank'] = 100*df['rolling_stone_critic'].rank(ascending=True, pct=True, method='dense')
piores = df.loc[df['cumulative_rank'] < 20]
piores_receita = piores['num_of_sales'].sum()
receita_total = albums_df['num_of_sales'].sum()
share_receita_total = 100*piores_receita/receita_total
print(f'Quantidade de artistas cortados: {piores.shape[0]}, Vendas Perdidas:{piores_receita}, % das Vendas Totais: {share_receita_total}')
