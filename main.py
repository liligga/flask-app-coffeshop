from flask import Flask, render_template, g
from products import products


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-keylalaolala312'

    from db import init_db
    init_db(app)

    return app


app = create_app()


@app.route('/')
def index_page():
    """Главная страница"""
    all_products = products
    return render_template('index.html', products=all_products)


@app.route('/products/<product>')
def product_page(product):
    """Страница товара"""
    product = next((x for x in products if x['id'] == int(product)), None)
    if not product:
        """Страница 404 если нет такого товара"""
        return render_template('404.html')
    return render_template('product.html', product=product)


@app.route('/basket')
def reservation_page():
    """Страница корзины"""
    return render_template('basket.html')


if __name__ == '__main__':
    app.run(debug=True)
