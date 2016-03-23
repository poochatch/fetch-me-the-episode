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


