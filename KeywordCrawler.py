import requests
from lxml import html
import argparse
import sys


parser = argparse.ArgumentParser(description='search a keyword on Walmart.com, and list items on the specific page')
parser.add_argument('keyword', help='search keyword')
parser.add_argument('-p', '--page', type=int, default=1)
args = parser.parse_args()

# take keyword and page number from command line
keyword = args.keyword
pageNum = args.page

# build the query url
url = 'http://www.walmart.com/search/?query=%s&page=%d&cat_id=0' % (keyword, pageNum)
page = requests.get(url)
tree = html.fromstring(page.content)

# check the validity of pageNum on the pagination widget, find the total number of pages
totalCount = int(tree.xpath('//ul[@class="paginator-list"]/li[last()]/a/text()')[0])
if pageNum < 1 or pageNum > totalCount:
    sys.exit('page num error!')


links = []
names = []
prices = []

res = []

items = tree.xpath('//div[@class="tile-content"]')
for item in items:

    node = item.xpath('.//a[@class="js-product-title"]/@href')
    if node:
        link = 'http://walmart.com%s' % (node[0])

    node = item.xpath('.//a[@class="js-product-title"]')
    if node:
        nameMark = node[0].xpath('mark/text()')
        name = node[0].xpath('text()')
        if name and nameMark and len(name) >= 2:
            itemName = '%s%s%s' % (name[0], nameMark[0], name[1])

    node = item.xpath('.//span[starts-with(@class, "price price-display")]')
    if node:
        ss = []
        for subNode in node[0].xpath('node()'):
            if isinstance(subNode, basestring):
                ss.append(subNode)
            else:
                ss.append(subNode.xpath('text()')[0])
        price = ''.join(ss).strip()

    res.append((link, itemName, price))

print res

"""
# link
items = tree.xpath('//a[@class="js-product-title"]/@href')
ips = ['http://walmart.com%s' % (x) for x in items]
print ips


# name
nodes = tree.xpath('//a[@class="js-product-title"]')
names = []
for node in nodes:
    nameMark = node.xpath('mark/text()')[0]
    name = node.xpath('text()')
    names.append('%s%s%s' % (name[0], nameMark, name[1]))

print names

# price
prices = []
nodes = tree.xpath('//span[@class="price price-display"]')
for node in nodes:
    ss = []
    for subNode in node.xpath('node()'):
        if isinstance(subNode, basestring):
            ss.append(subNode)
        else:
            ss.append(subNode.xpath('text()')[0])
    prices.append(''.join(ss).strip())

print prices
"""
