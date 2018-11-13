from flask_classy import FlaskView, route
from flask import jsonify, request
from sqlalchemy import extract
from schemas import SpendingSchema
from schemas import SpendingTypeSchema
from schemas import PageOfSpendingTypeSchema
from schemas import PageOfSpendingSchema
from schemas import PageOfExpensePartnershipSchema
from schemas import ExpensePartnershipSchema
from schemas import StatusExpensePaySchema
from schemas import PageOfStatusExpensePaySchema
import datetime

from model import SpendingType, Spending, ExpensePerProperty, ExpensePartnership, StatusExpensePay, Property, PropertyPerUser
from database import db
from werkzeug.exceptions import InternalServerError, Forbidden, BadRequest
from datetime import datetime


class ExpensesView(FlaskView):
    route_base = '/expenses'
    spending_schema = SpendingSchema()
    spending_types_schema = SpendingTypeSchema()
    expenses_schema = ExpensePartnershipSchema()
    expense_status_schema = StatusExpensePaySchema()
    pagination_spending_schema = PageOfSpendingSchema()
    pagination_spending_type_schema = PageOfSpendingTypeSchema()
    pagination_expenses_schema = PageOfExpensePartnershipSchema()
    pagination_expenses_status = PageOfStatusExpensePaySchema()

    def get(self):
        params = request.args
        page = params.get('page', 1)
        per_page = params.get('per_page', 10)
        id_expense = params.get('id', None)
        id_partnership = params.get('id_partnership', None)

        expenses = ExpensePartnership.query
        if not id_expense:
            expenses = expenses.order_by(ExpensePartnership.id.asc()).paginate(int(page), int(per_page),
                                                                               error_out=False)
            expenses_data = self.pagination_expenses_schema.dump(expenses).data

            return jsonify({'Expensas': expenses_data})
        else:
            expense = expenses.filter(ExpensePartnership.id == id_expense).first()
            expense_data = self.expenses_schema.dump(expense).data

            return jsonify({'Expensa': expense_data})

    def post(self):
        data = request.json
        expenses_obj = ExpensePartnership()
        id_partnership = data.get('id_partnership', None)
        expenses_obj.id_partnership = id_partnership
        expenses_obj.month = datetime.now().month
        expenses_obj.year = datetime.now().year
        expenses_obj.description = data.get('description', None)
        expenses_obj.since_date = '2018-11-01T00:00:09.243904+00:00'
        expenses_obj.until_date = '2018-11-30T23:59:00.243904+00:00'
        expenses_obj.generated_date = datetime.now()

        spending = Spending.query
        total_cost = 0
        spendings = spending.order_by(Spending.date.desc()).all()

        for spending in spendings:
            if spending.date.month == expenses_obj.month:
                total_cost = total_cost + spending.total_price

        expenses_obj.total_month = total_cost
        try:
            db.session.add(expenses_obj)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(str(e))
            raise InternalServerError('Unavailable to create new Expense')

        status_emitida = StatusExpensePay.query.filter(StatusExpensePay.name == "Emitida").first()

        properties = Property.query.filter(Property.id_partnership == id_partnership).all()

        expense_per_property = total_cost / len(properties)

        new_expense = ExpensePartnership.query.order_by(ExpensePartnership.id.desc()).first()

        for propertie in properties:
            relations = PropertyPerUser.query.filter(PropertyPerUser.id_property == propertie.id).all()
            for relation in relations:
                properti_data = ExpensePerProperty()
                properti_data.id_expense = new_expense.id
                properti_data.total_cost = expense_per_property
                properti_data.date_issue = new_expense.since_date
                properti_data.date_expiry = new_expense.until_date
                properti_data.id_status = status_emitida.id
                properti_data.id_prop_per_user = relation.id

                try:
                    db.session.add(properti_data)
                    db.session.commit()

                except Exception as e:
                    db.session.rollback()
                    print(str(e))
                    raise InternalServerError('Unavailable to create new ExpensePerProperty')

        new_expense = ExpensePartnership.query.order_by(ExpensePartnership.id.desc()).first()
        expense_data = self.expenses_schema.dump(new_expense).data

        expense_data = self.expenses_schema.dump(new_expense).data

        return jsonify({'Expense per partnership': expense_data})

    @route('/spendings', methods=['POST'])
    def post_spendings(self):

        data = request.json
        spending_obj = Spending()
        spending_obj.date = data.get('date', None)
        if not spending_obj.date:
            spending_obj.date = datetime.now()
        spending_obj.total_price = data.get('total_price', None)
        spending_obj.id_partnership = data.get('id_partnership', None)
        spending_obj.observation = data.get('observation', None)
        spending_obj.id_type = data.get('id_type', None)

        try:
            db.session.add(spending_obj)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(str(e))
            raise InternalServerError('Unavailable to create new Spending')

        new_spending = Spending.query.order_by(Spending.id.desc()).first()
        spending_data = self.spending_schema.dump(new_spending).data

        return jsonify({'Spending': spending_data})

    @route('/spendings', methods=['GET'])
    def get_spendings(self):
        params = request.args
        page = params.get('page', 1)
        per_page = params.get('per_page', 10)
        id_spending = params.get('id', None)
        id_partnership = params.get('id_partnership', None)

        spending = Spending.query
        if not id_spending:
            spendings = spending.order_by(Spending.id.asc()).paginate(int(page), int(per_page),
                                                                               error_out=False)
            spendings_data = self.pagination_spending_schema.dump(spendings).data

            return jsonify({'Spendings': spendings_data})
        else:
            spendings = spending.filter(Spending.id == id_spending).first()
            spending_data = self.spending_schema.dump(spendings).data

            return jsonify({'Spending': spending_data})

    @route('/spendings/types', methods=['POST'])
    def post_spendings_types(self):

        data = request.json
        spending_obj = SpendingType()
        spending_obj.name = data.get('name', None)

        try:
            db.session.add(spending_obj)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(str(e))
            raise InternalServerError('Unavailable to create new Type of Spending')

        new_type = SpendingType.query.order_by(SpendingType.id.desc()).first()
        type_data = self.spending_types_schema.dump(new_type).data

        return jsonify({'Type of Sepending': type_data})

    @route('/spendings/types', methods=['GET'])
    def get_spendings_types(self):
        params = request.args
        page = params.get('page', 1)
        per_page = params.get('per_page', 10)
        id_type = params.get('id', None)
        id_partnership = params.get('id_partnership', None)

        type_spending = SpendingType.query
        if not id_type:
            type_spending = type_spending.order_by(SpendingType.id.asc()).paginate(int(page), int(per_page),
                                                                               error_out=False)
            type_spending_data = self.pagination_spending_type_schema.dump(type_spending).data

            return jsonify({'Types of Spendings': type_spending_data})
        else:
            type_spending = type_spending.filter(SpendingType.id == id_type).first()
            type_spending_data = self.spending_types_schema.dump(type_spending).data

            return jsonify({'Type of Spendings': type_spending_data})

    @route('/status', methods=['POST'])
    def post_spendings_types(self):

        data = request.json
        expense_status_obj = StatusExpensePay()
        expense_status_obj.name = data.get('name', None)

        try:
            db.session.add(expense_status_obj)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(str(e))
            raise InternalServerError('Unavailable to create new Type of Spending')

        new_status = StatusExpensePay.query.order_by(StatusExpensePay.id.desc()).first()
        status_data = self.expense_status_schema.dump(new_status).data

        return jsonify({'Status of Pay Expenses': status_data})

    @route('/status', methods=['GET'])
    def get_spendings_types(self):
        params = request.args
        page = params.get('page', 1)
        per_page = params.get('per_page', 10)
        id_expense_status = params.get('id', None)
        id_partnership = params.get('id_partnership', None)

        expense_status = StatusExpensePay.query
        if not id_expense_status:
            expense_status = expense_status.order_by(StatusExpensePay.id.asc()).paginate(int(page), int(per_page),
                                                                                   error_out=False)
            expense_status_data = self.pagination_expenses_status.dump(expense_status).data

            return jsonify({'Status of Pay Expenses': expense_status_data})
        else:
            expense_status = expense_status.filter(StatusExpensePay.id == id_expense_status).first()
            expense_statu_data = self.spending_types_schema.dump(expense_status).data

            return jsonify({'Statu of Pay Expenses': expense_statu_data})
    #
    # def post_expenses_properties(self):
    #     return
