from unittest import TestCase
import re

from reward_app.vouchermanager import generate_voucher_code


class TestGenerate_voucher_code(TestCase):
    def test_generate_voucher_code(self):
        self.assertRegex(generate_voucher_code(1), '[A-Z]{4}0{3}1')
        self.assertRegex(generate_voucher_code(23), '[A-Z]{4}0{2}23')
        self.assertRegex(generate_voucher_code(1400), '[A-Z]{4}1400')
        self.assertRegex(generate_voucher_code(170), '[A-Z]{4}0{1}170')
