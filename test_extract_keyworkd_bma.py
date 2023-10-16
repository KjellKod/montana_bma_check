import unittest

from extract_keyword_bma import extract_urls_from_pdf   # replace 'your_module' with actual module name
from extract_keyword_bma import search_keywords_in_pdfs   # replace 'your_module' with actual module name




class TestPdfUrlExtractor(unittest.TestCase):
    def test_urls_extraction(self):
        '''
        Ensure that the urls returned by function 
        are matching the required pattern.
        '''
        original_pdf_filename = "test/region2maps2023.pdf" # a PDF file for testing
        res = extract_urls_from_pdf(original_pdf_filename)
        pdf_link_pattern = r'\d+_[\w\d_]+2023\.pdf'
        
        self.assertIsInstance(res, list, "Result should be a list")
        for url in res:
            filename = url.split('/')[-1]
            self.assertRegex(filename, pdf_link_pattern)

    def test_extract_urls_from_pdf(self):
        extracted_urls = extract_urls_from_pdf('test/region2maps2023.pdf')
        actual_count = len(extracted_urls)
        expected_count = 69
        self.assertEqual(actual_count, expected_count, 
                         f'The count of extracted URLs should be {expected_count} but got {actual_count}')

    def test_search_keywords_in_pdfs(self):
        files = ['region2maps2023.pdf']
        results = search_keywords_in_pdfs(["opportunities"], files, "test")
        expect_count = 1
        self.assertEqual(expect_count, len(results))
        self.assertEqual(results[0], "Keyword 'opportunities' found in 'region2maps2023.pdf' on page 1")


if __name__ == "__main__":
    unittest.main()
