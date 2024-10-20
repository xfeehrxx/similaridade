from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity as cs 
import pandas as pd

def semelhanca(query, document):
    
    total = df['title'].tolist() + [user]
    vectorizer = TfidfVectorizer()

    tfidfTotal = vectorizer.fit_transform(total)
    tfidfUser = tfidfTotal[-1]
    tfidfTitulos = tfidfTotal[:-1]

    return cs(tfidfUser, tfidfTitulos)

user = input('Digite um anime: ')
df= pd.read_csv('animeDataSet.csv')

similaridade = semelhanca(user, df['title'])
limiar = 0.95
indices_similares = [i for i, sim in enumerate(similaridade[0]) if sim >= limiar]

if indices_similares:
    titulos_similares = df['title'].iloc[indices_similares]
    similaridade = semelhanca(df['synop'][titulos_similares.index[0]], df['synop'])
else:
    top5 = similaridade[0].argsort()[-5:][::-1]
    titulos_parecidos = df['title'].iloc[top5]
    print(titulos_parecidos)
    user = input("Se o anime desejado apareceu na lista, digite o numero na frente dele, caso não tenha aparecido, aperte N: ")
    if user.lower() == 'n':
        user = input('Não temos o anime desejado na nossa base, favor digite a sinopse em ingles: ')
    else:
        user = df['synop'][int(user)]
    similaridade = semelhanca(user, df['synop'])

top5 = [i for i, sim in enumerate(similaridade[0]) if sim < 1.0]  
top5 = sorted(top5, key=lambda i: similaridade[0][i], reverse=True)[:5]  

print("\nTop 5 sinopses mais parecidas:")
for i in top5:
    titulo = df['title'].iloc[i]
    porcentagem = similaridade[0][i] * 100 
    print(f"{titulo} - Similaridade: {porcentagem:.2f}%")


