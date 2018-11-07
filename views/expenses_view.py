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
    route_base = '/expenses'
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

        new_expense = ExpensePartnership.query.order_by(ExpensePartnership.id.desc()).first()
        expense_data = self.expenses_schema.dump(new_expense).data

        return jsonify({'Expense per partnership': expense_data})
