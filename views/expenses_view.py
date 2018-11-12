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
    pagination_spending_schema = PageOfSpendingSchema()
    pagination_spending_type_schema = PageOfSpendingTypeSchema()
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
        expenses_obj.total_month = data.get('total_month', None)
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

    @route('/spendings', methods=['POST'])
    def post_spendings(self):

        data = request.json
        spending_obj = Spending()
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

