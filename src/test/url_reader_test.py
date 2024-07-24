from unittest import TestCase

import url_reader


class UrlReaderTests(TestCase):
    def test_read__returns_title(self):
        result = url_reader.read("https://open.spotify.com/track/02dphTJYUQ9pmdNC52iyOz")

        assert result[0] == "Fiesta Pagana"

    def test_read__returns_description(self):
        result = url_reader.read("https://open.spotify.com/track/02dphTJYUQ9pmdNC52iyOz")

        assert result[2] == "Mägo de Oz · Song · 2000"