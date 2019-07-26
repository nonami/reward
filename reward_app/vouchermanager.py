from reward_app.db import VoucherType, Voucher, db
from datetime import datetime, timedelta
import time
import csv
from concurrent.futures import ThreadPoolExecutor
import string
import random
from flask import copy_current_request_context
from flask.logging import default_handler
import logging
from sqlalchemy.exc import IntegrityError

executor = ThreadPoolExecutor(10)
LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(default_handler)


class InvalidVoucherError(Exception):
    pass


def select_voucher_type(order_value, voucher_types):

    for voucher_type in voucher_types:
        upper_bound_cond = voucher_type.order_upper_bound == 0 or order_value < voucher_type.order_upper_bound
        if voucher_type.order_lower_bound <= order_value and upper_bound_cond:
            return voucher_type


def generate_voucher_code(customer_id):
    code = ''.join(random.choice(string.ascii_uppercase) for i in range(4))
    return code + str(customer_id).zfill(4)


def process_voucher_list(c_list):
    start_time = time.time()
    try:
        reader = csv.reader(c_list.splitlines())
        voucher_types = VoucherType.query.all()
        for row in reader:
            voucher_type = select_voucher_type(int(row[2]), voucher_types)
            if voucher_type is not None:
                try:
                    voucher = Voucher(customer_id=row[0],
                                      voucher_type=voucher_type,
                                      voucher_code=generate_voucher_code(row[0]),
                                      created_at=datetime.utcnow())
                    db.session.add(voucher)
                    db.session.commit()
                except IntegrityError:
                    db.session.rollback()
    except Exception as e:
        print(e)
    duration = time.time() - start_time
    LOGGER.info(f"Took {duration} seconds")


def start_voucher_job(customer_list):
    LOGGER.info(customer_list)
    # process_voucher_list(customer_list.decode('utf-8'))
    # Process list in background
    job = copy_current_request_context(process_voucher_list)
    executor.submit(job, customer_list.decode('utf-8'))
    return True


def activate_voucher(customer_id):
    voucher = Voucher.query.filter_by(customer_id=customer_id).first()
    if voucher is None or not voucher.is_useable:
        raise InvalidVoucherError()
    if not voucher.activated:
        voucher.activated = True
        voucher.expire_at = datetime.utcnow() + timedelta(days=voucher.voucher_type.validity)
        db.session.commit()
    return voucher


def fetch_voucher_by_code(code):
    voucher = Voucher.query.filter_by(voucher_code=code).first()
    if voucher is None:
        raise InvalidVoucherError()
    return voucher


def mark_as_used(code):
    voucher = fetch_voucher_by_code(code)
    voucher.used = True
    db.session.commit()
    return voucher
