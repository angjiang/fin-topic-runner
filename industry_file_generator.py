import os, codecs, fnmatch
import re

class industry_file_generator():
    """
    Generates an aggregated industry document for all filings by year
    """
    def __init__(self, input_dir, output_dir, years):
        """
        Constructor.
        Inputs:
            input_dir = the input directory for the crawled results
            output_dir = the directory to store industry level files
            years = the list of years of interest
        """
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.years = years

    def file_generator(self):
        """
        Aggregates firm text docs by year and outputs an aggregated year document
        """
        years = self.years
        input_dir = self.input_dir
        output_dir = self.output_dir

        for counter, yr in enumerate(years):
            yr_pattern = "*-" + yr + "-*"
            file_paths = [os.path.join(input_dir, fname) for fname in os.listdir(input_dir) if fnmatch.fnmatch(fname, yr_pattern)]
            print len(file_paths)
            counter = counter + 1

            yr_document = []

            for f in file_paths:
                document = codecs.open(f,'r', encoding="utf8", errors='ignore').readlines()
                yr_document.extend(document)
                print len(yr_document)

            with open(output_dir + yr + ".txt", "w") as handle:
                yr_string = ''.join(yr_document)
                handle.write(yr_string)
                print str(counter) + " " + yr
                print len(re.findall(r'\w+', yr_string))

if __name__ == '__main__':
    input_dir = '/crawler_results' # crawled results directory
    output_dir = '/industry_files' # output directory
    years = ['05','06','07','08','09','10','11','12','13','14','15'] # interested years

    test = industry_file_generator(input_dir, output_dir, years)
    test.file_generator()

