from flask import Flask, jsonify, request

app = Flask(__name__)

stores=[
    {
    'name' : 'ABC stores',
    'items' : [{
                'name' : 'soap',
                'price' : 20
    }
    ]
}
]

@app.route('/')
def home():
    return 'Hello World'

#Get all stores
@app.route('/store')
def get_store():
    return jsonify({'stores' : stores})

#Get a store with store name
@app.route('/store/<string:name>')
def get_sore_name(name):
    for store in stores:
        if store['name']==name:
            return jsonify({'store' : store})

#Get items of a store
@app.route('/store/<string:name>/items')
def get_item(name):
    for store in stores:
        if store['name'] == name:
            return jsonify({'items': store['items']})

#Create store
@app.route('/store',methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
            'name': request_data['name'],
            'items': []
        }
    stores.append(new_store)
    return jsonify(new_store)


#Create items in a store
@app.route('/store/<string:name>/item',methods=['POST'])
def set_item(name):
    item=request.get_json()
    for store in stores:
        if name in store['name']:
            store['items'].append(item)
            return jsonify(store)
    return 'Store not found'



app.run(port=5000,debug=True)


