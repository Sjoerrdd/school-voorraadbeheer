from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key" # Deze key wordt gebruikt om wachtwoorden te salten.


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:''@localhost/crud' # protocol://gebruikersnaam:wachtwoord@host/database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Database aanmaken
# TODO: Importen uit aparte bestanden
class Product(db.Model):

  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(100))
  quantity = db.Column(db.Integer)
  minimum = db.Column(db.Integer)


  def __init__(self, name, quantity, minimum):
    self.name     = name
    self.quantity = quantity
    self.minimum  = minimum


class User(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  name = db.Column(db.String(100))
  password = db.Column(db.String(100))


  def __init__(self, name, email, phone):
    self.name = name
    self.password = password
    self.phone = phone

# Homepagina
@app.route('/')
def Index():
  return render_template("index.html", products = Product.query.all())

# Product bijwerken. (Aantallen, naam of minimum wijzigen.)
@app.route('/update', methods = ['GET', 'POST'])
def update():
  if request.method == 'POST':
    product = Product.query.get(request.form.get('id'))
    product.name = request.form['name']
    product.quantity = request.form['quantity']
    product.minimum = request.form['minimum']
    db.session.commit()
    flash("Product " + request.form["name"] + " succesvol bijgewerkt.")
    return redirect(url_for('Index'))

# Nieuw product toevoegen
@app.route('/insert', methods = ['POST'])
def insert():
  if request.method == 'POST': # POST request. (Kan ook alleen maar POST zijn, maar fallback om fouten te voorkomen door oudere browsers.)

    product = Product(
      request.form['name'], 
      request.form['quantity'], 
      request.form['minimum']
    )
    db.session.add(product)
    db.session.commit()
    flash("Product "+ request.form["name"] +" succesvol toegevoegd.")
    return redirect(url_for('Index'))

# Product verwijderen.
@app.route('/delete/<id>/', methods = ['GET', 'POST'])
def delete(id):
    db.session.delete(Product.query.get(id))
    db.session.commit()
    flash("Product succesvol verwijderd.")
    return redirect(url_for('Index'))


# Flask debuggen.
if __name__ == "__main__":
    app.run(debug=True)