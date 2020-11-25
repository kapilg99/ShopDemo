import json
import os

import requests
from flask import Flask, request
from flask.helpers import url_for
from flask.templating import render_template, render_template_string

app = Flask(__name__)


def write_json(data, filename='databases/database.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.route("/")
def index():
    """
    Index page.
    """
    return render_template("home.html")

@app.route("/order")
def order():
    """
    Display Ordered item
    """
    number = request.args.get("number")
    name = request.args.get("name")
    price = request.args.get("price")
    with open("keys/keys.json") as keys_file:
        loaded_json = json.loads(keys_file.read())
        keys = loaded_json["keys"]
        fast2sms_api_key = keys[0]["fast2sms"]
        message = f"You have ordered {name} : {price}"
        url = "https://www.fast2sms.com/dev/bulk"
        payload = f"sender_id=FSTSMS&message={message}&language=english&route=p&numbers={number}"
        headers = {
        'authorization': fast2sms_api_key,
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        }
        response = requests.request("POST", url, data=payload, headers=headers)
        print(response.text)
    return f"You have ordered {name} : Rs.{price}"

@app.route("/display")
def products():
    """
    Display all products.
    """
    to_print="""
            <table >
                <tr>
                    <th>Product ID</th>
                    <th>Product Name</th>
                    <th>Price</th>
                </tr>
        """
    if os.path.exists("databases/database.json"):
        with open("databases/database.json", "r") as db_file:
            try:
                loaded_json = json.loads(db_file.read())
                for item in loaded_json["items"]:
                    order_url = render_template_string(url_for("order"))
                    to_print += f"""<tr>
                                        <form action="{order_url}">
                                            <td>{item['id']}<input type="hidden" name="id" value="{item['id']}"></td>
                                            <td>{item['name']}<input type="hidden" name="name" value="{item['name']}"></td>
                                            <td>{item['price']}<input type="hidden" name="price" value="{item['price']}"></td>
                                            <td><input type="text" name="number" placeholder="Enter phone number"></td>
                                            <td><input type="submit" value="Order"></td>
                                        </form>
                                    </tr>
                                """
                to_print += "</table>"
                to_print = render_template_string(to_print)
                return render_template("products.html").format(product_list=to_print)
            except :
                return render_template("products.html").format(product_list="")
    else:
        return render_template("products.html").format(product_list="Database File Does Not Exist")

@app.route("/insert_product")
def insert_product():
    """
    Insert new product.
    """
    return render_template("insert_product.html")

@app.route("/inserted_product", methods=["PUT", "GET"])
def inserted_product():
    """
    Insert new product.
    """
    if os.path.exists("databases/database.json"):
        with open("databases/database.json") as db_file:
            try:
                loaded_json = json.loads(db_file.read())
                items = loaded_json["items"]
                new_item = {
                    "id" : request.args.get("id"),
                    "name" : request.args.get("name"),
                    "price" : request.args.get("price")
                }
                items.append(new_item)
                write_json(loaded_json)  
                return render_template("insertion_successful.html")
            except :
                return render_template("insertion_fail.html")

if __name__ == "__main__":
    app.run(debug=True)

    
