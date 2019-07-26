from unittest import TestCase
from unittest.mock import patch

from reward_app.db import VoucherType, Voucher


class TestFetch_voucher_by_code(TestCase):

    def setUp(self) -> None:
        pass

    @patch('reward_app.db.Voucher')
    def test_fetch_voucher_by_code(self, voucher_model):
        v = Voucher()
        voucher_model.query.filter_by.return_value.first.return_value = v

        from reward_app.vouchermanager import fetch_voucher_by_code
        r = fetch_voucher_by_code("")
        self.assertEqual(v, r)

    @patch('reward_app.db.Voucher')
    def test_fetch_voucher_by_code_fail(self, voucher_model):
        voucher_model.query.filter_by.return_value.first.return_value = None

        from reward_app.vouchermanager import fetch_voucher_by_code, InvalidVoucherError
        self.assertRaises(InvalidVoucherError, fetch_voucher_by_code, "")
