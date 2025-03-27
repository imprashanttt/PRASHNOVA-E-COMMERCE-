from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session,
    send_from_directory,
)
from flask_wtf import FlaskForm, form
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from flask_mail import Mail, Message
import os


app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey"  # Required for CSRF Protection
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:1234@localhost/store"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "prashu8511@gmail.com"
app.config["MAIL_PASSWORD"] = "zvep pvsq juuq ynck"
app.config["UPLOAD_FOLDER"] = "UPLOADS"


db = SQLAlchemy(app)
mail = Mail(app)
bcrypt = Bcrypt(app)


class userAuth(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    address = StringField(
        "Address", validators=[DataRequired(), Length(min=10, max=200)]
    )
    email = EmailField("Email", validators=[DataRequired(), Length(min=2, max=100)])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8, max=20)]
    )
    submit = SubmitField("Submit")


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(300), nullable=False)

    def __init__(self, username, email, address, password):
        self.username = username
        self.email = email
        self.address = address
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(600), nullable=False)

    def __init__(self, title, price, description, image, quantity, category):
        self.title = title
        self.price = price
        self.quantity = quantity
        self.description = description
        self.image = image
        self.category = category


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)

    def __init__(self, user_id, product_id, quantity):
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity


@app.context_processor
def inject_user_status():
    user_logged_in = "username" and "user_id" in session
    try:
        return {"user_logged_in": user_logged_in, "username": session["username"]}
    except:
        return {"user_logged_in": user_logged_in}


@app.route("/")
def index():
    product = Product.query.all()
    try:
        user_logged_in = "username" and "user_id" in session
        return render_template(
            "index.html",
            user_logged_in=user_logged_in,
            username=session["username"],
            user_id=session["user_id"],
            product=product,
        )

    except Exception as e:
        return render_template("index.html", user_logged_in=False, product=product)


@app.route("/register", methods=["POST", "GET"])
def register():
    form = userAuth()
    if request.method == "GET":
        return render_template("register.html", form=form)
    else:
        username = form.username.data
        address = form.address.data
        email = form.email.data
        password = form.password.data
        try:
            user = User(username, email, address, password)
            db.session.add(user)
            db.session.commit()
            return redirect("login")
        except Exception as e:
            print(f"This is having an error :- {e} ")
            return render_template("register.html", form=form)


@app.route("/login", methods=["POST", "GET"])
def login():
    form = userAuth()
    if request.method == "GET":
        return render_template("login.html", form=form)
    else:
        email = form.email.data
        password = form.password.data
        try:
            user = User.query.filter_by(email=email).first()
            print(user.email)
            print(user.password)
            if user.email and bcrypt.check_password_hash(user.password, password):
                session["username"] = user.username
                session["user_id"] = user.id
                print(session["username"])
                return redirect("/")
        except Exception as e:
            return f"This is having an error :- {e} "
            # return render_template('index.html',username=session['username'],user_id=session['user_id'])


@app.route("/add", methods=["POST", "GET"])
def add():
    if request.method == "GET":
        return render_template("addProduct.html")
    else:
        title = request.form["title"]
        price = request.form["price"]
        description = request.form["description"]
        quantity = request.form["quantity"]
        category = request.form["category"]
        image = request.files["image"]
        filename = image.filename
        image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        product = Product(title, price, description, filename, quantity, category)
        db.session.add(product)
        db.session.commit()
        return "Product added successfully"


@app.route("/image/<filename>")
def image(filename):
    upload_folder = os.path.abspath(app.config["UPLOAD_FOLDER"])
    return send_from_directory(upload_folder, filename)


@app.route("/cart/<pid>")
def cart(pid):
    user_logged_in = "username" and "user_id" in session
    if user_logged_in:
        product = Product.query.get_or_404(pid)
        return render_template("checkout.html", product=product)
    else:
        return redirect("/login")


@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("user_id", None)
    return redirect("/")


@app.route("/buy/<pid>", methods=["GET", "POST"])
def buy(pid):
    quants = request.form["quantity"]
    product = Product.query.get_or_404(pid)
    cart = Cart(user_id=session["user_id"], product_id=pid, quantity=float(quants))
    db.session.add(cart)
    db.session.commit()
    print("Item added to cart Successfully")
    return redirect("/")


@app.route("/paid/<finalBill>", methods=["GET", "POST"])
def paid(finalBill):
    print(finalBill)
    return render_template(
        "payment.html", username=session["username"], finalBill=finalBill
    )


@app.route("/paymentConfirm",methods=["GET", "POST"])
def confirmPayment():
    try:
        user=User.query.get_or_404(session['user_id'])
        def sendMail(email,message):
            with app.app_context():
                msg=Message('Your Purchase has been completed successfully',
                            sender='prashu8511@gmail.com',
                            recipients=[email]
                            )
                msg.body=message
                mail.send(msg)
        sendMail(email=user.email,message="Your Product will be delivered to your address soon")
    except Exception as e:
        print(f"Everything working well but error is {e}")
            
    return render_template("paymentSuccess.html", username=session["username"])


@app.route("/shop", methods=["GET", "POST"])
def shop():
    product = Product.query.all()
    if request.method == "POST":
        try:
            value = request.form["category"]
            print(value)
            products = Product.query.filter_by(category=value).all()
            return render_template("shop.html", products=products)
        except:
            return render_template("shop.html", products=product)
    else:
        return render_template("shop.html", products=product)


@app.route("/viewcart")
def viewcart():
    cart = Cart.query.filter_by(user_id=session["user_id"]).all()
    user = User.query.get_or_404(session["user_id"])
    productList = []
    quantityList = []
    finalBill = 0
    i = 0
    for cart in cart:
        print(cart.product_id)
        productList.append(cart.product_id)
        quantityList.append(cart.quantity)
    products = []
    for product in productList:
        prod = Product.query.get_or_404(product)
        products.append(prod)

    for product in products:
        finalBill += product.price * quantityList[i]
        i += 1
    print(finalBill)
    return render_template(
        "cartitem.html",
        products=products,
        user=user,
        quantity=quantityList,
        finalBill=finalBill,
    )
    


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/remove/<pid>")
def remove(pid):
    cart = Cart.query.filter_by(user_id=session["user_id"], product_id=pid).first()
    db.session.delete(cart)
    db.session.commit()
    return redirect("/viewcart")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
