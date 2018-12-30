import data as dt
import numpy as np
from sklearn import naive_bayes
from sklearn import metrics

from sklearn.preprocessing import Normalizer
def normalizar(X):
    transformer = Normalizer().fit_transform(X)
    transformer
    Normalizer(copy=True, norm='l2')
    return transformer
    print(transformer)


dataset = dt.selecionar_features(['radiant_win', 'hero_id','level'])

#dataset = dt.selecionar_features(['radiant_win', 'hero_id','level'])

classes = [i[0][0] for i in dataset]
dc = [i[1] for i in dataset]
dc = np.array(dc)

dc = normalizar(dc)
print(dc)
naive = naive_bayes.MultinomialNB()
treino = dc[0:50000]
treino_classe = classes[0:50000]
teste = dc[50000:60000]
teste_classes = classes[50000:60000]
naive.fit(treino,treino_classe)
x = naive.predict(teste)
y = metrics.accuracy_score(y_true=teste_classes, y_pred=x)
print(y)