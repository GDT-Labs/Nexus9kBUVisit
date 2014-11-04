class Device(object):
    # Initializer
    def __init__(self, name):
        # An instance variable to hold the student's name
        self._name = name
 
    # Getter method
    @property
    def name(self):
        return self._name
 
    # Setter method
    @name.setter
    def name(self, new_name):
        self._name = new_name