from marshmallow import Schema, fields


class UserPermissionSchema(Schema):
    id_user_permission = fields.Integer()
    user_permission_arn = fields.String()


class UserReducedSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    name = fields.String()
    lastname = fields.String()
    active = fields.Boolean()
    email = fields.String()


class UserRoleSchema(Schema):
    id_user_role = fields.Integer()
    role_description = fields.String()
    active = fields.Boolean()
    is_super_role = fields.Boolean()
    permissions = fields.List(fields.Nested(UserPermissionSchema()))


class UserPositionSchema(Schema):
    id_user_position = fields.Integer()
    position_description = fields.String()
    active = fields.Boolean()


class UserStatusSchema(Schema):
    id_user_status = fields.Integer()
    status_description = fields.String()
    active = fields.Boolean()


class UserGroupSchema(Schema):
    id_user_group = fields.Integer()
    user_group_name = fields.String()
    user_group_description = fields.String()
    users = fields.List(fields.Nested(UserReducedSchema()))


class UserSchema(Schema):
    id_user = fields.Integer()
    user_username = fields.String()
    user_name = fields.String()
    user_lastname = fields.String()
    active = fields.Boolean()
    user_email = fields.String()
    user_profile_pic = fields.String()
    user_hired_date = fields.DateTime()
    user_birth_date = fields.DateTime()
    user_status = fields.Nested(UserStatusSchema())
    user_role = fields.List(fields.Nested(UserRoleSchema()))
    user_position = fields.Nested(UserPositionSchema())
    user_dni = fields.String()
    user_phone = fields.String()
    user_personal_message = fields.String()
    user_facebook = fields.String()
    user_sex = fields.String()
    user_groups = fields.List(fields.Nested(UserGroupSchema()))
    recognitions_count = fields.Integer()


class ClaimTypeSchema(Schema):
    id = fields.Integer()
    name = fields.String()


class ClaimStatusSchema(Schema):
    id = fields.Integer()
    name = fields.String()


class ClaimSchema(Schema):
    id = fields.Integer()
    category = fields.Nested(ClaimTypeSchema())
    title = fields.String()
    subject = fields.String()
    user_sender = fields.Nested(UserReducedSchema())
    user_reciver = fields.Nested(UserReducedSchema())
    id_property = fields.Integer()
    id_partnership = fields.Integer()
    date = fields.DateTime()
    status = fields.Nested(ClaimStatusSchema())
    date_end_claim = fields.DateTime()
    picture = fields.String()


class ClaimMessagesSchema(Schema):
    id = fields.Integer()
    id_partnership = fields.Integer()
    comment = fields.String()
    date = fields.DateTime()
    claim = fields.Nested(ClaimSchema())
    id_user_reciver = fields.Integer()
    id_user_sender = fields.Integer()


class NeighborhoodSchema(Schema):
    id_neighborhood = fields.Integer()
    name = fields.String()
    city = fields.String()


class PartnershipSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    address = fields.String()
    id_neighborhood = fields.Integer() #No funciona el Nested(NeigborhoodSchema())
    admin = fields.Nested(UserReducedSchema())


class PropertySchema(Schema):
    id = fields.Integer()
    id_partnership = fields.Integer() #No me funciona el .Nested(PartnershipSchema())
    floor = fields.Integer()
    ph = fields.String()
    block = fields.Integer()
    lot = fields.String()


class PaginationSchema(Schema):
    has_next = fields.Boolean()
    has_prev = fields.Boolean()
    next_num = fields.Integer()
    page = fields.Integer()
    pages = fields.Integer()
    per_page = fields.Integer()
    prev_num = fields.Integer()


class PropertyPerUserSchema(Schema):
    id = fields.Integer()
    id_user = fields.Integer()
    partner = fields.Integer() #No quiere funcionar ni con Integer, ni con Nested de partnership, ni con id_partnership
    id_relation = fields.Integer()
    property = fields.Nested(PropertySchema())


class RelationPropertyPerUserSchema(Schema):
    id = fields.Integer()
    name = fields.String()


class VisitorSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    lastname = fields.String()
    dni = fields.String()
    sex = fields.String()


class EventSchema(Schema):
    id = fields.Integer()
    id_partnership = fields.Integer()
    hour_since = fields.DateTime()
    hour_until = fields.DateTime()
    id_user = fields.Integer()


class VisitorPerEventSchema(Schema):
    id = fields.Integer()
    id_visitor = fields.Nested(VisitorSchema()) #No funciona el Nested de VisitorSchema()
    id_event = fields.Integer() #No funciona el Nested de EventSchema()


class PartnershipAdministratorSchema(Schema):
    id = fields.Integer()
    name = fields.String()

class SpendingTypeSchema(Schema):
    id = fields.Integer()
    name = fields.String()

class StatusExpensePaySchema(Schema):
    id = fields.Integer()
    name = fields.String()

class ExpensePartnershipSchema(Schema):
    id = fields.Integer()
    id_partnership = fields.Integer() #deberia ser un nested, pero ya me canse de probar partnership y q no funcione
    month = fields.String()
    description = fields.String()
    generated_date = fields.DateTime()
    total_month = fields.Float()

class SpendingSchema(Schema):
    id = fields.Integer()
    date = fields.DateTime()
    total_price = fields.Float()
    id_expense = fields.Integer() #deberia ser Nested
    observation = fields.String()
    id_type = fields.Integer() #deberia ser nested

class ExpensePerPropertySchema(Schema):
    id = fields.Integer()
    id_expense = fields.Integer() #deberia ser nested
    id_prop_per_user = fields.Integer() #deberia ser nested
    total_cost = fields.Float()
    date_issue = fields.DateTime()
    date_expiry = fields.DateTime()
    date_paid = fields.DateTime()
    observation = fields.String()
    id_status = fields.Integer() #deberia ser nested

class PageOfPartnershipAdministratorSchema(PaginationSchema):
    items = fields.List(fields.Nested(PartnershipAdministratorSchema()))


class PageOfClaimsSchema(PaginationSchema):
    items = fields.List(fields.Nested(ClaimSchema()))


class PageOfClaimsMessagesSchema(PaginationSchema):
    items = fields.List(fields.Nested(ClaimMessagesSchema()))


class PageOfUsersSchema(PaginationSchema):
    items = fields.List(fields.Nested(UserReducedSchema()))


class PageOfPartnershipSchema(PaginationSchema):
    items = fields.List(fields.Nested(PartnershipSchema()))


class PageOfPropertySchema(PaginationSchema):
    items = fields.List(fields.Nested(PropertySchema()))


class PageOfNeighborhoodSchema(PaginationSchema):
    items = fields.List(fields.Nested(NeighborhoodSchema()))


class PageOfPropertyPerUserSchema(PaginationSchema):
    items = fields.List(fields.Nested(PropertyPerUserSchema()))


class PageOfRelationPropertyPerUserSchema(PaginationSchema):
    items = fields.List(fields.Nested(RelationPropertyPerUserSchema()))


class PageOfVisitorSchema(PaginationSchema):
    items = fields.List(fields.Nested(VisitorSchema()))


class PageOfEventSchema(PaginationSchema):
    items = fields.List(fields.Nested(EventSchema()))


class PageOfVisitorPerEventSchema(PaginationSchema):
    items = fields.List(fields.Nested(VisitorPerEventSchema()))

class PageOfSpendingTypeSchema(PaginationSchema):
    items = fields.List(fields.Nested(SpendingTypeSchema()))

class PageOfStatusExpensePaySchema(PaginationSchema):
    items = fields.List(fields.Nested(StatusExpensePaySchema()))

class PageOfExpensePartnershipSchema(PaginationSchema):
    items = fields.List(fields.Nested(ExpensePartnershipSchema()))

class PageOfSpendingSchema(PaginationSchema):
    items = fields.List(fields.Nested(SpendingSchema()))

class PageOfExpensePerPropertySchema(PaginationSchema):
    items = fields.List(fields.Nested(ExpensePerPropertySchema()))