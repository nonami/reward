from reward_app import vouchermanager, authmanager
from flask import jsonify, Blueprint, request
from functools import wraps


bp = Blueprint('vouchers', __name__, url_prefix='/vouchers')


def authenticate():
    message = {'message': "Authenticate."}
    resp = jsonify(message)

    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'

    return resp


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()

        elif not authmanager.check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


@bp.errorhandler(vouchermanager.InvalidVoucherError)
def bad_request(error):
    message = {
            'message': 'Bad request',
    }
    resp = jsonify(message)
    resp.status_code = 400

    return resp


# routes
@bp.route('', methods=('POST',))
def create_vouchers():
    vouchermanager.start_voucher_job(request.data)
    return jsonify({'message': 'List queued for processing'})


@bp.route('/<int:customer_id>/customer-id', methods=('PUT',))
@requires_auth
def activate_voucher(customer_id):
    return jsonify(vouchermanager.activate_voucher(customer_id).to_dict())


@bp.route('/<code>', methods=('GET',))
@requires_auth
def fetch_customer_voucher(code):
    return jsonify(vouchermanager.fetch_voucher_by_code(code).to_dict())


@bp.route('/<code>', methods=('PUT',))
@requires_auth
def mark_voucher_as_used(code):
    return jsonify(vouchermanager.mark_as_used(code).to_dict())
