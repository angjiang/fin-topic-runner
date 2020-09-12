# Scraper & Topic Model for 10Ks 

This project extracts and models topics based on public company disclosure in 10Ks. It consists of a scraper for a user-defined index of firm-based (across years) or industry-based (across firms) companies, text normalization and processing, file aggregation, and finally outputs n top LDA topics for each constructed index.

The original intention behind this project was research on identifying informational measures for financial disclosure.

## Data Inputs

To run this project, collect a list of relevant 10Ks for each  index of interest with the appropriate archive location in SEC Edgar. This can be obtained via WRDS or any other similar financial database.

## Filing Crawler

The [filing crawler](./filing_crawler.py) extracts the actual 10K content from the filing, removes tables and non-textual data, and prepares documents for modeling.

## Topic Generator 

The [topic generator](topic_generator.py) generates n topics and outputs the top y words using LDA. 

For each firm’s 10K textual data file, a term-document matrix is created and [stop words](fin_stopwords.csv) are removed. Topics are generated using LDA. For this data, 30 topics and top 20 words per topic are recommended to legibly assess output. 

To create firm-based topics, filings should be aggregated across years with 10 years as the recommended time frame to generate topics.

To create industry-based topics, filings should be aggregated over a relatively constrained index of comparable companies per a filing year to generate topics. The [industry file generator](/industry_file_generator.py) aggregates documents by year to generate the relevant inputs.

