from NoteBook import NoteBook
from collections import namedtuple



class Menu:

    def __init__(self):
        self.NoteBook = NoteBook()
        self.choices = {
            "1" : self.displayMenu,
            "2" : self.showNotes,
            "3" : self.addNote,
            "4" : self.deleteNote,
            "5" : self.updateMemo,
            "6" : self.addTag,
            "7" : self.deleteTag,
        }

    def Menu( self ):
        return " 1: Display Menu\n" \
               " 2: Show Notes\n" \
               " 3: Add Note\n" \
               " 4: Delete Note\n" \
               " 5: Update Memo\n" \
               " 6: Add Tag\n" \
               " 7: Delete Tag\n" \


    def displayMenu( self ):
        while True:
            print(self.Menu())
            choice = input("Enter Your Input: ")
            action = self.choices.get(choice)
            if action:
                action()

    def showNotes( self ):
        for note in self.NoteBook.notes:
            print(note)
    def addNote( self ):
        memo=input("Enter your Note: ")
        tags_raw=input("Enter tags: ")
        tags=tags_raw.split()
        self.NoteBook.addNote(memo,tags)

    def deleteNote( self ):
        Id = int(input("Enter Note Id: "))
        self.NoteBook.deleteNote(Id)

    def updateMemo( self ):
        Id = int(input("Enter Note Id: "))
        updatedMemo = input("Enter New memo: ")
        self.NoteBook.updateMemo(Id, updatedMemo)

    def addTag( self ):
        Id = int ( input ( "Enter Note Id: " ) )
        newTag = input("Enter New Tag: ")
        self.NoteBook.addTag(Id,newTag)

    def deleteTag( self ):
        Id = int ( input ( "Enter Note Id: " ) )
        deleteTag = input("Enter Tag to be deleted: ")
        self.NoteBook.deleteTag(Id,deleteTag)


if __name__== '__main__':
    menu = Menu()
    menu.displayMenu()







