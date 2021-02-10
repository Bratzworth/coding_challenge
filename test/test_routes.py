import json
import unittest

from app.routes import app

class TestApi(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_health(self):
        result = self.client.get('/health-check')
        self.assertEqual(str(result.data, "UTF-8"), "All Good!")

    def test_profile_bitbucket(self):
        # ideally at this point we would have a test bitbucket profile
        # i'm not going to do that for now, so we can just test with some public team
        result = self.client.get('/profile?bitbucket-team=mailchimp')
        self.assertDictEqual(json.loads(result.data), {'forks': 0, 'languages': {'dart': 1, 'javascript': 3, 'php': 2, 'python': 2, 'ruby': 2}, 'repos': 10, 'topics': {}, 'watchers': 386})
        
    def test_profile_github(self):
        # ideally at this point we would have a test github profile
        # i'm not going to do that for now, so we can just test with some public org
        result = self.client.get('/profile?github-org=mailchimp')
        self.assertDictEqual(json.loads(result.data), {'forks': 4, 'languages': {'css': 1, 'html': 1, 'java': 1, 'javascript': 3, 'kotlin': 1, 'none': 2, 'objective-c': 2, 'php': 8, 'python': 3, 'ruby': 6, 'swift': 1}, 'repos': 25, 'topics': {'android-sdk': 1, 'ecommerce': 2, 'email-marketing': 2, 'ios-sdk': 1, 'kotlin': 1, 'magento': 2, 'magento2': 1, 'mailchimp': 2, 'mailchimp-sdk': 2, 'php': 2, 'sdk': 2, 'sdk-android': 1, 'sdk-ios': 1, 'swift': 1}, 'watchers': 7959})
    
    def test_profile_both(self):
        # again we would ideally have a test github/bitbucket profile
        result = self.client.get('/profile?bitbucket-team=mailchimp&github-org=mailchimp')
        self.assertDictEqual(json.loads(result.data), {'forks': 4, 'languages': {'css': 1, 'dart': 1, 'html': 1, 'java': 1, 'javascript': 6, 'kotlin': 1, 'none': 2, 'objective-c': 2, 'php': 10, 'python': 5, 'ruby': 8, 'swift': 1}, 'repos': 35, 'topics': {'android-sdk': 1, 'ecommerce': 2, 'email-marketing': 2, 'ios-sdk': 1, 'kotlin': 1, 'magento': 2, 'magento2': 1, 'mailchimp': 2, 'mailchimp-sdk': 2, 'php': 2, 'sdk': 2, 'sdk-android': 1, 'sdk-ios': 1, 'swift': 1}, 'watchers': 8345})