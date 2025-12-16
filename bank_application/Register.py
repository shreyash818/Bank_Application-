class Register:
    def __init__(self, regnumber, firstname, lastname, password, accbal):
        self.regnumber = regnumber
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.accbal = accbal


    # RegNumber
    @property
    def regnumber(self):
        return self._regnumber

    @regnumber.setter
    def regnumber(self, value):
        self._regnumber = value

    # FirstName
    @property
    def firstname(self):
        return self._firstname

    @firstname.setter
    def firstname(self, value):
        self._firstname = value

    # LastName
    @property
    def lastname(self):
        return self._lastname

    @lastname.setter
    def lastname(self, value):
        self._lastname = value

    # Password
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    # Account Balance
    @property
    def accbal(self):
        return self._accbal

    @accbal.setter
    def accbal(self, value):
        self._accbal = value