import mysql.connector
from Register import Register

class myDatabase:
    def __init__(self):  # ✅ FIXED: added double underscores
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="bank1_app"
        )
        self.cursor = self.conn.cursor(dictionary=True)

    # ---------- Save Account ----------
    def saveData(self, regobj):
        query = """INSERT INTO accounts (RegNumber, FirstName, LastName, Password, AccBal)
                   VALUES (%s, %s, %s, %s, %s)"""
        values = (regobj.regnumber, regobj.firstname, regobj.lastname, regobj.password, float(regobj.accbal))
        self.cursor.execute(query, values)
        self.conn.commit()

    # ---------- Fetch User by Username ----------
    def fetchUserByUsername(self, username):
        query = "SELECT * FROM accounts WHERE LastName = %s"
        self.cursor.execute(query, (username,))
        return self.cursor.fetchone()

    # ---------- Fetch User by Reg Number ----------
    def fetchUserByRegNo(self, regnumber):
        query = "SELECT * FROM accounts WHERE RegNumber = %s"
        self.cursor.execute(query, (regnumber,))
        return self.cursor.fetchone()

    # ---------- Fetch All Users ----------
    def fetchAllUsers(self):
        self.cursor.execute("SELECT * FROM accounts")
        res = self.cursor.fetchall()
        print("Fetched:", res)
        return res

    # ---------- Update User ----------
    def updateUser(self, regnumber, firstname, lastname, accbal):
        query = """UPDATE accounts 
                   SET FirstName = %s, LastName = %s, AccBal = %s 
                   WHERE RegNumber = %s"""
        self.cursor.execute(query, (firstname, lastname, float(accbal), regnumber))
        self.conn.commit()

    # ---------- Delete User ----------
    def deleteUser(self, regnumber):
        try:
            # Delete related records first
            self.cursor.execute("DELETE FROM recharges WHERE RegNumber = %s", (regnumber,))
            self.cursor.execute("DELETE FROM transactions WHERE RegNumber = %s", (regnumber,))

            # Then delete from accounts
            self.cursor.execute("DELETE FROM accounts WHERE RegNumber = %s", (regnumber,))
            
            # Commit all changes
            self.conn.commit()
            print(f"✅ User {regnumber} deleted successfully.")
        except mysql.connector.Error as err:
            print(f"❌ Error deleting user {regnumber}: {err}")
            self.conn.rollback()

    # ---------- Get Balance ----------
    def getBalance(self, regnumber):
        query = "SELECT AccBal FROM accounts WHERE RegNumber = %s"
        self.cursor.execute(query, (regnumber,))
        res = self.cursor.fetchone()
        return res["AccBal"] if res else 0.0

    # ---------- Update Balance ----------
    def updateBalance(self, regnumber, new_balance):
        query = "UPDATE accounts SET AccBal = %s WHERE RegNumber = %s"
        self.cursor.execute(query, (float(new_balance), regnumber))
        self.conn.commit()

    # ---------- Add Recharge ----------
    def addRecharge(self, reg, operator, mobile, amount):
        query = """INSERT INTO recharges (RegNumber, Operator, Mobile, Amount)
                   VALUES (%s, %s, %s, %s)"""
        self.cursor.execute(query, (reg, operator, mobile, float(amount)))
        self.conn.commit()

    # ---------- Get All Recharges ----------
    def getRecharges(self, regnumber):
        query = "SELECT * FROM recharges WHERE RegNumber = %s ORDER BY Date DESC"
        self.cursor.execute(query, (regnumber,))
        return self.cursor.fetchall()

    # ---------- Add Transaction ----------
    def addTransaction(self, reg, ttype, amount):
        query = """INSERT INTO transactions (RegNumber, Type, Amount)
                   VALUES (%s, %s, %s)"""
        self.cursor.execute(query, (reg, ttype, float(amount)))
        self.conn.commit()

    # ---------- Get All Transactions ----------
    def getTransactions(self, regnumber):
        query = """SELECT * FROM transactions 
                   WHERE RegNumber = %s ORDER BY Date DESC"""
        self.cursor.execute(query, (regnumber,))
        return self.cursor.fetchall()
