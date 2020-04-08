import unittest
import binascii
from scryptos import TLS

class TestTLS(unittest.TestCase):
  def setUp(s):
    pass

  def test_PMS(s):
    client_random = binascii.unhexlify("459c9c9b92a5415c282c8ef43ed0d6b283b648b5f6126a99d5dd67549416431a")
    server_random = binascii.unhexlify("5495d651289dbf15ba6eb6c68d37f8e3d8071ccc2a1dcb56d7cb634f95304d60")
    pre_master_secret = binascii.unhexlify("030379ada3f4f7cff7c114fa625abe9a4bbb457eda3f3f58838f116a01300f7d44886c8639e41c52024e12c31bb6d96f")
    master_secret = binascii.unhexlify("ae791f3deb5bf85d3e6b0b154a557e2882a6afc1d0fc60b82f42df601be82a7520fa88c14c37410ed1220e99b9eb7bcb")
    s.assertEqual(TLS.calc_master_secret_v1_v1_1("sha256", pre_master_secret, client_random, server_random), master_secret)
    client_random = binascii.unhexlify("7712ca85fcd84204104909836b7c92cec6094277f1c0efe885102d74a30b6dcc")
    server_random = binascii.unhexlify("63e2b53d65a8e860794ff15e90e7a369b179843f349b68df4b59d1ac53003735")
    pre_master_secret = binascii.unhexlify("8b39a3951e455666750834255ff25dbd78aabbf535a1f3bd39090c5980b4b49a2a7a8580f083b1a57e987d92e86027ccc14a8dd469fac7b7868249e55c41d29714a50d2c7f9275308271bea3231178113ccefac00e4499b53df6f24babfdb1d53c323dea995e43029bc743f5d1ef634f54820e3488ffaf7a203a1be29065d20e")
    master_secret = binascii.unhexlify("599dae45bea108da405cebfa1fd4414acccdc24ab4262c1c1e86af60da2de9712933343d3c6f92486db4bdbda9d693f8")
    s.assertEqual(TLS.calc_master_secret("sha256", pre_master_secret, client_random, server_random), master_secret)
