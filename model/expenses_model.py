from database import db

class SpendingType(db.Model):
    __tablename__ = 'spending_type'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __init__(self, name=None):
        self.name = name

class StatusExpensePay(db.Model):
    __tablename__ = 'status_expense_pay'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def __init__(self, name=None):
        self.name = name

class ExpensePartnership(db.Model):
    __tablename__ = 'expense_partnership'
    id = db.Column(db.Integer, primary_key=True)
    id_partnership = db.Column(db.Integer, db.ForeignKey('partnership.id'))
    partnership = db.relationship('Partnership', foreign_keys=[id_partnership], cascade="merge")
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(500), nullable=True)
    since_date = db.Column(db.DateTime, nullable=False)
    until_date = db.Column(db.DateTime, nullable=False)
    generated_date = db.Column(db.DateTime, nullable=True)
    total_month = db.Column(db.Float, nullable=True)
    active = db.Column(db.Float, nullable=True) #Dependiente del until_date

    def __init__(self, id_partnership=None, month=None, year=None, description=None,
                 since_date=None, until_date=None, generated_date=None, total_month=None, active=None):
        self.id_partnership = id_partnership
        self.month = month
        self.year = year
        self.description = description
        self.since_date = since_date
        self.until_date = until_date
        self.generated_date = generated_date
        self.total_month = total_month
        self.active = active

class Spending(db.Model):
    __tablename__ = 'spending'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable = False)
    total_price = db.Column(db.Float, nullable = False)
    id_partnership = db.Column(db.Integer, db.ForeignKey('partnership.id'))
    partnership = db.relationship('Partnership', foreign_keys=[id_partnership], cascade="merge")
    observation = db.Column(db.String, nullable=True)
    bill_picture = db.Column(db.String, nullable=True)
    id_type = db.Column(db.Integer, db.ForeignKey('spending_type.id'))
    type = db.relationship('SpendingType', foreign_keys=[id_type], cascade="merge")

    def __init__(self, date=None, total_price=None, id_partnership=None, observation=None,
                 bill_picture=None, id_type=None):
        self.date = date
        self.total_price = total_price
        self.id_partnership = id_partnership
        self.observation = observation
        self.bill_picture = bill_picture
        self.id_type = id_type

class ExpensePerProperty(db.Model):
    __tablename__ = 'expense_per_property'
    id = db.Column(db.Integer, primary_key=True)
    id_expense = db.Column(db.Integer, db.ForeignKey('expense_partnership.id'))
    expense = db.relationship('ExpensePartnership', foreign_keys=[id_expense], cascade="merge")
    id_prop_per_user = db.Column(db.Integer, db.ForeignKey('property_per_user.id'))
    prop_per_user = db.relationship('PropertyPerUser', foreign_keys=[id_prop_per_user], cascade="merge")
    total_cost = db.Column(db.Float, nullable=False)
    date_issue = db.Column(db.DateTime, nullable=False)
    date_expiry = db.Column(db.DateTime, nullable=False)
    date_paid = db.Column(db.DateTime, nullable=True)
    observation = db.Column(db.String, nullable=True)
    id_status = db.Column(db.Integer, db.ForeignKey('status_expense_pay.id'))
    status = db.relationship('StatusExpensePay', foreign_keys=[id_status], cascade="merge")
