from unittest import TestCase

from reward_app.db import VoucherType
from reward_app.vouchermanager import select_voucher_type


class TestSelect_voucher_type(TestCase):
    def test_select_voucher_type(self):
        v_types = []
        n = 3
        for i in range(n):
            v_types.append(VoucherType(
                order_lower_bound=i * 1000,
                order_upper_bound=(i + 1) * 1000 if i < n - 1 else 0
            ))

        print(select_voucher_type(100, v_types))
        self.assertEqual(select_voucher_type(100, v_types), v_types[0])
        self.assertEqual(select_voucher_type(1000, v_types), v_types[1])
        self.assertEqual(select_voucher_type(2500, v_types), v_types[2])
        self.assertEqual(select_voucher_type(400000, v_types), v_types[2])
        self.assertEqual(select_voucher_type(1999, v_types), v_types[1])
        self.assertIsNone(select_voucher_type(-20, v_types))

