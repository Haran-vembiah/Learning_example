import random

import pandas as pd

list1 = ['Lydia', 'Hari', 'Vidhusha', 'Nagaraj', 'Priya', 'Saranya', 'Latha', 'Santini', 'Aravindh', 'Prema']
list2 = ["Peter Piper picked a peck of pickled peppers", "The sixth sick sheik's sixth sheep's sick",
         "How can a clam cram in a clean cream can?", "I saw a kitten eating chicken in the kitchen",
         "Fred fed Ted bread, and Ted fed Fred bread", "Lesser leather never weathered wetter weather better",
         "Which witch switched the Swiss wristwatches?",
         "Betty bought a bit of butter. But the butter Betty bought was bitter",
         "Send toast to ten tense stout saints’ ten tall tents", "Scissors sizzle, thistles sizzle",
         "Two tiny timid toads trying to trot to Tarrytown"]
ran_name = []
ran_word = []
# print(random.choice(list3))
print(len(list1))
for x in range(len(list1)):
    random_name = random.choice(list1)
    ran_name.append(random_name)
    print(random_name)
    list1.remove(random_name)
for y in range(len(ran_name)):
    random_word = random.choice(list2)
    ran_word.append(random_word)
    print(random_word)
    list2.remove(random_word)

df = pd.DataFrame(
    {
        'Names': ran_name,
        'Twisters': ran_word
    }
)
df_name = pd.DataFrame(
    {
        'Names': ran_name
    }
)
with pd.ExcelWriter('fun_events.xlsx') as writer:
    df.to_excel(writer, sheet_name='Twister', index=False)
    df_name.to_excel(writer, sheet_name='Names', index=False)
