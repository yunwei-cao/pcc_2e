class Employee():
    """A class to represent an employee."""
    
    def __init__(self, fname, lname, salary):
        """Initialize the employee."""
        self.fname = fname.title()
        self.lname = lname.title()
        self.salary = salary
        
    def give_raise(self, amount = 5000):
        """Give the employee a raise."""
        self.salary += amount