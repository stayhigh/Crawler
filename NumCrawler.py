"""
This basic crawler search the number of items searched on Walmart website
"""

import requests
from lxml import html
import re
import argparse

parser = argparse.ArgumentParser(description='retrieve the number of items on Walmart.')
parser.add_argument('keyword', help = 'the keyword for searching')
args = parser.parse_args()

keyword = args.keyword
url = 'http://www.walmart.com/search/?query=%s' % (keyword)
page = requests.get(url)
tree = html.fromstring(page.content)

totalNumLine = tree.xpath('//div[@class="result-summary-container"]/text()')
match = re.search(r'^.*Showing.*of (.+) results', totalNumLine[0])
num = int(match.group(1).replace(',', ''))

print "%d %s are found on walmart" % (num, keyword)








