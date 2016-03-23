#! /usr/bin/env python

# aport.app test suite

import unittest, requests

if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) ) 
        from app.aport_app import FileManagement, FetchInfo, FetchTorrent
    else:
        from  ..app.aport_app import FileManagement, FetchInfo, FetchTorrent 
        


class TestFileManagement(unittest.TestCase):
    def setUp(self):
        self.file_management = FileManagement('download_history.txt')

    def test_load_file_into_buffer_loads_open_file(self):
        self.file_management.load_file_into_buffer(self.file_management.file_name)
        self.assertEqual('r',self.file_management.file.mode)
        self.assertRaises(IOError, self.file_management.load_file_into_buffer, 'non_existing_file')
    
    def test_parse_closed_file(self):
        self.file_management.load_file_into_buffer(self.file_management.file_name)
        self.assertEqual(True, self.file_management.file.closed)

    def test_parse_has_read_file_into_buffer(self):
        self.assertIsInstance(self.file_management.buffer, list)
        self.assertNotEqual(len(self.file_management.buffer),0)

    def test_buffer_has_correct_data(self):
        prefixes = ('#',' ','\n','\r','\t')
        for line in self.file_management.buffer:
            self.assertIsInstance(line, list)
            self.assertEqual(len(line), 6)
            self.assertEqual(False, line[0].startswith(prefixes))
            for word in line:
                self.assertIsInstance(word , (unicode, str))
                self.assertNotEqual(0, len(word))
                self.assertEqual(False,word.startswith('#'))
                
                
    
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


    
class TestFetchTorrent(object):
    pass

if __name__ == '__main__':
    unittest.main()
