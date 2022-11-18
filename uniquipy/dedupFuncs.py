#--------------------------------------------------------------------
#
#   Module:         dedupFuncs
#   Description:    Simple script for removing duplicate EndNote entries
#   Author:         T.Monks
#   Python ver:     2.7.2
#
#   Logic:          1. Strip punctuation/whitespace from titles
#                   2. Remove all matching titles (pass 1)
#                   3. Flag all entries with matching:
#                       a. author surnames (concatonated, lowercase, no whitespace)
#                       b. Year of pub
#                       c. Volumn of pub
#                       d. journal title (no puct/whitespace)
#--------------------------------------------------------------------

import sys
sys.path.append(r"C:\Python27\Lib\string")


class Results:
    def __init__(self):
        self.duplicates = []
        self.edit = []

       
def remove_punct(title):
    s = title.translate(string.maketrans("",""), string.punctuation)
    return s.replace(' ', '')


def uniqify(seq, idfun=None): 
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   unique = Results()
   
   for item in seq:
       marker = idfun(item)
       if marker in seen:
           unique.duplicates.append(item)
           continue
       seen[marker] = 1
       unique.edit.append(item)

   return unique




def likely(records):
    found = set()
    likely_dups = []
    
    for item in records:
        li = item[len(item)-2]
        if li not in found:
            found.add(li)
        else:
            likely_dups.append(item)
            
    return likely_dups
            

def read_records(fileName):

    try:
        f = open(fileName, 'r')
    except IOError as e:
        try:
            f = open(fileName + '.txt', 'r')

        except IOError as e:
            print "Error accessing file.  Please make sure that filename is correct."
            sys.exit()

    curr_record = []
    likely_details = ()
    all_records = []
    title = ''
    journal = ''
    authors = ''
    year = 0
    vol = 0
    
    for line in f:
               
        if line[0:2] == '%0':

            likely_details = authors, year, vol, journal
            curr_record.append(likely_details)
            curr_record.append(title)
            authors = ''
            all_records.append(curr_record)
            curr_record = []
                        
        elif line[0:2] == '%T':
            
            title = remove_punct(line[3:len(line)-1].lower())

        elif line[0:2] == '%J':
            
            journal = remove_punct(line[3:len(line)-1].lower())

        elif line[0:2] == '%D':
           
            year = line[3:len(line)-1]

        elif line[0:2] == '%V':
            
            year = line[3:len(line)-1]

        elif line[0:2] == '%A':
            
            authors = ''.join([authors, line[3:line.find(',')].lower()])
            
        
        curr_record.append(line)
        
    all_records.append(curr_record)
    f.close()
    return all_records


def output_records(fileName, postFix, all_records):
    newFileName = fileName + '_' + postFix + '.txt'
    f = open(newFileName, 'w')

    for record in all_records:
        for line in record[0:len(record)-2]:
            f.write(str(line))
            

    f.close()    
    






    






    
