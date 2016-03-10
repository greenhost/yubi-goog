'''
    Unit tests for yubi_goog's.
'''

import unittest
import binascii
from yubi_goog import TokenGenerator


class TestTokenGenerator(unittest.TestCase):
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
        ytg = TokenGenerator()
        self.assertEqual(
            self.secret_hex,
            binascii.hexlify(ytg.get_secret(self.secret))
        )

    def test_setup(self):
        '''
            Test that the setup function gives the correct secret for the
            Yubikey.
        '''
        ytg = TokenGenerator()
        hexlified = '9fc2d93a1cd137ddb7bd9fc2d93a1cd137ddb7bd'

        self.assertEqual(hexlified, ytg.setup(self.secret_bin))

    def test_generate_challenge(self):
        '''
            Test that the generate_challenge function gives the correct
            challenge give a fixed point in time.
        '''
        ytg = TokenGenerator()
        self.assertEqual(
            binascii.unhexlify('0000000002e56192'),
            ytg.generate_challenge(1457614623.53)
        )

    def test_totp(self):
        '''
            Check that 3 tokens are generated correctly given a secret and a
            fixed point in time.
        '''

        test_vectors = [
            {'time': 1111111111, 'otp': '756232'},
            {'time': 1234567890, 'otp': '042878'},
            {'time': 2000000000, 'otp': '990159'}
        ]
        ytg = TokenGenerator()
        for pair in test_vectors:
            flttime = pair['time']
            real_otp = pair['otp']

            chal = ytg.generate_challenge(flttime)

            self.assertEqual(real_otp, ytg.totp(self.secret, chal))

if __name__ == '__main__':
    unittest.main()
