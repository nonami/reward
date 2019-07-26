from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

from flask_sqlalchemy import SQLAlchemy

from reward_app.db import Voucher


class TestMark_as_used(TestCase):

    def setUp(self) -> None:
        pass

    @patch('reward_app.vouchermanager.fetch_voucher_by_code')
    def test_mark_as_used(self, fetch_voucher_by_code_mock):
        v = Voucher()
        fetch_voucher_by_code_mock.return_value = v

        from reward_app.vouchermanager import mark_as_used
        import reward_app.vouchermanager
        reward_app.vouchermanager.db = MagicMock()
        reward_app.vouchermanager.db.session.commit.return_value = None
        result = mark_as_used("")
        self.assertEqual(result, v)
        self.assertTrue(result.used)
        self.assertFalse(result.is_useable)
        self.assertTrue(fetch_voucher_by_code_mock.called)
