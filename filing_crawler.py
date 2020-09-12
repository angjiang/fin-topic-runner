from urllib import urlopen
from bs4 import BeautifulSoup
import re

class filing_crawler:
    """
    Reads a CSV list of Edgar file locations and scrapes URLs to obtain 10K documents
    """
    def __init__(self, input_file, output_dir):
        """
        Constructor.

        Inputs:
            input_file must be a CSV with only one column containing Edgar file location
            output_dir is the directory to store the crawled results

        """
        self.input_file = input_file
        self.output_dir = output_dir

    def edgar_scrape(self):
        """
        Generates URLs, scrapes them, cleans and generates text from soup
        """
        with open(input_file, "r") as f:
            for counter, row in enumerate(f):
                html = urlopen("http://www.sec.gov/Archives/" + row).readlines()
                filename = ''.join(x.strip() for x in row.split('/')[-1])
                counter = counter +1

                # extracts the 10K from the full submission file
                total_filing = []
                copy = False
                for line in html:
                    if line.strip() == "<SEQUENCE>1":
                        copy = True
                    elif line.strip() == "</DOCUMENT>":
                        copy = False
                    elif copy:
                        total_filing.append(line)

                # make soup and remove tables
                total_filing = ' '.join([line.strip() for line in total_filing])
                total_filing_soup = BeautifulSoup(total_filing, "lxml")
                for element in total_filing_soup(["table"]):
                    element.decompose()

                # get text and remove non-text values
                total_filing_soup_text = total_filing_soup.get_text()
                total_filing_text = re.sub(r"[^a-zA-Z]", " ", total_filing_soup_text)

                # writes cleaned text to files in directory
                with open(output_dir + filename, "w") as handle:
                    handle.write(total_filing_text)
                    print str(counter) + " " + filename

if __name__ == '__main__':
    input_file = 'edgar.csv'
    output_dir = '/resultsDirectory'

    test = filing_crawler(input_file, output_dir)
    test.edgar_scrape()
