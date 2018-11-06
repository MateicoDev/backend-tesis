from flask_classy import FlaskView, route
from flask import jsonify, request

from schemas import SpendingSchema
from schemas import SpendingTypeSchema
from schemas import PageOfSpendingTypeSchema
from schemas import PageOfSpendingSchema
from schemas import PageOfExpensePartnershipSchema
from schemas import ExpensePartnershipSchema

from model import SpendingType, Spending, ExpensePerProperty, ExpensePartnership
from database import db
from werkzeug.exceptions import InternalServerError, Forbidden, BadRequest
from datetime import datetime


class ExpensesView(FlaskView):
    route_base = '/expenses/'
    spending_schema = SpendingSchema()
    spending_types_schema = SpendingTypeSchema()
    expenses_schema = ExpensePartnershipSchema()
    pagination_spending_schema = PageOfSpendingTypeSchema()
    pagination_spending_type_schema = PageOfSpendingSchema()
    pagination_expenses_schema = PageOfExpensePartnershipSchema()

    def get(self):
        params = request.args
        page = params.get('page', 1)
        per_page = params.get('per_page', 10)
        idUser = params.get('id_user', None)

    def post(self):
        data = request.json
        expenses_obj = ExpensePartnership()
        expenses_obj.id_partnership = data.get('id_partnership', None)
        expenses_obj.total_cost = data.get('total_cost', None)
        expenses_obj.month = datetime.now().month
        expenses_obj.year = datetime.now().year
        expenses_obj.description = data.get('description', None)
        expenses_obj.since_date = data.get('since_date', None)
        expenses_obj.until_date = data.get('until_date', None)
        expenses_obj.generated_date = datetime.now()

        try:
            db.session.add(expenses_obj)
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            print(str(e))
            raise InternalServerError('Unavailable to create new Expense')

        new_expense = ExpensePerProperty.query.order_by(ExpensePerProperty.id.desc()).first()
        expense_data = self.expenses_schema.dump(new_expense).data

        return jsonify({'Expense per partnership': expense_data})
