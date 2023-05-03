from flask import jsonify, request
from flask.views import MethodView

from auth import check_password, hash_password, check_auth
from crud import create_item, delete_item, get_item, patch_item
from errors import HttpError
from models import Token, User, get_session_maker, Ads
from schema import PatchUser, Register, CreateAds, PatchAds, Login, validate


Session = get_session_maker()


def register():
    if not request.json:
        raise HttpError(400, 'request error')
    user_data = validate(Register, request.json)
    with Session() as session:
        user_data['password'] = hash_password(user_data['password'])
        user = create_item(session, User, **user_data)
        return jsonify({'id': user.id})


def login():
    if not request.json:
        raise HttpError(400, 'request error')
    login_data = validate(Login, request.json)
    with Session() as session:
        user = session.query(User).filter(User.email == login_data['email']).first()
        if user is None or not check_password(user.password, login_data['password']):
            raise HttpError(401, 'Invalid user or password')

        token = Token(user=user)
        session.add(token)
        session.commit()
        return jsonify({'token': token.id})


class UserView(MethodView):

    def get(self, user_id: int):
        with Session() as session:
            user = get_item(user_id, session)
            return jsonify(
                {
                    'id': user.id,
                    'email': user.email,
                    'creation_time': user.creation_time.isoformat() # преобразуем формат datetime в iso для вывода
                }
            )

    def patch(self, user_id: int):
        if not request.json:
            raise HttpError(400, 'request error')
        with Session() as session:
            patch_data = validate(PatchUser, request.json)
            if 'password' in patch_data:
                patch_data['password'] = hash_password(patch_data['password'])

            token = check_auth(session)
            user = get_item(session, User, user_id)
            if token.user_id != user.id:
                raise HttpError(403, 'user has no access')
            user = patch_item(session, user, **patch_data)

            return jsonify(
                {
                    'id': user.id,
                    'email': user.email,
                    'registration_time': user.registration_time.isoformat(),
                }
            )

    def delete(self, user_id: int):
        with Session() as session:
            user = get_item(session, User, user_id)
            token = check_auth(session)
            if token.user_id != user.id:
                raise HttpError(403, 'user has no access')

            delete_item(session, user)

            return jsonify({
                'status': 'deleted'
            })


class AdsView(MethodView):
    def post(self):
        if not request.json:
            raise HttpError(400, 'request error')
        with Session() as session:
            token = check_auth(session)
            ads_data = validate(CreateAds, request.json)
            ads_data['user'] = token.user
            ads = create_item(session, Ads, **ads_data)
            return jsonify(
                {
                    'id': ads.id,
                    'title': ads.title,
                    'description': ads.description,
                    'owner_id': ads.owner_id,
                })

    def get(self, advert_id: int):
        with Session() as session:
            ads = get_item(session, Ads, advert_id)
            return jsonify(
                {
                    'id': ads.id,
                    'title': ads.title,
                    'description': ads.description,
                    'owner_id': ads.owner_id,
                    'creation_time': ads.creation_time.isoformat(),
                }
            )

    def patch(self, advert_id: int):
        if not request.json:
            raise HttpError(400, 'request error')
        with Session() as session:
            patch_data = validate(PatchAds, request.json)
            token = check_auth(session)
            ads = get_item(session, Ads, advert_id)
            if token.user_id != ads.owner.id:
                raise HttpError(403, 'user has no access')
            ads = patch_item(session, ads, **patch_data)

            return jsonify(
                {
                    'id': ads.id,
                    'title': ads.title,
                    'description': ads.description,
                    'owner_id': ads.owner_id,
                    'creation_time': ads.creation_time.isoformat(),
                }
            )

    def delete(self, advert_id: int):
        with Session() as session:
            ads = get_item(session, Ads, advert_id)
            token = check_auth(session)
            if token.user_id != ads.owner.id:
                raise HttpError(403, 'user has no access')
            delete_item(session, ads)
            return jsonify({'deleted': True})
