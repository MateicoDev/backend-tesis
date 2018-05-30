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
    id_user = fields.Integer()
    id_partnership = fields.Integer()
    comment = fields.String()
    date = fields.DateTime()
    claim = fields.Nested(ClaimSchema())


class PartnershipSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    address = fields.String()
    id_neighborhood = fields.Integer()
    admin = fields.Nested(UserReducedSchema())


class PaginationSchema(Schema):
    has_next = fields.Boolean()
    has_prev = fields.Boolean()
    next_num = fields.Integer()
    page = fields.Integer()
    pages = fields.Integer()
    per_page = fields.Integer()
    prev_num = fields.Integer()


class PageOfClaimsSchema(PaginationSchema):
    items = fields.List(fields.Nested(ClaimSchema()))


class PageOfClaimsMessagesSchema(PaginationSchema):
    items = fields.List(fields.Nested(ClaimMessagesSchema()))


class PageOfUsersSchema(PaginationSchema):
    items = fields.List(fields.Nested(UserReducedSchema()))


class PageofPartnershipSchema(PaginationSchema):
    items = fields.List(fields.Nested(PartnershipSchema()))




