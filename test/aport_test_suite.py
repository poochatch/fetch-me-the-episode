#! /usr/bin/env python

# aport.app test suite

import unittest, requests

if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) ) 
        from app.fetchinfo import FetchInfo
        from app.fetchtorrent import FetchTorrent
        from app.db import HandleDataBase, Shows, DownloadedEpisodes
    else:
        from app.fetchinfo import FetchInfo
        from app.fetchtorrent import FetchTorrent
        from app.db import HandleDataBase, Shows, DownloadedEpisodes
        
class TestHandleDataBase(unittest.TestCase):

    def setUp(self):
        self.db = HandleDataBase()

    def test_get_enty_by_field_returns_db_entry(self):
        entry = self.db.get_entry_by_field('The Vikings','title')
        self.assertIsInstance(entry, Shows)

    def test_get_enty_by_field_raises_exception(self):
        self.assertRaises(ValueError, self.db.get_entry_by_field, 'non-existant-entry', 'title')
        self.assertRaises(ValueError, self.db.get_entry_by_field, 'The Vikings', 'non-existant-field')
    
    def test_get_matching_entries_returns_list_of_db_entries(self):
        rows = self.db.get_matching_entries('The Vikings','title')
        self.assertIsInstance(rows, list)
        self.assertNotEqual(0, len(rows))
        for entry in rows:
            self.assertIsInstance(entry, Shows)

    def test_get_matching_entries_raises_for_wrong_query(self):
        self.assertRaises(ValueError, self.db.get_matching_entries, 'non-existant-entry','title')
        self.assertRaises(ValueError, self.db.get_matching_entries, 'The Vikings','non-existant-field')

    def test_find_exact_title_finds_the_title(self):
        test_cases = ['vikings', 'the vikings', ' The    Vikings ',\
                     'The Vikings ', ' the vikings ', 'thevikings',\
                     '#@!the vikings@@! @ @! @! ', 'The vikings' \
                       '"the vikings"' ]
        for test_case in test_cases:
            query = self.db.find_exact_title(test_case)
            self.assertEqual(query.id, 1)

    def test_get_last_download_details_returns_episode_entry(self):
        entry = self.db.get_entry_by_field('The Vikings', 'title')
        for episode in entry.downloaded_episodes:
            self.assertIsInstance(episode, DownloadedEpisodes)
            

    def test_get_last_download_details_returns_correct_entry(self):
        pass

    def test_get_show_url_returns_correct_url_and_raises_if_no_entry_or_wrong_argument(self):
        url = self.db.get_show_url('The Vikings')
        self.assertIsNotEqual(0, len(url))
        self.assertIsEqual(True, url.startswith('/'))
        self.assertRaises(ValueError, self.db.get_show_url, 'non-existant-entry')
        self.assertRaises(ValueError, self.db.get_show_url, 'The Vikings','invalid-url-or-wrong-argument')

    def test_get_all_episodes_returns_list_of_db_entries(self):
        rows = self.db.get_all_episodes_of_show('The Vikings')
        self.assertIsInstance(rows, list)
        self.assertNotEqual(0, len(rows))
        for entry in rows:
            self.assertIsInstance(entry, Shows)
            self.assertEqual(entry.id, 1)

    def test_add_show_raises_for_invalid_entry(self):
        test_cases = [' Breaking Bad', 'breaking    bad   ',\
                     'Breaking*Bad', 'breaking_bad','"breaking bad"', 2, True, ['/breaking bad']]
        test_cases_ = ['breakingbad',' /breaking-bad', '# breaking bad', 'breaking bad',123, False, (0,0)]
        for test_case in test_cases:
            for test_case_ in test_cases_:
                self.assertRaises(self.db.add_show(test_case, test_case_)

    def test_update_session(self):
        # how?
        pass

        

class TestFetchInfo(unittest.TestCase):
    series = ['vikings', 'the-walking-dead'] # list of valid url from next-episode.net
    titles = ['the vikings', 'vikings', 'walking dead', 'the walking dead']

    def setUp(self):
        self.fetch = FetchInfo()

    def test_parse_lenght_is_6(self):
        pass    

    def test_parse_returns_string(self):
        pass

    def test_parse_returns_string_with_only_s_and_e_letters_present(self):
        pass

    def test_fech_raises_404(self):
        self.assertRaises(requests.exceptions.HTTPError, self.fetch.fetch,'http://google.com/non-existent-url')

    def test_fetch_returns_response_obj(self):
        for title in self.series:
            self.assertIsInstance(self.fetch.fetch(title), requests.models.Response)

    def test_resolve_url_returns_string(self):
        for title in self.titles:
            self.assertIsInstance(self.fetch.resolve_url(title), (str,unicode))
    def test_resolve_url_finds_correct_title(self):
        pass    


    def test_get_field(self):
        pass
    


    def test_reads_last_watched_raises_for_no_file(self):
        pass

    def test_not_watched_returns_list_of_apropriate_length(self):
        pass

    def test_read_top_watched_returns_list_of_urls(self):
        top = self.fetch.get_top_watched()
        self.assertIsInstance(top, list)
        for title in top:
            self.assertIsInstance(title,tuple)
            self.assertIsInstance(title[1],(str,unicode))
    
class TestFetchTorrent(object):
    pass

if __name__ == '__main__':
    unittest.main()
