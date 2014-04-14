import unittest

from mock import MagicMock

from frodo_base import FrodoBase


class ConcreteFrodoBase(FrodoBase):
    required_attr = ('attr1', 'attr2')


# noinspection PyProtectedMember
class TestFrodoBase(unittest.TestCase):
    def setUp(self):
        pass

    def test_init(self):
        configuration = MagicMock()
        aname = 'aname'
        concrete = ConcreteFrodoBase(aname, configuration, test=5)
        self.assertEqual(concrete.configuration, configuration)
        self.assertEqual(concrete.name, aname)
        self.assertDictEqual({'test': 5}, concrete._kwargs)

    def test_validate_when_all_missing(self):
        configuration = MagicMock()
        aname = 'aname'
        concrete = ConcreteFrodoBase(aname, configuration)
        errors = concrete.validate()
        self.assertEqual(2, len(errors))
        self.assertSetEqual(set(errors.keys()), set(ConcreteFrodoBase.required_attr))

    def test_validate_when_one_missing(self):
        configuration = MagicMock()
        aname = 'aname'
        concrete = ConcreteFrodoBase(aname, configuration, attr1=5)
        errors = concrete.validate()
        self.assertEqual(1, len(errors))
        self.assertSetEqual(set(errors.keys()), set(ConcreteFrodoBase.required_attr) - {'attr1'})

    def test_validate_when_none_missing(self):
        configuration = MagicMock()
        aname = 'aname'
        concrete = ConcreteFrodoBase(aname, configuration, attr1=5, attr2=6)
        errors = concrete.validate()
        self.assertFalse(errors)

    def test_as_dict(self):
        configuration = MagicMock()
        aname = 'aname'
        concrete = ConcreteFrodoBase(aname, configuration, attr1=5, attr2=6)
        self.assertDictEqual({'attr1': 5, 'attr2': 6}, concrete.as_dict())