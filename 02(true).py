from collections import UserDict

class Field:
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value
    def __repr__(self) -> str:
        return str(self)
        


class Name(Field):
    ...
    
class Phone(Field):
    ...
    
class Record:
    def __init__(self, name: Name, phone: Phone = None):
        self.name = name
        self.phones = []
        if phone:
            self.phones.append(phone)
    
    def change_phone(self, old_phone, new_phone):
        for k,v in enumerate(self.phones):
            if old_phone.value == v.value:
                self.phones[k] = new_phone
                return f"Old phone {old_phone} change to {new_phone}"
        return f"{old_phone} absent for contact {self.name}"
    
    def add_phone(self, phone: Phone):
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return f"phone {phone} add to contact {self.name}"
        return f"phone {phone} already exists for contact {self.name}"
    
    def __str__(self) -> str:
        return f"{self.name}: {', '.join(str(p) for p in self.phones)}"
    
    
    
class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return 'Add success'
    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())




users_contact = AddressBook()

list_end = ['good bye', 'close', 'exit']

def decorator_input_error(func):
    def wrapper(*args):
        try:
            return func(*args)
        except ValueError:
            return('Give me correct data please')
        except IndexError:
            return('Give me correct data please')
        except KeyError:
            return('Give me correct data please')
    return wrapper

@decorator_input_error
def hello(*args):
    return 'How can I help you?'

@decorator_input_error
def add(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    rec: Record = users_contact.get(str(name))
    if rec:
        return rec.add_phone(phone)
    rec = Record(name, phone)
    return users_contact.add_record(rec)
    

@decorator_input_error
def change_number(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec: Record = users_contact.get(str(name))
    if rec:
        return rec.change_phone(old_phone, new_phone)
    users_contact[name] = phone
    return f"no contact {name} in address book"

@decorator_input_error
def phone(*args):
    name_user = args[0]
    phone = args[1]  
    for name, phone in users_contact.items():
        if name_user == name:
            return phone
        
@decorator_input_error
def show_all(*args):
    return users_contact

@decorator_input_error
def no_command(*args):
    return 'unknown_command'

dict_command = {'hello': hello,
                'add': add,
                'change': change_number,
                'phone': phone,
                'show': show_all,
                }

def parser(text: str) -> tuple[callable, tuple[str]]:
    text1 = text.split()
    if text1[0] in dict_command.keys():
        return dict_command.get(text1[0]), text.replace(text1[0], '').strip().split()
    return no_command, text

def main():
    while True:
        user_input = input('>>>')
        user_input = user_input.lower()
        
        if user_input in list_end:
            print('Good bye!')
            break
        
        command, data = parser(user_input)
        result = command(*data)
        print(result)
        
        
        
        
if __name__ == '__main__':
    main()