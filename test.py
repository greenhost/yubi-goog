'''
    Unit tests for yubi_goog's.
'''

import unittest
import binascii
from yubi_goog import ytg_get_secret, ytg_setup, ytg_yubi


class TestYubiGoog(unittest.TestCase):
    '''
        Test TokenGenerator methods
    '''
    def setUp(self):
        self.secret = 'T7BNSOQ42E353N55T7BNSOQ42E353N55'
        self.secret_hex = '9fc2d93a1cd137ddb7bd9fc2d93a1cd137ddb7bd'
        self.secret_bin = binascii.unhexlify(self.secret_hex)

    def test_get_secret(self):
        '''
            Test secret conversion from Base32 to binary format (stored in hex
            format for convenience).
        '''
        self.assertEqual(
            self.secret_hex,
            binascii.hexlify(ytg_get_secret(self.secret))
        )

    def test_setup(self):
        '''
            Test that the setup function gives the correct secret for the
            Yubikey.
        '''
        hexlified = '9fc2d93a1cd137ddb7bd9fc2d93a1cd137ddb7bd'

        self.assertEqual(hexlified, ytg_setup(self.secret_bin))

if __name__ == '__main__':
    unittest.main()
