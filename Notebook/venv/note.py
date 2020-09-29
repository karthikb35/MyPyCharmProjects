import datetime


class note:
    Id = 1
    def __init__(self, memo, tags=''):
        
        self.id = note.Id
        self.memo = memo
        self.tags = tags
        self.creation_date = datetime.date.today ( )
        note.Id += 1
    
    def updateMemo( self, memo ):
        self.memo=memo
    
    def addTag( self, tag ):
        self.tags.append(tag)
    
    def deleteTag( self, tag ):
        if tag in self.tags:
            self.tags.remove(tag)
            
    def __str__(self):
        return f'{self.id}\t{self.creation_date}\t{self.memo}\t{self.tags}'
        
    
        