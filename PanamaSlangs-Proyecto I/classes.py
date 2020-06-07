class Slang ():
    """
    Clase utilizada para crear instancias de palabras del Slang Panameño
    """
    def __init__(self, slang, definition):
        self.slang=slang
        self.definition=definition

    def __repr__(self):
        return f"En panamá {self.slang} significa {self.definition}"