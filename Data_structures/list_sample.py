samp = [['Burette 1', '', 'MB/ACT_A1'], ['Burette 2', '', 'Not connected'], ['Burette 5', '', 'Not connected'], ['burette 3', '', 'Not connected'], ['burette 5', '', 'Not connected']]
if all('burette 15' not in sublist for sublist in samp):
    print('exist')
if any('burette 5' in sublist for sublist in samp):
    print('exist')