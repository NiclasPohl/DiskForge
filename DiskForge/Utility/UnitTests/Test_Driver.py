import unittest

path_to_diskimage = "/home/niclas/asservat_74382-23.img"


# Nach Testing hat sich ergeben das md5 am schnellsten ist (wenn auch trotzdem 68 Sekunden braucht)
class TestStringMethods(unittest.TestCase):
    def test_string(self):
        self.assertEqual("FOO", "FOO")


if __name__ == '__main__':
    unittest.main
