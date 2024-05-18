from flask import Flask, request, render_template, g
from flask.json import jsonify
from products import products
from db import get_db
from flask_wtf import FlaskForm
from wtforms import HiddenField, StringField, EmailField, TelField
from wtforms.validators import InputRequired, Length


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-keylalaolala312'

    from db import init_db
    init_db(app)

    return app


app = create_app()


class OrderForm(FlaskForm):
    """Форма для оформления заказа"""

    full_name = StringField('Name, Surname', validators=[
        InputRequired(message='Пожалуйста, введите ваше имя'),
        Length(min=4, max=45)
    ])
    email = EmailField('E-mail', validators=[
        InputRequired(message='Пожалуйста, введите ваш email'),
        Length(min=5, max=50)
    ])
    total_price = HiddenField('Products')


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


@app.route('/basket', methods=['GET', 'POST'])
def basket_page():
    """Страница корзины"""
    form = OrderForm()
    if request.method == 'POST' and form.validate_on_submit():
        print(form.full_name.data)
        print(form.email.data)
        print(form.total_price.data)
        db = get_db()
        db.execute(
            """
            INSERT INTO orders
            (full_name, email, total_price) VALUES
            (?, ?, ?)
            """,
            (form.full_name.data, form.email.data, form.total_price.data)
        )
        db.commit()
        return render_template("index.html")
    return render_template('basket.html', form=form)


@app.route('/basket-products')
def products_for_basket():
    """Список товаров для корзины"""
    ids = request.args.get('ids')
    if not ids:
        return jsonify([])
    ids = ids.split(',')
    selected_products = []
    for id in ids:
        product = next((x for x in products if x['id'] == int(id)), None)
        if product:
            selected_products.append(product)
    return jsonify(selected_products)


if __name__ == '__main__':
    app.run(debug=True)
