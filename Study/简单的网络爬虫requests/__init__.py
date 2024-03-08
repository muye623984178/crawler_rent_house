import re

match = re.search('..g','bing')
print(match.group())
print(re.sub('i', 'I', 'bing'))
