import re
from enum import Enum

class VideoExpression(Enum):
    none = 0
    decisive = 1
    angry = 2
    funny = 3
    insicure = 4
    curious = 5
## example
### metadata = 

### 1|Hello it'me, Ciro.(1)|11(duration in seconds)
def regex() -> str:
    return '[(]\d[)]'


#regex [(]\d[)]$
def hasExpression(sentence)->bool:
    return bool(re.match(".*[?.!][(]\d[)]$", sentence))

def sentence_without_expression(sentence)->str:
    return re.sub('[(]\d[)]$', sentence)

def expression(sentence):
    expression = re.search('[(]\d[)]$', sentence)
    expression_raw_value = expression.group(0).lstrip('(').rsplit(')')
    if int(expression_raw_value[0]) > len(VideoExpression):
        expression_raw_value = 0
    return VideoExpression(int(expression_raw_value[0]))

