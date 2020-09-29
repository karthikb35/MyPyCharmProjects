from note import note

class NoteBook:
    def __init__(self):
        self.Id = 1
        self.notes=[]

    def addNote( self, memo, tags='' ):
        self.notes.append(note( memo,tags))
        self.Id +=1
    
    def _findNote( self, Id ):
        for note in self.notes:
            if note.id == Id:
                return note
        
    def deleteNote( self, Id ):
        if Id in [note.id for note in self.notes ]:
            self.notes.remove(self._findNote(Id))
    
    def updateMemo( self, Id, newmemo ):
        if Id in [note.id for note in self.notes ]:
            note = self._findNote(Id)
            note.updateMemo(newmemo)
            
    def addTag( self, Id, tag ):
        if Id in [note.id for note in self.notes]:
            note = self._findNote ( Id )
            note.addTag(tag)
    
    def deleteTag( self, Id, tag ):
        if Id in [note.id for note in self.notes]:
            note = self._findNote ( Id )
            note.deleteTag(tag)
        