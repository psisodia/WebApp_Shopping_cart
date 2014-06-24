from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2


app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site""" 
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()
    return render_template("all_melons.html",
                           melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    print melon
    return render_template("melon_details.html",
                  display_melon = melon)

@app.route("/cart")
def shopping_cart():
    """TODO: Display the contents of the shopping cart. The shopping cart is a
    list held in the session that contains all the melons to be added. Check
    accompanying screenshots for details."""

    melon_list = []
    print "session", session

    if session.get('melon_cart') == None:
        session['melon_cart'] = {}

    for melon_id in session['melon_cart']:
        melon_list.append(model.get_melon_by_id(melon_id))

    # create a list combining the melon attributes and count
    cart_items = []
    for melon_object in melon_list:
        # we want to get the melon id, the melon name, price and the count (located in session['melon_cart'])

        melon_attributes = {
            "id" : melon_object.id,
            "price" : melon_object.price,
            "name" : melon_object.common_name,
            "quantity" : session['melon_cart'][str(melon_object.id)]
        }
        cart_items.append(melon_attributes)

    print "cart items", cart_items
    return render_template("cart.html", cart_items = cart_items)
    
@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """TODO: Finish shopping cart functionality using session variables to hold
    cart list.
    
    Intended behavior: when a melon is added to a cart, redirect them to the
    shopping cart page, while displaying the message
    "Successfully added to cart" """

    if session.get('melon_cart') == None:
        session['melon_cart'] = {}

    id = str(id)
    if id in session['melon_cart']:
        print "HERE"
        session['melon_cart'][id] += 1
    else:
        session['melon_cart'][id] = 1

    return redirect('/cart')


@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""
    return "Oops! This needs to be implemented"


@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

if __name__ == "__main__":
    app.run(debug=True)
