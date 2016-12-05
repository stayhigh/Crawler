# execute the program and check the result
rm item_price_result.csv
python KeywordCrawler.py 021200471551 && cat item_price_result.csv && soffice --calc item_price_result.csv 
