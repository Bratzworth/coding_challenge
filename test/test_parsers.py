import random
import asyncio
import unittest
from collections import defaultdict

import app
from app import parsers


class TestParsers(unittest.TestCase):
    def test_get_requests(self):
        # ideally at this point we would stand up a local server to test this with
        # i'm not going to do that for now, so we can just test with some endpoint
        
        # test single request
        test = asyncio.run(parsers.get_request_json("https://api.bitbucket.org/2.0/repositories/pygame"))
        self.assertEqual(test, {"pagelen": 10, "values": [], "page": 1, "size": 0})
    
        # test using the async for multiple requests at the same time
        test_multiple = asyncio.run(parsers.get_multiple_json(["https://api.bitbucket.org/2.0/repositories/pygame"]))

        self.assertEqual(len(test_multiple), 1)
        self.assertEqual(test_multiple[0], {"pagelen": 10, "values": [], "page": 1, "size": 0})
    
    def test_parse_language(self):
        for test in ["", None]:
            self.assertEqual(parsers.parse_language(test), "none")
        
        for test in ["AAAA", "Python", "python"]:
            self.assertEqual(parsers.parse_language(test), test.lower())
    
    def test_parse_bitbucket(self):
        # test empty parse
        test_empty = parsers.parse_bitbucket(None)
        
        self.assertEqual(test_empty.repos, 0)
        self.assertEqual(test_empty.forks, 0)
        self.assertEqual(test_empty.watchers, 0)
        self.assertEqual(test_empty.languages, defaultdict(int, {}))
        self.assertEqual(test_empty.topics, defaultdict(int, {}))
        
        # ideally at this point we would have a test bitbucket profile
        # i'm not going to do that for now, so we can just test with some endpoint
        test = parsers.parse_bitbucket("mailchimp")
        
        self.assertEqual(test.repos, 10)
        self.assertEqual(test.forks, 0)
        self.assertEqual(test.watchers, 386)
        self.assertDictEqual(dict(test.languages), {"dart": 1, "javascript": 3, "php": 2, "python": 2, "ruby": 2})
        self.assertEqual(test.topics, defaultdict(int, {}))
        
    def test_parse_github(self):
        # test empty parse
        test_empty = parsers.parse_github(None)
        
        self.assertEqual(test_empty.repos, 0)
        self.assertEqual(test_empty.forks, 0)
        self.assertEqual(test_empty.watchers, 0)
        self.assertEqual(test_empty.languages, defaultdict(int, {}))
        self.assertEqual(test_empty.topics, defaultdict(int, {}))
        
        # ideally at this point we would have a test github profile
        # i'm not going to do that for now, so we can just test with some public endpoint 
        test = parsers.parse_github("pygame")
        
        self.assertEqual(test.repos, 6)
        self.assertEqual(test.forks, 3)
        self.assertEqual(test.watchers, 3237)
        self.assertDictEqual(dict(test.languages), {"c": 1, "python": 7, "ruby": 1})
        self.assertDictEqual(dict(test.topics), {"flask": 1, "game-dev": 1, "game-development": 1, "gamedev": 1,
                                                 "pygame": 2, "python": 2, "sdl": 1, "sdl2": 1, "sqlalchemy": 1})