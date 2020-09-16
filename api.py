from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
'''
import pandas as pd
from sklearn.model_selection import train_test_split
'''
from sklearn.linear_model import LinearRegression
import pickle


modelo = pickle.load(open('modelo.dat', 'rb'))

# df = pd.read_csv('casas.csv')
# colunas = ['tamanho', 'preco']
# df = df[colunas]
colunas = ['tamanho', 'ano', 'garagem']

'''
X = df.drop('preco', axis=1)
y = df['preco']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
modelo = LinearRegression()
modelo.fit(X_train, y_train)

pickle.dump(modelo, open('modelo.dat', 'wb'))
'''


app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'otoniel'
app.config['BASIC_AUTH_PASSWORD'] = 'flask'

basic_auth = BasicAuth(app)


@app.route('/')
def index():
    return 'Olá'


@app.route('/sentimento/<frase>')
@basic_auth.required
def sentimento(frase):
    tb = TextBlob(frase)
    tb_en = tb.translate(to='en')
    sentimento = tb_en.sentiment.polarity
    return f'<h1>Seu sentimento é: {sentimento}</h1>'


'''
@app.route('/casa/<int:area>')
def preco(area):
    preco = modelo.predict([[area]])
    return f'Uma casa de área {area} custa aproximadamente {preco}'
'''


@app.route('/casa', methods=['POST'])
@basic_auth.required
def preco():
    dados = request.get_json()
    dados_input = [dados[col] for col in colunas]
    preco = modelo.predict([dados_input])
    return jsonify(preco=preco[0])


if __name__ == "__main__":
    app.run()
