from flask_cors import CORS, cross_origin
from flask import Flask, flash, redirect, request, Response, render_template, url_for
from models import end_point_action

# Instantiate object app
app = Flask(__name__, template_folder='templates')
# Add cross origin security
CORS(app)
app.secret_key = 'the random string'

# connect to database
from db_manager import db, setup_database,execute_sql,execute_update
if (db == None):
    app.logger.error("Not able to connect to db")
    raise Exception("ERROR")
setup_database(db)
app.logger.info("Database created and populated")

@app.route("/")
def home():
    return redirect(url_for("auth"))

@app.route('/auth', methods = ['GET', 'POST'])
def auth():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        record = execute_sql(db,
            f"SELECT * FROM users WHERE email = '{email}' AND password = '{password}'")
        email_checker = execute_sql(db,
            f"SELECT * FROM users WHERE email = '{email}'")
        if not record:
            flash(f"You have entered the wrong password for {email}.")
            return render_template("auth/Login.html")
        elif not record:
            flash("Account doesnt exist!")
            return render_template("auth/Login.html")
        else:
            flash("Logged in")
        return redirect(url_for("rentals"))
        #return render_template("listings/index.html")
    
    elif request.method == 'GET':
        return render_template("auth/Login.html")
    
@app.route('/register', methods = ['POST'])
def register():
    if request.method == 'POST':
        email = request.form.get("email")
        password = request.form.get("password")
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        age = request.form.get("age")

        duplicate_account = execute_sql(db,
            f"SELECT * FROM users WHERE email = '{email}'") 
        if len(duplicate_account): 
            flash(f"Account already exists for {email}!")
            return redirect(url_for("auth"))
        
        record = execute_update(db,
            f'''
            INSERT INTO users (fname, lname, email, age, password) values
            ('{fname}', '{lname}', '{email}', {age}, '{password}');
            ''')
        db.commit()
        flash(f"Yay {fname} you now have an account!!!")
    return redirect(url_for("auth"))
        
@app.route('/<string:email>/edit', methods=('GET', 'POST')) #char or int
def edit(email):
    if request.method == 'POST':
        password = request.form['password']
        credit_card = request.form['credit_card']
        credit_card_type = request.form['credit_card_type']
        credit_card_action = request.form['credit_card_action']
        
        if not password:
            flash('Password is required!')
        else:
            
            execute_update(db,f'''UPDATE user SET password = {password}
                                WHERE email = {email}''')
            db.commit()
            flash('Updated your password!!!')
        ## Update credit card only
        if not (credit_card and credit_card_type):
            flash('Credit card number and type is required!')
        else:
            credit_card_operation(credit_card_action, credit_card, credit_card_type, email)
            flash('Updated your credit card!!!')
            
    return render_template('auth/Update.html')

def credit_card_operation(action, number, type, email):
    if action == "UPDATE":
        execute_update(db,f'''UPDATE credit_card SET type = '{type}',
                                number = '{number}'
                                WHERE email = '{email}';''')
            
    elif action == "ADD":
        execute_update(db,f'''INSERT INTO credit_card(type,number,email) values
                           ('{type}','{number}','{email}');''')
    db.commit()
    return

@app.route('/listings')
def get_my_listings():
    listings = execute_sql(db,
        f'''SELECT h.location, h.price, h.num_room, hr.rating, hr.date, u.username 
        FROM houses h, house_ratings hr, users u 
        WHERE u.email = h.owner_email AND 
        hr.houseid = h.id 
        ORDER BY h.location DESC'''
    )
    db.commit()
    return render_template('listings/index.html', listings=listings)
        
@app.route('/listings/create', methods = ['GET', 'POST'])
# @login_required #to add login required function --> either in auth(), etc
def create_listing():
    if request.method == 'POST':
        location = request.form.get('location')
        price = request.form.get('price')
        num_room = request.form.get('num_room')
		# How do we generate random unique not null id number?
		# How do we obtain the current user's email to execute SQL command?
    if not location or not price or not num_room:
        error = 'All fields are required.'
    if error is not None:
        flash(error)
    else:
        id = generate_random_id() # function to be made
        execute_sql(db,
        f"INSERT INTO houses (id, location, price, num_room, owner_email), ('{id}','{location}', '{price}', '{num_room}, '{g.user['email']}')"
        )
    return redirect(url_for('display_my_listings'))
    
@app.route('/rentals', methods = ['GET', 'POST'])
def rentals():
    rental = execute_sql(db,
        f'''SELECT * FROM houses WHERE is_rented = false'''
    )
    db.commit()
    return render_template('rentals.html', rental=rental)

if __name__ == "__main__":
    app.run()