"""
User API endpoints for HBnB application
"""
from flask_restx import Namespace, Resource, fields
from hbnb.app.services.facade import HBnBFacade

api = Namespace('users', description='User operations')

# Create a facade instance
facade = HBnBFacade()

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user', min_length=1, max_length=50),
    'last_name': fields.String(required=True, description='Last name of the user', min_length=1, max_length=50),
    'email': fields.String(required=True, description='Email of the user'),
    'is_admin': fields.Boolean(description='Admin status', default=False),
    'password': fields.String(required=True, description='Password of the user')   #add password as input
})

# Define the user response model (without password)
user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email address'),
    'is_admin': fields.Boolean(description='Admin status'),
    'created_at': fields.DateTime(description='Creation date'),
    'updated_at': fields.DateTime(description='Last update date')
})


@api.route('/')
class UserList(Resource):
    """Handles operations on the user collection"""

    @api.doc('list_users')
    @api.marshal_list_with(user_response_model)
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Get list of all users"""
        users = facade.get_all_users()
        users_list = []
        for user in users:
            u = user.to_dict()
            u.pop('password', None)  # Remove password before returning
            users_list.append(u)
        return users_list, 200

    @api.doc('create_user')
    @api.expect(user_model, validate=True)
    @api.marshal_with(user_response_model, code=201)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(409, 'Email already registered')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        
        # Create user instance
        new_user = facade.create_user(user_data)

        # Hash the password before saving (inside User model or here)
        new_user.hash_password(user_data['password'])

        # Update user in repository after hashing
        facade.user_repo.update(new_user)

        # Prepare response without password
        user_dict = new_user.to_dict()
        user_dict.pop('password', None)
        return user_dict, 201


@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
class UserResource(Resource):
    """Handles operations on a single user"""

    @api.doc('get_user')
    @api.marshal_with(user_response_model)
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        # Remove password before returning
        user_dict = user.to_dict()
        user_dict.pop('password', None)
        return user_dict, 200

    @api.doc('update_user')
    @api.expect(user_model, validate=True)
    @api.marshal_with(user_response_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(409, 'Email already registered')
    def put(self, user_id):
        """Update user information"""
        user_data = api.payload

        # Check if user exists
        existing_user = facade.get_user(user_id)
        if not existing_user:
            api.abort(404, 'User not found')

        # Check if email is being changed to one that already exists
        if 'email' in user_data and user_data['email'] != existing_user.email:
            user_with_email = facade.get_user_by_email(user_data['email'])
            if user_with_email:
                api.abort(409, 'Email already registered')

        # Update user fields
        updated_user = facade.update_user(user_id, user_data)

        # Remove password before returning
        user_dict = updated_user.to_dict()
        user_dict.pop('password', None)
        return user_dict, 200
