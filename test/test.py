#! /opt/local/bin/python2.7

class Employee:

    count = 0
    company = 'foobar'
    raise_amount = 1.04

    def __init__(self, first, last):
        self.first = first
        self.last = last
        self.email = first + '.' + last + '@' + self.company + '.com'
        self.pay = 40000
        Employee.count += 1

    def apply_raise(self):
        self.pay *= self.raise_amount

    def increase_raise(self, increase):
        self.raise_amount = increase

    @classmethod
    def set_raise_amount(cls, amount):
        cls.raise_amount = amount


if __name__ == "__main__":
    emp_1 = Employee('Jean-Pierre', 'Forcioli')
    emp_2 = Employee('Alain', 'Forcioli')

    Employee.set_raise_amount(10)
    print emp_1.raise_amount
    print emp_2.raise_amount    
