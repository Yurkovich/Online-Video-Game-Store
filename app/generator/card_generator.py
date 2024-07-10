def generate_product_html(product):
    html = '''
                    <div class="game-item">
                        <div class="card-img-container">
                            <img class="card-img" src="{}" alt=""/>
                        </div>
                        <div class="card-game-title">
                            <h3>{}</h3>
                            <h4>{}</h4>
                        </div>
                        <div class="card-price-discount">
                            <p class="popular-card-price">{} ₽</p>
                            <p class="popular-card-discount">{}%</p>
                        </div>
                    </div>
    '''.format(product['image_url'], product['product_name'], product['genre'], product['price'], product['discount'])

    return html