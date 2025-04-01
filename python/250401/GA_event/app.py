from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/item_info')
def item_info():
    # 선택한 상품 
    user_select = int(request.args['item'])
    print(user_select)
    print(type(user_select))
    return render_template('item_info.html', 
                           selected = user_select)

@app.route('/shop')
def shop():
    # 물건의 수량 
    item_cnt = int(request.args['cnt'])
    # 물건의 가격
    item_price = int(request.args['price'])

    return render_template('shop.html', 
                           price = item_cnt * item_price)



app.run(host='0.0.0.0', port='8080', debug=True)