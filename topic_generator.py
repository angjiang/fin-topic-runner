import os, codecs, fnmatch
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS
import lda
import numpy as np
import pandas as pd
import csv

class topic_generator():
    """
    Generates firm level or industry level topics from relevant filings
    - to generate firm-level topics, aggregate filings for a given firm across the relevant time scale
    - to generate industry-level topics, aggregate filings for the firms within the industry index for a given year
    """
    def __init__(self, input_dir, fin_stopwords_file, output_file, n_topics, n_top_words):
        """
        Constructor.

        Inputs:
        input_dir is the directory of relevant filings.
        fin_stopwords_file is the file for the appended stopwords
        output_file is the specified CSV
        n_topics is the number of topics to be modeled
        n_top_words is the number of top words per topic to be retrieved and written
        fyear is the year of interest
        :return:
        """
        self.input_dir = input_dir
        self.fin_stopwords = fin_stopwords
        self.output_file = output_file
        self.n_topics = n_topics
        self.n_top_words = n_top_words
        #self.fyear = fyear

    def stopwords(self):
        fin_stopwords = []
        with open(fin_stopwords,"rb") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                fin_stopwords.extend(row)

        stopwords = ENGLISH_STOP_WORDS.union(fin_stopwords)
        self.stopwords = stopwords

    def file_manager(self):
        """
        Manages the text document processing batches
        :return:
        """
        #fyear = self.fyear
        #yr_pattern = "*-" + fyear + "-*"

        file_paths = [os.path.join(input_dir, fname) for fname in os.listdir(input_dir)]
        self.file_paths = file_paths

    def lda_modeler(self):
        """
        Generates topics from LDA
        :return:
        """
        file_paths = self.file_paths
        stopwords = self.stopwords

        # set up LDA model
        model = lda.LDA(n_topics=n_topics, n_iter=500, random_state=1)

        for counter, f in enumerate(file_paths):
            document = codecs.open(f,'r', encoding="utf8", errors='ignore').readlines()
            filename = ''.join(x.strip() for x in f.split('/')[-1])
            counter = counter + 1

            # create document-term matrix
            count_df = CountVectorizer(stop_words=stopwords, analyzer='word', lowercase=True, strip_accents="unicode")
            A = count_df.fit_transform(document)

            # store values of dtm
            num_terms = len(count_df.vocabulary_)
            terms = num_terms * [""]
            for term in count_df.vocabulary_.keys():
                terms[ count_df.vocabulary_[term] ] = term

            # apply LDA model
            model.fit(A)
            topic_word = model.topic_word_
            doc_topic = model.doc_topic_

            # create empty dataframes for output storage
            top_topic_words_df = pd.DataFrame(np.random.randn(n_top_words, 0))
            top_topic_dist_df = pd.DataFrame(np.random.randn(n_top_words, 0))

            # collects output and generates starting dataframes
            for i, topic_dist in enumerate(topic_word):
                top_topic_words = np.array(terms)[np.argsort(topic_dist)][:-n_top_words-1:-1]
                top_topic_dist = np.sort(topic_dist)[:-n_top_words-1:-1]

                top_topic_words_df[i] = pd.DataFrame(top_topic_words)
                top_topic_dist_df[i] = pd.DataFrame(top_topic_dist)

            # manipulates dataframes for output
            top_topic_words_df = top_topic_words_df.transpose()
            top_topic_dist_df = top_topic_dist_df.transpose()

            top_topic_words_df.rename(columns=lambda x: "word_" + str(x), inplace=True)
            top_topic_dist_df.rename(columns=lambda x: "topic_wrd_cnt_" + str(x), inplace=True)
            results_df = pd.concat([top_topic_words_df, top_topic_dist_df],axis=1,join='outer')

            results_df['doc_cnt'] = num_terms
            results_df['doc_topic'] = pd.DataFrame(np.transpose(doc_topic))
            results_df['fname'] = filename

            # generates column titles for output
            cols = results_df.columns.tolist()
            cols = cols[-1:] + cols[:-1]
            results_df = results_df[cols]

            col_labels = cols
            col_labels.insert(0,"topic")
            col_labels = np.asarray(col_labels)

            # write output to CSV file
            with open(output_file, "a") as f:
                results_df.to_csv(f, header=False, index=True)
                print str(counter) + " " + filename

        # append column titles to final output using pandas
        with open(output_file, "rb") as f:
            results_df = pd.read_csv(f, names=col_labels, header=None)

        # write finalized CSV
        with open(output_file, "wb") as f:
            results_df.to_csv(f, header=True, index=False)

if __name__ == '__main__':
    input_dir = '/industry_files'
    fin_stopwords = 'fin_stopwords.csv'
    n_top_words = 20
    n_topics = 30
    #fyear = '13'
    output_file = 'topic_output.csv'

    test = topic_generator(input_dir, fin_stopwords_file, output_file, n_top_words, n_topics)
    test.stopwords()
    test.file_manager()
    test.lda_modeler()



