"""Logged-in page routes."""
import os
from os import environ, path
from flask import Blueprint, render_template, redirect, url_for, request, Response
from flask_login import current_user, login_required, logout_user
from fuzzywuzzy import process


from werkzeug.utils import secure_filename



main_bp = Blueprint(
    'main_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

@main_bp.route('/')
def index():
    return render_template('index.html')


@main_bp.route('/contuct')
def contact():
    return render_template('contact.jinja2')


@main_bp.route('/home', methods=['GET'])
@login_required
def home():
    return render_template(
        'home.jinja2',
        title='Sniffer Search',
        current_user=current_user,
    )

@main_bp.route('/AboutUs')
def about():
    return render_template('aboutus.html')

@main_bp.route("/")
@main_bp.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('main_bp.index'))


@main_bp.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        # conn = MySQLdb.connect("localhost", "root", "123456", "data")
        # cursor.execute("select * from client-data")
        # data = cursor.fetchall()  # data from database
        # username = request.form.get('uname')
        # userpass = request.form.get('upass')
        # nadmin = environ.get('ADMIN_USER')
        # admin_user = environ.get('ADMIN_PASSWORD')
        # if(username==nadmin) and (userpass==admin_user):
        return render_template('admindash.jinja2')  # , value=data)
    else:
        return render_template('admin.jinja2')


@main_bp.route("/uploader", methods=['GET', 'POST'])
def uploader():
    if request.method == "POST":
        f = request.files['file1']
        AL = ['pdf', 'PDF', 'Docx', 'docx']
        lw = [f.filename[len(f.filename) - 4:len(f.filename)], f.filename[len(f.filename) - 3:len(f.filename)]]

        if (lw[0] in AL) or (lw[1] in AL):
            f.save(path.join(environ.get('UPLOAD_LOCATION'), secure_filename(f.filename)))
            return redirect(url_for('main_bp.home', msg="Uploaded successfully"))
        else:
            return redirect(url_for('main_bp.home', msg="Files not allowed"))

@main_bp.route("/clean", methods=["POST"])
def clean():
    if request.method=="POST":
        for i in range(10):
            a = 1+3
        msg = "complete cleaning"
        return render_template("home.jinja2" , msg = msg )


@main_bp.route("/results", methods=['POST'])
def search_request():
    if request.method == "POST":
        t = request.form.get("text")
        print(t)
        print(os.getcwd())
        document = os.listdir("./flask_login_tutorial/document")
        print(document)
        images = os.listdir("./images")
        print(images)
        best_match = process.extract(t,images)
        print(best_match)
        def takeSecond(elem):
            return elem[1]
        best_match.sort(key=takeSecond)
        best_match.reverse()
        print(best_match)
        images = []
        for p in best_match:
            if p[1] > 35:
                images.append(p[0])
        images = images[0:3]
        print(images)

        text = {"key1":"1.)This creature has female counterparts named Penny and Gown.This creature appears dressed in Viking armor and carrying an ax when he is used as the mascot of PaX, a least privilege protection patch.This creature’s counterparts include Daemon on the Berkeley Software Distribution, or BSD." , "key2":"2.)This creature has female counterparts named Penny and Gown.This creature appears dressed in Viking armor and carrying an ax when he is used as the mascot of PaX, a least privilege protection patch.This creature’s counterparts include Daemon on the Berkeley Software Distribution, or BSD.",
                "key3":"3.)This creature has female counterparts named Penny and Gown.This creature appears dressed in Viking armor and carrying an ax when he is used as the mascot of PaX, a least privilege protection patch.This creature’s counterparts include Daemon on the Berkeley Software Distribution, or BSD."}
        a = zip(text ,document)
        return render_template('results.jinja2',images=images,text=text,a=a)
    else:
        return "Not Allowed"
    # return send_file('ques-ans.pdf', attachment_filename='ques-ans.pdf')
from flask import send_file





@main_bp.route("/results/<string:filename>", methods=["POST"])
def image(filename):
        images = os.listdir("./images")
        print("Arun 1", images)
        if image in images:
            print("Arun",image)
            return send_file("./images/"+filename)
        else:
            print("Arun 2", image)
            return render_template("pdfreader.jinja2", pdf=filename)


@main_bp.route("/results/<string:filename>" , methods=["GET","POST"])
def pdf_reader(filename):
        return render_template("pdfreader.jinja2", pdf=filename)














