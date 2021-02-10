import json
import random
import unittest
from collections import defaultdict

import app
from app import profile

class TestOrganizationProfile(unittest.TestCase):
    def test_init_empty(self):
        test = profile.OrganizationProfile()
        
        self.assertEqual(test.repos, 0)
        self.assertEqual(test.forks, 0)
        self.assertEqual(test.watchers, 0)
        self.assertEqual(test.languages, defaultdict(int, {}))
        self.assertEqual(test.topics, defaultdict(int, {}))
    
    def test_init_filled(self):
        repos = random.randint(0, 10)
        forks = random.randint(0, 10)
        watchers = random.randint(0, 10)
        
        language_options = ["python", "java", "objective-c", "c++", "swift", "php"]
        languages = {random.choice(language_options): random.randint(0,10)}
        
        topic_options = ["test", "test2", "topic"]
        topics = {random.choice(topic_options): random.randint(0,10)}

        test = profile.OrganizationProfile(repos = repos, forks = forks, watchers = watchers, languages = languages, topics = topics)
        
        self.assertEqual(test.repos, repos)
        self.assertEqual(test.forks, forks)
        self.assertEqual(test.watchers, watchers)
        self.assertDictEqual(dict(test.languages), languages)
        self.assertDictEqual(dict(test.topics), topics)
    
    def test_add_both_empty(self):
        empty_1 = profile.OrganizationProfile()
        empty_2 = profile.OrganizationProfile()
        test = empty_1 + empty_2
        
        self.assertEqual(test.repos, 0)
        self.assertEqual(test.forks, 0)
        self.assertEqual(test.watchers, 0)
        self.assertEqual(test.languages, defaultdict(int, {}))
        self.assertEqual(test.topics, defaultdict(int, {}))
    
    def test_add_empty_to_filled(self):
        repos = random.randint(0, 10)
        forks = random.randint(0, 10)
        watchers = random.randint(0, 10)
        
        language_options = ["python", "java", "objective-c", "c++", "swift", "php"]
        languages = {random.choice(language_options): random.randint(0,10)}
        
        topic_options = ["test", "test2", "topic"]
        topics = {random.choice(topic_options): random.randint(0,10)}

        filled = profile.OrganizationProfile(repos = repos, forks = forks, watchers = watchers, languages = languages, topics = topics)
        empty = profile.OrganizationProfile()

        test_1 = filled + empty
        self.assertEqual(test_1.repos, repos)
        self.assertEqual(test_1.forks, forks)
        self.assertEqual(test_1.watchers, watchers)
        self.assertDictEqual(dict(test_1.languages), languages)
        self.assertDictEqual(dict(test_1.topics), topics)
        
        test_2 = empty + filled
        self.assertEqual(test_2.repos, repos)
        self.assertEqual(test_2.forks, forks)
        self.assertEqual(test_2.watchers, watchers)
        self.assertDictEqual(dict(test_2.languages), languages)
        self.assertDictEqual(dict(test_2.topics), topics)
        
    def test_add_both_filled(self):
        language_options = ["python", "java", "objective-c", "c++", "swift", "php"]
        topic_options = ["test", "test2", "topic"]

        repos_1 = random.randint(0, 10)
        forks_1 = random.randint(0, 10)
        watchers_1 = random.randint(0, 10)
        languages_1 = {random.choice(language_options): random.randint(0,10)}
        topics_1 = {random.choice(topic_options): random.randint(0,10)}

        repos_2 = random.randint(0, 10)
        forks_2 = random.randint(0, 10)
        watchers_2 = random.randint(0, 10)
        languages_2 = {random.choice(language_options): random.randint(0,10)}
        topics_2 = {random.choice(topic_options): random.randint(0,10)}

        repos_gold = repos_1 + repos_2
        forks_gold = forks_1 + forks_2
        watchers_gold = watchers_1 + watchers_2
        
        # languages_gold should have both dictionaries merged with their values added together
        languages_gold = defaultdict(int)
        for language, count in languages_1.items():
            languages_gold[language] += count
        for language, count in languages_2.items():
            languages_gold[language] += count
        
        # topics_gold should have both dictionaries merged with their values added together
        topics_gold = defaultdict(int)
        for topic, count in topics_1.items():
            topics_gold[topic] += count
        for topic, count in topics_2.items():
            topics_gold[topic] += count

        filled_1 = profile.OrganizationProfile(repos = repos_1, forks = forks_1, watchers = watchers_1, languages = languages_1, topics = topics_1)
        filled_2 = profile.OrganizationProfile(repos = repos_2, forks = forks_2, watchers = watchers_2, languages = languages_2, topics = topics_2)

        test_1 = filled_1 + filled_2
        self.assertEqual(test_1.repos, repos_gold)
        self.assertEqual(test_1.forks, forks_gold)
        self.assertEqual(test_1.watchers, watchers_gold)
        self.assertDictEqual(test_1.languages, languages_gold)
        self.assertDictEqual(test_1.topics, topics_gold)
        
        test_2 = filled_2 + filled_1
        self.assertEqual(test_2.repos, repos_gold)
        self.assertEqual(test_2.forks, forks_gold)
        self.assertEqual(test_2.watchers, watchers_gold)
        self.assertDictEqual(test_2.languages, languages_gold)
        self.assertDictEqual(test_2.topics, topics_gold)
        
    def test_dict(self):
        repos = random.randint(0, 10)
        forks = random.randint(0, 10)
        watchers = random.randint(0, 10)
        
        language_options = ["python", "java", "objective-c", "c++", "swift", "php"]
        languages = {random.choice(language_options): random.randint(0,10)}
        
        topic_options = ["test", "test2", "topic"]
        topics = {random.choice(topic_options): random.randint(0,10)}

        test = profile.OrganizationProfile(repos = repos, forks = forks, watchers = watchers, languages = languages, topics = topics)
        
        test_dict = test.dict()
        
        self.assertEqual(test_dict, {"repos": repos, "forks": forks, "watchers": watchers, "languages": languages, "topics": topics})
