
from flask import Flask,render_template,flash,redirect,url_for,session,logging,request #flask frameworku icindeki flask sınıfını dahil ediyoruz
from flask_mysqldb import MySQL
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
#kullanıcı kayıt formu

class RegisterForm(Form):
    name = StringField("isim soyisim",validators=[validators.length(min=4,max=25)])
    username = StringField("kullanıcı adı",validators=[validators.length(min=4,max=35)])
    email = StringField("e mail",validators=[validators.email(message = "lutfen gecerli bir email adresi girinizz ")])
    password = PasswordField ("Parola:", validators=[
        validators.DataRequired(message="lutfen bir parola belirleyinn"),
        validators.EqualTo(fieldname= "confirm",message="parolanız uyusmuyor")])
    confirm = PasswordField("parola dogrula ")
class LoginForm(Form):
    username = StringField("kullanıcı adı:")
    password = PasswordField("Parola")



app = Flask(__name__)
app.secret_key="itblog"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "itblog"
app.config["MYSQL_CURSORCLASS"]= "DictCursor"

mysql=MySQL(app) #cursor mysql veritabaninda islem yapmamizi saglayan yapi






@app.route("/")
def index():
    articles=[
        {"id":1 ,"title":"deneme1","content":"deneme1 icerik"},
        {"id":2 ,"title":"deneme2","content":"deneme2 icerik"},
        {"id":3 ,"title":"deneme3","content":"deneme1 icerik"}




    ]
    return render_template("index.html" ,articles= articles)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


#kayıt olma
@app.route("/register",methods=["GET","POST"])
def register():
    form = RegisterForm(request.form)


    if request.method == "POST" and form.validate():
        name = form.name.data 
        username = form.username.data
        email = form.email.data
        password = sha256_crypt.encrypt(form.password.data)  #sifrelenims parola gonderildi 

        cursor = mysql.connection.cursor()

        sorgu="insert into users(name,email,username,password) VALUES(%s,%s,%s,%s)" #format metodu kullanılabilir

        cursor.execute(sorgu,(name,email,username,password))  #demet kullandik tek elemanli dmetde sonuna virgul koyy
        mysql.connection.commit()


        cursor.close()
        flash("basariyla kayit oldunuz","succes")

         #myadminüzerinde islem yapmamizgerekenkisim
        
         #postmu get mi oldugunu anladık
        return redirect(url_for("login"))
    else:

        return render_template("register.html",form = form)

#login islemi
@app.route("/login",methods =["GET","POST"])
def login():
    form = LoginForm(request.form)


    if request.method == "POST":
        username = form.username.data
        password_entered = form.password.data

        cursor = mysql.connection.cursor()
        print(cursor)
       
    #sorgumuzu yazacgiz

        sorgu="Select * From users where username = %s "
    
        result = cursor.execute(sorgu,(username,))
        print(result)

        if result > 0:
            data = cursor.fetchone()
            print(data)
            real_password = data["password"]
            if sha256_crypt.verify(password_entered,real_password):
                flash("basarıyla giris yaptınız....","success")
                session["logged_in"]=True
                session["username"]= username #session baslatıldı 
                return redirect(url_for("index"))
            else:
                flash("parolanızı yanlış girdiniz ", "danger")
                return redirect(url_for("login"))    
        else:
                flash("BOYLE BİR KULLANİCİ BULUNMUYOR","danger")
                return redirect(url_for("login"))
    return render_template("login.html",form = form) 

@app.route("/logout")

def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/article/<string:id>")  #flask dinamik url güzelce arastir
def detail(id):
    return "article id " + id


if __name__ == "__main__":
    app.run(debug=True) #web sunucumuz hata mesajlarımızı göstericek

    #flaskwtf ve wtfin kendi dokumantasyonunu inceleeeee
