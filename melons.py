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
    melon = model.get_melon_by_id(id)
    print melon
    return render_template("melon_details.html",
                  display_melon = melon)

@app.route("/cart")
def shopping_cart():
    #This code checks if shopping cart is empty, if so set this dictionary to empty
    #So page does not throw error and display empty shopping cart
    melon_list = []
    print "session", session

    if session.get('melon_cart') == None:
        session['melon_cart'] = {}
    #This block iterates through sessionmelon cart for each melon id 
    #and creates a list of melon objects with all melon details pulled from Db.
    for melon_id in session['melon_cart']:
        curr_melon = model.get_melon_by_id(melon_id)
        melon_list.append(curr_melon)

    # This block itetrates through melon list for each melon object and adds each melon attribute to list
    cart_items = []
    for melon_object in melon_list:

        # we want to get the melon id, the melon name, price and the count (located in session['melon_cart'])
        melon_attributes = {
            "id" : melon_object.id,
            "price" : melon_object.price,
            "name" : melon_object.common_name,
            "quantity" : session['melon_cart'][str(melon_object.id)],
            "total" : int(melon_object.price) * int(session['melon_cart'][str(melon_object.id)])
        }
        cart_items.append(melon_attributes)

    #This code calculates whole total of shopping cart
    final_total = 0
    for my_item_dict in cart_items:
        my_total = my_item_dict.get("total")
        final_total = my_total + final_total

    #print "cart items", cart_items
    return render_template("cart.html", cart_items = cart_items, final_total = final_total)
    
@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """TODO: Finish shopping cart functionality using session variables to hold
    cart list.
    
    Intended behavior: when a melon is added to a cart, redirect them to the
    shopping cart page, while displaying the message
    "Successfully added to cart" """
#This code saves melons in the shopping cart
    if session.get('melon_cart') == None:
        session['melon_cart'] = {}

    id = str(id)
    if id in session['melon_cart']:
        print "HERE"
        session['melon_cart'][id] += 1  
    else:
        session['melon_cart'][id] = 1
    flash("Successfully added melon to the cart %s" % id )

    return redirect('/cart')


@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    username = request.form.get("email")
    password = request.form.get("password")
    #Stores username, password collected from form and checks against Db.
    cname = model.get_customer_by_email(username)
    print cname.givenname

    #if user exist in Db, sends them to logged in session, otherwise 
    #sends them to melons page
    if cname != None:
        session['email'] = cname.email
        print session['email']
        flash("Successfully logged in %s" % cname.email)
    return redirect("/melons")

    return "Oops! This needs to be implemented"

@app.route("/logout")
def process_logout():
    del session['email']

    return redirect("/melons")

@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

if __name__ == "__main__":
    app.run(debug=True)
