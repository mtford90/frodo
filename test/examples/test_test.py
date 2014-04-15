import os
import unittest


class TestExampleSpec(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ['FRODO_CONF'] = 'spec.yaml'
        cls.conf = __import__('configuration')

    @classmethod
    def tearDownClass(cls):
        os.unsetenv('FRODO_CONF')



    # def test_test_as_dict(self):
    #     test = self.conf.tests['mytest']
    #     d = test.as_dict()
    #     self.assertDictEqual({
    #                              'target': 'Unit Tests',
    #                              'test_case': 'InviteFriendsToAlbumDataSourceTestCase',
    #                              'env': self.conf.environs['myenv'],
    #                              'config': self.conf.configs['myconfig'],
    #                              'preconditions': [self.conf.preconditions['myprecond']]
    #                          }, d)
    #
    # def test_only(self):
    #     test = self.conf.tests['mytest']
    #     only = test._construct_only()
    #     self.assertEqual(only, '%s:%s' % (test.target, test.test_case))
    #
    # def test_run(self):
    #     test = self.conf.tests['mytest']
    #     test.run()
    #     self.assertTrue(test.has_run)
    #     self.assertEqual(len(test.relevant), 4)