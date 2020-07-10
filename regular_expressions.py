import re


# ===================================================== re.search()========================================
patterns = ['term1','term2']
text_to_search = "This is a string with term1, but it does not have the other term"
for pattern in patterns:
    print(f"Searching for the {pattern} in {text_to_search}")
    # print(re.search(text_to_search,pattern))
    if re.search(pattern,text_to_search):
        print("Pattern matched")
        match = re.search(pattern,text_to_search)
        print(match)
        print(type(match))
        print(match.start())
        print(match.end())
    else:
        print("Pattern not matched")

# ===================================================== re.split()========================================
print("================================================")
print("This is from re.split() method")
split_term = '@'
phrase = "What is youe email, is it hello@gmail.com"
splitted_items = re.split(split_term,phrase)
print(splitted_items)

# ===================================================== re.findall()========================================
print("================================================")
print("This is from findall() method")
find_match = 'match'
phrase_to_find = "This is one Match, and this is another match, also there is one more match"
finded_list = re.findall(find_match,phrase_to_find)
print(finded_list)
print(f"The count of match is: {len(finded_list)}")



# ===================================================== re.repetition patterns========================================
print("================================================")
print("This is from repetition patterns method")
test_phrase = 'sdsd..sssbddd...sdddsddd...dsds...dsssss...sdddd...sdd'
def multi_re_find(patterns,phrase):
    '''
    Takes in a list of regex patterns
    Prints a list of all matches
    '''
    for pattern in patterns:
        print('Searching the phrase using the re check: %r' %(pattern))
        print(re.findall(pattern,phrase))
        print(len(re.findall(pattern,phrase)))
        print('\n')
test_patterns = [ 'sd*',     # s followed by zero or more d's
                'sb+',          # s followed by one or more d's
                'sd?',          # s followed by zero or one d's
                'sd{3}',        # s followed by three d's
                'sd{2,3}',      # s followed by two to three d's
                ]
multi_re_find(test_patterns,test_phrase)


print("================================================")
print("This is from character sets patterns method")
char_test_patterns = ['[sd]',    # either s or d
                's[sd]+']   # s followed by one or more s or d
multi_re_find(char_test_patterns,test_phrase)
print("================================================")
print("This is from Exclusion match")
exclusion_test_phrase = 'This is a string! But it has punctuation. How can we remove it?'
exc_pattern = '[^?!. ]+'
print(re.findall(exc_pattern,exclusion_test_phrase))



print("================================================")
print("This is from character Ranges")
charrange_test_phrase = 'This is an example sentence. Lets see if we can find some letters. aND'

charrange_test_patterns=['[a-z]+',      # sequences of lower case letters
               '[A-Z]+',      # sequences of upper case letters
               '[a-zA-Z]+',   # sequences of lower or upper case letters
               '[A-Z][a-z]+',  # one upper case letter followed by lower case letters
               '[a-z][A-Z]+'] # Sequence of lowercase letter


multi_re_find(charrange_test_patterns,charrange_test_phrase)

print("================================================")
print("This is from Escape code")
esc_test_phrase = 'This is a string with some numbers 1233 and a symbol #hashtag'

esc_test_patterns=[ r'\d+', # sequence of digits
                r'\D+', # sequence of non-digits
                r'\s+', # sequence of whitespace
                r'\S+', # sequence of non-whitespace
                r'\w+', # alphanumeric characters
                r'\W+', # non-alphanumeric
                ]

multi_re_find(esc_test_patterns,esc_test_phrase)


# email_pattern = '[a-z][@][a-z][.][a-z]+'
# email_phrase = 'haranbala@gmail.com'
# if re.findall(email_pattern,email_phrase):
#     print("Email matched")
# else:
#     print("Email not matched")
samp_pattern = 'eggs'
samp_phrase = "eggseggssandeggs"
# =================Match()=====================search match in the beginning
if re.match(samp_pattern,samp_phrase):
    print("Pattern matched")
else:
    print("Pattern not matched")
print(re.match(samp_pattern,samp_phrase))
# =================Search()=====================search whether the phrase contains the given pattern
if re.search(samp_pattern,samp_phrase):
    print("Pattern matched")
else:
    print("Pattern not matched")
print(re.search(samp_pattern,samp_phrase))
# =================findall()=====================find and give a list of matches found
if re.findall(samp_pattern,samp_phrase):
    print("Pattern matched")
else:
    print("Pattern not matched")
print(re.findall(samp_pattern,samp_phrase))
# =================find and replace - sub()===================== Replaces the pattern with new given text in the phrase
ori_string = "Hi this is John, i am John"
fr_pattern = 'John'
new_replace = 'Haran'
new_text = re.sub(fr_pattern,new_replace,ori_string)
print(new_text)
# =================Dot metacharacter(.)===================== Find out the match by replacing dot with any character in the given phrase
dot_pattern = 'gr.y'
dor_phrase = 'grey'
if re.match(dot_pattern,dor_phrase):
    print("Match found")

# =================Caret(^) and Dollar($) metacharacter===================== Find out the match
caret_pattern = '^gr.y$'
caret_phrase = 'grfy'
if re.match(caret_pattern,caret_phrase):
    print("Match found g")
else:
    print("Caret match not found")
print(re.findall(caret_pattern,caret_phrase))