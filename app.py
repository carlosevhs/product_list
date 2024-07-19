from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# MockAPI URL
MOCKAPI_URL = 'https://669a5a209ba098ed61ff5259.mockapi.io/products'


@app.route('/')
def index():
    response = requests.get(MOCKAPI_URL)
    products = response.json()
    products.sort(key=lambda x: x['value'])
    return render_template('index.html', products=products)


@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        value = float(request.form['value'])
        description = request.form['description']
        available = request.form['availability'] == 'true'

        new_product = {
            "name": name,
            "value": value,
            "description": description,
            "available": available
        }

        requests.post(MOCKAPI_URL, json=new_product)
        return redirect(url_for('index'))

    return render_template('add_product.html')


@app.route('/edit/<product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    if request.method == 'POST':
        try:
            name = request.form['name']
            value = float(request.form['value'])
            description = request.form['description']
            available = request.form['availability'] == 'true'

            updated_product = {
                "name": name,
                "value": value,
                "description": description,
                "available": available
            }

            response = requests.put(f"{MOCKAPI_URL}/{product_id}", json=updated_product)
            if response.status_code == 200:
                return redirect(url_for('index'))
            else:
                return "Erro ao editar o produto", 500
        except Exception as e:
            return "Erro ao processar o formulário", 500

    response = requests.get(f"{MOCKAPI_URL}/{product_id}")
    if response.status_code == 200:
        product = response.json()
        return render_template('edit_product.html', product=product)
    else:
        return "Erro ao carregar o produto", 500


@app.route('/delete/<product_id>')
def delete_product(product_id):
    response = requests.delete(f"{MOCKAPI_URL}/{product_id}")
    if response.status_code == 200:
        return redirect(url_for('index'))
    else:
        return "Erro ao excluir o produto", 500


if __name__ == '__main__':
    app.run(debug=True)
