__author__ = 'Sebastian.Law'

import processemail
import transaction
import re

s = []
# s.append(' Badly Drawn Boy at Barbican Centre London, London, UK')
# s.append('  181759978    |    Order date: 21/07/2015')
# s.append('  181759978    |    Order date: 21/07/2015')
# s.append(' x 1')
# s.append(' Badly Drawn Boy at Barbican Centre London, London, UK')
# s.append(' 30/10/2015 19:30 - The O2 Arena')
s.append('Quantity:')
s.append(' 4 ticket(s) Level 1 Seating')
# s.append(' £344.99 per ticket')
# s.append(' 30/10/2015 19:30 - The O2 Arena')
# s.append('Order #: 181759978    |    Order date: 21/07/2015')
s.append(' x')

s = [l.strip() for l in s]

tag = 'Quantity:'
offset = 0
split_string = 'ticket\(s\)'
split_element = 0
specific = ' 4 ticket(s) Level 1 Seating'
check = re.split(split_string,specific)

# out = transaction.extract(s, tag, offset, split_string, split_element)


print("\ntests.py complete\n")