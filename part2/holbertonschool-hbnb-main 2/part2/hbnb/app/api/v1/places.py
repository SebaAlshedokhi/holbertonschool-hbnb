from flask import request
from flask_restx import Namespace, Resource, fields
from hbnb.app.services import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'id': fields.String(readonly=True),
    'title': fields.String(required=True),
    'description': fields.String,
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.String(required=True),
    'amenities': fields.List(fields.String)
})


@api.route('/')
class PlaceList(Resource):

    def get(self):
        """Retrieve list of places (basic info only)"""
        places = facade.get_all_places()
        return [
            {
                'id': p.id,
                'title': p.title,
                'latitude': p.latitude,
                'longitude': p.longitude
            }
            for p in places
        ], 200

    @api.expect(place_model)
    def post(self):
        """Create a new place"""
        try:
            place = facade.create_place(request.json)
            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner_id': place.owner.id,
                'amenities': [a.id for a in place.amenities]
            }, 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<place_id>')
class PlaceResource(Resource):

    def get(self, place_id):
        """Retrieve a place by ID"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name
            },
            'amenities': [
                {'id': a.id, 'name': a.name}
                for a in place.amenities
            ]
        }, 200

    def put(self, place_id):
        """Update a place"""
        try:
            place = facade.update_place(place_id, request.json)
            return {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'updated_at': place.updated_at
            }, 200
        except ValueError as e:
            api.abort(400, str(e))
        except LookupError:
            api.abort(404, 'Place not found')
