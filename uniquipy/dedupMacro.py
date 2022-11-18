from dedupFuncs import *



def run_dedup(fileName):
    print 'Reading records...'
    all_records = read_records(fileName)

    print 'Excluding duplicate titles...'
    edited_records = uniqify(all_records, lambda x: x[len(x)-1:][0])

    print 'Flagging likely duplicates...'
    likely_dups = likely(edited_records.edit)

    print 'Outputting results...'
    output_records(fileName, 'edit', edited_records.edit)
    output_records(fileName, 'dups', edited_records.duplicates)
    output_records(fileName, 'likely_dups', likely_dups)

    print 'deduplication complete'
    print 'duplicates removed: ', len(edited_records.duplicates)
    print 'Possible duplicates: ', len(likely_dups)
    
    return DedupResultContainer(all_records,  edited_records, likely_dups)
    
    


class DedupResultContainer():
    def __init__(self,  found,  edited,  likely):
        """
        Constructor
        """
        self.found = found
        self.edited_records = edited
        self.likely_dups = likely

    def count_found(self):
        return len(self.found)
        
    def count_title_duplicates(self):
        return len(self.edited_records.duplicates)
        
    def count_likely_duplicates(self):
        return len(self.likely_dups)
            
    def count_unique(self):
        return len(self.found) -  len(self.edited_records.duplicates)
        
        
