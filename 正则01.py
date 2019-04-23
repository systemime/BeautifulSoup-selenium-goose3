import re

txt='<p>ni hao</p>'

re1='(<)'	# Any Single Character 1
re2='.*?'	# Non-greedy match on filler
re3='(>)'	# Any Single Character 2

rg = re.compile(re1+re2+re3,re.IGNORECASE|re.DOTALL)
m = rg.search(txt)
if m:
    c1=m.group(1)
    c2=m.group(2)
    print(c1+c2+"\n")