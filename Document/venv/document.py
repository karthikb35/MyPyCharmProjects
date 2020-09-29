class Character:
    def __init__(self, character, bold=False, italic = False, underline = False):
        self._character = character
        self.bold = '*' if bold else ''
        self.italic = '/' if italic else ''
        self.underline = '_' if underline else ''

    def __str__(self):
        return self.bold+self.italic+self.underline+self._character


class Cursor:
    def __init__(self):
        self.position = 0

    def moveright( self ):
        self.position += 1

    def moveleft( self ):
        self.position -=1

class Document:
    def __init__(self):
        self.characters = []
        self.cursor = Cursor()

    def insert( self, character ):
        self.characters.insert(self.cursor.position, str(character))
        self.cursor.moveright()

    def home( self ):
        while self.characters[self.cursor.position-1]!='\n' and self.cursor.position > 0:
            self.cursor.moveleft()

    def end( self ):
        while self.characters[self.cursor.position-1] != '\n' and self.cursor.position < len(self.characters):
            self.cursor.moveright()

    def delete( self ):
        del self.characters[self.cursor.position]

    @property
    def string( self ):
        for char in self.characters:
            print(char, end = '' if char != '\n' else '')
