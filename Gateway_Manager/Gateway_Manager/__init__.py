from flask import *
import sqlite3
from functools import wraps
import os
#MAIN APPLICATION

app = Flask(__name__)

err_msg=""
AUTH_FLAG='Deny'
db_path='/usr/share/apache2/default-site/htdocs/Gateway_Manager/Gateway_Manager/test.db'

ip=os.popen('ip addr show eth1').read().split("inet ")[1].split("/")[0]
conn = sqlite3.connect(db_path)
cur=conn.cursor()
cur.execute("UPDATE Device SET IPv4 = ?  WHERE KEY = 1",(ip,))
conn.commit()
conn.close()
def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if AUTH_FLAG=='Deny':
            return redirect(url_for("login",err_msg="Please login"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@app.route("/login/<err_msg>")
def login(err_msg=" "):
    return render_template('login.html',msg=err_msg)

@app.route("/validate",methods=['GET', 'POST'])
def validate():
    global AUTH_FLAG
    if request.method == 'POST':
      try:
         username = request.form['username']
         password = request.form['password']
         if username=='admin' and password=='admin':
            AUTH_FLAG='Allow'
            return redirect(url_for("admin"))
         else:
            return redirect(url_for("login",err_msg="Incorrect credentials!!!"))
      except:
           return redirect(url_for("login",err_msg="error in login"))


@app.route("/admin")
@authorize
def admin():
    global AUTH_FLAG
    AUTH_FLAG='Deny'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur=conn.cursor()
    cur.execute("SELECT * FROM Device") 
    dev_row=cur.fetchall()
    cur.execute("SELECT * FROM Cloud")
    cld_row=cur.fetchall()
    cur.execute("SELECT * FROM Gateway")
    gwy_row=cur.fetchall()
    conn.close()
    return render_template('dash.html',device_data=dev_row,cloud_data=cld_row,gw_data=gwy_row)

@app.route("/upd",methods=['GET','POST'])
def update():
        if request.form["group"]=='Logout':
            return redirect(url_for("login",err_msg="logged out"))
        elif request.form["group"]=='Device':
            return redirect(url_for("config",grp="dev"))
        elif request.form["group"]=='Cloud':
            return redirect(url_for("config",grp="cld"))
        elif request.form["group"]=='Gateway':
            return redirect(url_for("config",grp="gw"))

@app.route("/config/<grp>")
def config(grp=" "):
    if grp=="dev":
        return render_template('device.html')
    elif grp=="cld":
        return render_template('cloud.html')
    elif grp=="gw":
        return render_template('gw.html')

@app.route("/save",methods=['GET','POST'])
def save():
    if request.form["group"]=='Device':
        i=request.form["dev_id"]
        n=request.form["dev_name"]
        f=request.form["dev_netif"]
        s=request.form["dev_status"]
        conn = sqlite3.connect(db_path)
        cur=conn.cursor()
        cur.execute("UPDATE Device SET ID=?,NAME=?,INTERFACE=?,STATUS=?  WHERE KEY = 1",(i,n,f,s))
        conn.commit()
        conn.close()
        return redirect(url_for("login",err_msg="configuration updated Please login"))
    elif request.form["group"]=='Cloud':
        pr=request.form["cloud_pro"]
        c=request.form["cloud_type"]
        h=request.form["cloud_host"]
        pt=request.form["cloud_port"]
        conn = sqlite3.connect(db_path)
        cur=conn.cursor()
        cur.execute("UPDATE Cloud SET PROTOCOL=?,CONTYPE=?,HOST=?,PORT=?  WHERE KEY = 1",(pr,c,h,pt))
        conn.commit()
        conn.close()
        return redirect(url_for("login",err_msg="configuration updated Please login"))
    elif request.form["group"]=='Gateway':
        n=request.form["gw_node"]
        c=request.form["gw_cloud"]
        conn = sqlite3.connect(db_path)
        cur=conn.cursor()
        cur.execute("UPDATE Gateway SET N_STATUS=?,C_STATUS=?  WHERE KEY = 1",(n,c))
        conn.commit()
        conn.close()
        return redirect(url_for("login",err_msg="configuration updated Please login"))
    
    elif request.form["group"]=='Cancel':
        return redirect(url_for("login",err_msg="Not configured"))


    

        




if __name__ == '__main__':
    app.run()

