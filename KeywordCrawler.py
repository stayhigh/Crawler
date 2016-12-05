import requests
from lxml import html
import argparse
import sys
import csv
import os

parser = argparse.ArgumentParser(description='search a keyword on Walmart.com, and list items on the specific page')
parser.add_argument('keyword', help='search keyword')
parser.add_argument('-p', '--page', type=int, default=1)
args = parser.parse_args()

# take keyword and page number from command line
keyword = args.keyword
pageNum = args.page
query = sys.argv[1]

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
        #if name and nameMark and len(name) >= 2:
        print "name:",name
        print "nameMark:",nameMark
        print "len(name):",len(name)
        if name and len(name) == 1:
            #itemName = '%s%s%s' % (name[0], nameMark[0], name[1])
            itemName = '%s' % (name[0])
        else:
            print '! mulitiple items, we need to choose the best one for ' + query

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

#print res # res is a list of tuples
#print 
for eachitem in res:
    print eachitem

eachitemlist=list(eachitem)
eachitemlist.insert(0, query)
eachitem = tuple(eachitemlist)


OUTPUTFILE="item_price_result.csv"
if not os.path.isfile(OUTPUTFILE) or os.path.getsize(OUTPUTFILE) == 0:
    with open(OUTPUTFILE, 'wb') as out:
        print 'insert label at first row'
        csv_out=csv.writer(out)
        csv_out.writerow(["UPC","url", "item", "price"])
    

with open(OUTPUTFILE,'ab+') as out:
    csv_out=csv.writer(out)
    csv_out.writerow(eachitem)

#data=[('smith, bob',2),('carol',3),('ted',4),('alice',5)]


#with open('item_price_result.csv','wb') as out:
#    csv_out.writerow(['name','num'])
#            for row in data:
#                        csv_out.writerow(row)

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
