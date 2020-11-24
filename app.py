import json
import os

from flask import Flask, request
from flask.templating import render_template

app = Flask(__name__)


def write_json(data, filename='databases/database.json'): 
    with open(filename,'w') as f: 
        json.dump(data, f, indent=4) 

@app.route("/")
def index():
    """
    Index page.
    """
    return render_template("home.html")


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
                    to_print += f"""<tr>
                                        <td>{item['id']}</td>
                                        <td>{item['name']}</td>
                                        <td>{item['price']}</td>
                                    </tr>
                                    """
                to_print += "</table>"
                return render_template("products.html").format(product_list=to_print)
            except :
                return render_template("products.html").format(product_list="No Products available")
    else:
        return render_template("products.html").format(product_list="No Products available")

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
