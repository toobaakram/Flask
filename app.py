from flask import Flask , render_template ,request ,flash , redirect , url_for , session
from flask_mysqldb import MySQL
from passlib.handlers.sha2_crypt import sha512_crypt
from wtforms import Form , StringField , TextAreaField, PasswordField , validators
from functools import wraps


app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "12345"
app.config['MYSQL_DB'] = "ssuetFlask"
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

# Init database
mysql = MySQL(app)

class contactus(Form):
    name = StringField('name' , [validators.Length(min=1 , max=50)])
    email = StringField('email' , [validators.Length(min=6 , max=50)])
    message = StringField('message' , [validators.Length(min=1 , max=200)])


@app.route('/contact' , methods=["GET" , "POST"])
def contact1():
    form = contactus(request.form)
    if request.method == 'POST' and form.validate():
        name =  form.name.data
        email = form.email.data
        message = form.message.data
        # create cursor
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contact(name , email , message) VALUES(%s, %s , %s)" ,
        (name , email , message))
        
        # commit to db
        mysql.connection.commit()

        # close connectioin
        cur.close()

        flash("Your message has been sent" , "success")
        return redirect(url_for('contact'))

    return render_template("contact.html")



@app.route("/")
def home():
    return render_template('index.html')

@app.route("/about")
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True , port=3000)