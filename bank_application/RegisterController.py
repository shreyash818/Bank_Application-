from flask import Flask, render_template, request, redirect, url_for, session
from RegisterDb import myDatabase
from Register import Register

# ---------------------- APP CONFIG ----------------------
app = Flask(__name__)
app.secret_key = "super_secret_key"

# Database connection
mydb = myDatabase()


# ---------------------- HOME ----------------------
@app.route('/')
def home():
    return render_template('home.html')


# ---------------------- LOGIN ----------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        uname = request.form.get('username')
        pwd = request.form.get('password')

        result = mydb.fetchUserByUsername(uname)
        if result:
            db_reg = result["RegNumber"]
            db_first = result["FirstName"]
            db_last = result["LastName"]
            db_pass = result["Password"]
            db_acc = result["AccBal"]

            if pwd == db_pass:
                session['user'] = {
                    "RegNumber": db_reg,
                    "FirstName": db_first,
                    "Username": db_last,
                    "AccBal": float(db_acc)
                }
                return redirect(url_for('dashboard'))
            else:
                message = "Incorrect password!"
        else:
            message = "Username not found!"
    return render_template('loginview.html', message=message)


# ---------------------- DASHBOARD ----------------------
@app.route('/Dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('Dashboard.html', user=session['user'])


# ---------------------- LOGOUT ----------------------
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


# ---------------------- REGISTER ----------------------
@app.route('/RegisterView', methods=['GET', 'POST'])
def register():
    message = ""
    if request.method == 'POST':
        regnumber = request.form.get('regnumber')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        password = request.form.get('Password')
        accbal = request.form.get('accbal')

        try:
            accbal = float(accbal)
        except:
            accbal = 0.0

        regobj = Register(regnumber, firstname, lastname, password, accbal)

        try:
            mydb.saveData(regobj)
            return redirect(url_for('login'))
        except Exception as e:
            message = f"Error: {str(e)}"
    return render_template('RegisterView.html', message=message)


# ---------------------- SEARCH ----------------------
@app.route('/search', methods=['GET', 'POST'])
def search():
    message = ""
    user_data = None
    if request.method == 'POST':
        regnumber = request.form.get('regnumber')
        try:
            result = mydb.fetchUserByRegNo(regnumber)
            if result:
                user_data = result
                message = f"Record Found for Reg No: {regnumber}"
            else:
                message = "No record found."
        except Exception as e:
            message = f"Error: {str(e)}"
    return render_template('SearchView.html', message=message, user_data=user_data)


# ---------------------- UPDATE ----------------------
@app.route('/update', methods=['GET', 'POST'])
def update():
    message = ""
    if request.method == 'POST':
        regnumber = request.form.get('regnumber')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')
        accbal = request.form.get('accbal')
        try:
            result = mydb.fetchUserByRegNo(regnumber)
            if result:
                mydb.updateUser(regnumber, firstname, lastname, accbal)
                message = "Record updated successfully!"
            else:
                message = "No record found."
        except Exception as e:
            message = f"Error: {str(e)}"
    return render_template('UpdateView.html', message=message)


# ---------------------- DELETE ----------------------
@app.route('/delete', methods=['GET', 'POST'])
def delete():
    message = ""
    if request.method == 'POST':
        regnumber = request.form.get('regnumber')
        try:
            result = mydb.fetchUserByRegNo(regnumber)
            if result:
                mydb.deleteUser(regnumber)
                message = "Record deleted successfully!"
            else:
                message = "No record found."
        except Exception as e:
            message = f"Error: {str(e)}"
    return render_template('DeleteView.html', message=message)


# ---------------------- DISPLAY ----------------------
@app.route('/display')
def display():
    try:
        users = mydb.fetchAllUsers()
        if not users:
            return render_template('DisplayView.html', users=[], message="No records found.")

        user_list = []
        for u in users:
            reg = u.get("RegNumber", "")
            first = u.get("FirstName", "")
            last = u.get("LastName", "")
            acc = u.get("AccBal", 0.0)
            pwd = u.get("Password", "")
            user_list.append((reg, first, last, acc, pwd))

        message = f"Total {len(user_list)} record(s) found."
        return render_template('DisplayView.html', users=user_list, message=message)

    except Exception as e:
        return render_template('DisplayView.html', users=[], message=f"Error: {str(e)}")


# ---------------------- PROFILE ----------------------
@app.route('/Profileview')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    user = session['user']
    return render_template('Profileview.html', user=user)


# ---------------------- RECHARGE ----------------------
@app.route('/RechargeView', methods=['GET', 'POST'])
def recharge():
    if 'user' not in session:
        return redirect(url_for('login'))

    message = ""
    user = session['user']

    if request.method == 'POST':
        operator = request.form.get('operator')
        mobile = request.form.get('mobile')
        try:
            amount = float(request.form.get('amount'))
        except:
            amount = 0.0

        try:
            new_balance = float(user['AccBal']) - amount
            if new_balance < 0:
                message = "Insufficient Balance!"
            else:
                mydb.updateBalance(user['RegNumber'], new_balance)
                user['AccBal'] = new_balance
                session['user'] = user

                mydb.addRecharge(user['RegNumber'], operator, mobile, amount)
                mydb.addTransaction(user['RegNumber'], "Debit", amount)

                message = f"Recharge of ₹{amount} done successfully!"
        except Exception as e:
            message = f"Error: {str(e)}"

    return render_template('RechargeView.html', user=user, message=message)


# ---------------------- TRANSACTIONS ----------------------
@app.route('/TransactionView')
def transaction():
    if 'user' not in session:
        return redirect(url_for('login'))

    user = session['user']
    try:
        records = mydb.getTransactions(user['RegNumber'])
        transactions = []
        for r in records:
            transactions.append({
                'type': r['Type'],
                'amount': r['Amount'],
                'date': str(r['Date'])
            })
    except Exception as e:
        print("Error fetching transactions:", e)
        transactions = []

    return render_template('TransactionView.html', user=user, transactions=transactions)


# ---------------------- MAIN ----------------------
if __name__ == "__main__":
    app.run(debug=True)
