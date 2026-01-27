"""Review API endpoints for HBnB application"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from hbnb.app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')

facade = HBnBFacade()

# Define the review model for input validation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text', min_length=1),
    'rating': fields.Integer(required=True, description='Rating (1-5)', min=1, max=5),
    'place_id': fields.String(required=True, description='Place ID being reviewed')
})

# Define the review response model
review_response_model = api.model('ReviewResponse', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating'),
    'user_id': fields.String(description='User ID'),
    'place_id': fields.String(description='Place ID'),
    'created_at': fields.String(description='Creation date'),
    'updated_at': fields.String(description='Last update date')
})


@api.route('/')
class ReviewList(Resource):
    """Handles operations on the review collection"""

    @api.doc('list_reviews')
    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Get list of all reviews"""
        reviews = facade.get_all_reviews()
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id,
                'created_at': review.created_at.isoformat() if hasattr(review.created_at, 'isoformat') else review.created_at,
                'updated_at': review.updated_at.isoformat() if hasattr(review.updated_at, 'isoformat') else review.updated_at
            }
            for review in reviews
        ], 200

    @api.doc('create_review')
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(404, 'User or Place not found')
    @jwt_required()
    def post(self):
        """Create a new review"""
        data = api.payload

        # Get user from JWT
        current_user_id = get_jwt_identity()
        data['user_id'] = current_user_id

        # Validate place exists
        place = facade.get_place(data['place_id'])
        if not place:
            api.abort(404, 'Place not found')

        new_review = facade.create_review(data)

        return {
            'id': new_review.id,
            'text': new_review.text,
            'rating': new_review.rating,
            'user_id': new_review.user_id,
            'place_id': new_review.place_id,
            'created_at': new_review.created_at.isoformat(),
            'updated_at': new_review.updated_at.isoformat()
        }, 201


@api.route('/<review_id>')
@api.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    """Handles operations on a single review"""

    @api.doc('get_review')
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')

        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id,
            'created_at': review.created_at.isoformat(),
            'updated_at': review.updated_at.isoformat()
            }, 200

    @api.doc('update_review')
    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update review information"""
        data = api.payload
        current_user_id = get_jwt_identity()

        if not data:
            api.abort(400, 'Request body is required')
            
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')

        if review.user_id != current_user_id:
            api.abort(403, 'Unauthorized action')

        updated_review = facade.update_review(review_id, data)

        return {
            'id': updated_review.id,
            'text': updated_review.text,
            'rating': updated_review.rating,
            'user_id': updated_review.user_id,
            'place_id': updated_review.place_id,
            'created_at': updated_review.created_at.isoformat(),
            'updated_at': updated_review.updated_at.isoformat()
        }, 200

    @api.doc('delete_review')
    @api.response(200, 'Review deleted successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user_id = get_jwt_identity()
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')

        if review.user_id != current_user_id:
            api.abort(403, 'Unauthorized action')

        facade.delete_review(review_id)
        return {}, 200
    

@api.route('/place/<place_id>/reviews')
@api.param('place_id', 'The place identifier')
class PlaceReviewList(Resource):
    """Handles operations for reviews of a specific place"""

    @api.doc('get_place_reviews')
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""

        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')

        reviews = facade.get_reviews_by_place(place_id)
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id,
                'created_at': review.created_at.isoformat(),
                'updated_at': review.updated_at.isoformat()
            }
            for review in reviews
        ], 200
