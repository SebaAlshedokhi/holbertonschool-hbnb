"""Review API endpoints for HBnB application"""
from flask_restx import Namespace, Resource, fields
from flask import request
from hbnb.app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')

facade = HBnBFacade()

# Define the review model for input validation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text', min_length=1),
    'rating': fields.Integer(required=True, description='Rating (1-5)', min=1, max=5),
    'user_id': fields.String(required=True, description='User ID who wrote the review'),
    'place_id': fields.String(required=True, description='Place ID being reviewed')
})

# Define the review response model
review_response_model = api.model('ReviewResponse', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating'),
    'user_id': fields.String(description='User ID'),
    'place_id': fields.String(description='Place ID'),
    'user': fields.Nested(api.model('ReviewUser', {
        'id': fields.String(description='User ID'),
        'first_name': fields.String(description='User first name'),
        'last_name': fields.String(description='User last name')
    })),
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
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User or Place not found')
    def post(self):
        """Create a new review"""
        data = request.get_json()

        # Validate required fields
        if not data:
            api.abort(400, 'Request body is required')

        if 'text' not in data or not data.get('text'):
            api.abort(400, 'text is required and must be non-empty')

        if 'rating' not in data:
            api.abort(400, 'rating is required')

        try:
            rating = int(data['rating'])
            if rating < 1 or rating > 5:
                api.abort(400, 'rating must be between 1 and 5')
        except (ValueError, TypeError):
            api.abort(400, 'rating must be an integer between 1 and 5')

        if 'user_id' not in data or not data.get('user_id'):
            api.abort(400, 'user_id is required')

        if 'place_id' not in data or not data.get('place_id'):
            api.abort(400, 'place_id is required')

        # Validate user exists
        try:
            user = facade.get_user(data['user_id'])
            if not user:
                api.abort(404, 'User not found')
        except ValueError:
            api.abort(404, 'User not found')

        # Validate place exists
        try:
            place = facade.get_place(data['place_id'])
            if not place:
                api.abort(404, 'Place not found')
        except ValueError:
            api.abort(404, 'Place not found')

        try:
            new_review = facade.create_review(data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user_id,
                'place_id': new_review.place_id,
                'created_at': new_review.created_at.isoformat() if hasattr(new_review.created_at, 'isoformat') else new_review.created_at,
                'updated_at': new_review.updated_at.isoformat() if hasattr(new_review.updated_at, 'isoformat') else new_review.updated_at
            }, 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<review_id>')
@api.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    """Handles operations on a single review"""

    @api.doc('get_review')
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        try:
            review = facade.get_review(review_id)
            if not review:
                api.abort(404, 'Review not found')

            return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id,
                'created_at': review.created_at.isoformat() if hasattr(review.created_at, 'isoformat') else review.created_at,
                'updated_at': review.updated_at.isoformat() if hasattr(review.updated_at, 'isoformat') else review.updated_at
            }, 200
        except ValueError:
            api.abort(404, 'Review not found')

    @api.doc('update_review')
    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update review information"""
        data = request.get_json()

        if not data:
            api.abort(400, 'Request body is required')

        # Check if review exists
        try:
            existing_review = facade.get_review(review_id)
            if not existing_review:
                api.abort(404, 'Review not found')
        except ValueError:
            api.abort(404, 'Review not found')

        # Validate text if provided
        if 'text' in data and not data.get('text'):
            api.abort(400, 'text must be non-empty')

        # Validate rating if provided
        if 'rating' in data:
            try:
                rating = int(data['rating'])
                if rating < 1 or rating > 5:
                    api.abort(400, 'rating must be between 1 and 5')
            except (ValueError, TypeError):
                api.abort(400, 'rating must be an integer between 1 and 5')

        # Validate user if being updated
        if 'user_id' in data:
            try:
                user = facade.get_user(data['user_id'])
                if not user:
                    api.abort(404, 'User not found')
            except ValueError:
                api.abort(404, 'User not found')

        # Validate place if being updated
        if 'place_id' in data:
            try:
                place = facade.get_place(data['place_id'])
                if not place:
                    api.abort(404, 'Place not found')
            except ValueError:
                api.abort(404, 'Place not found')

        try:
            updated_review = facade.update_review(review_id, data)
            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user_id': updated_review.user_id,
                'place_id': updated_review.place_id,
                'created_at': updated_review.created_at.isoformat() if hasattr(updated_review.created_at, 'isoformat') else updated_review.created_at,
                'updated_at': updated_review.updated_at.isoformat() if hasattr(updated_review.updated_at, 'isoformat') else updated_review.updated_at
            }, 200
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('delete_review')
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        try:
            review = facade.get_review(review_id)
            if not review:
                api.abort(404, 'Review not found')

            facade.delete_review(review_id)
            return {}, 200
        except ValueError:
            api.abort(404, 'Review not found')


@api.route('/place/<place_id>/reviews')
@api.param('place_id', 'The place identifier')
class PlaceReviewList(Resource):
    """Handles operations for reviews of a specific place"""

    @api.doc('get_place_reviews')
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            place = facade.get_place(place_id)
            if not place:
                api.abort(404, 'Place not found')
        except ValueError:
            api.abort(404, 'Place not found')

        reviews = facade.get_reviews_by_place(place_id)
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
