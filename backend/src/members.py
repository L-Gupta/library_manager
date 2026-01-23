"""
Member management module for Library Manager
"""
import datetime as dt
import random
from backend_utils import SEPARATOR


class Member:
    """Represents a library member"""
    
    def __init__(self, db, member_id=None, name=None, dob=None, gender=None, contact=None, email=None, password=None):
        """Initialize a member object"""
        self.db = db
        self.member_id = member_id
        self.name = name
        self.dob = dob
        self.gender = gender
        self.contact = contact
        self.email = email
        self.password = password
        self.status = 'active'
    
    @staticmethod
    def generate_unique_id(db):
        """Generate a unique member ID"""
        while True:
            mid = ''
            for i in range(3):
                mid += str(random.randint(0, 9))
            mid += chr(random.randint(65, 90))
            for i in range(2):
                mid += str(random.randint(0, 9))
            
            query = "select cust_id from member_details;"
            db.execute(query)
            existing_ids = [row[0] for row in db.fetchall()]
            
            if mid not in existing_ids:
                return mid
    
    def save(self):
        """Save member to database"""
        query1 = "insert into member_details values(%s, %s, %s, %s);"
        values1 = (self.member_id, self.email, self.password, self.status)
        self.db.execute(query1, values1)
        self.db.commit()
        
        query2 = "insert into member values(%s, %s, %s, %s, %s);"
        values2 = (self.member_id, self.name, self.dob, self.gender, self.contact)
        self.db.execute(query2, values2)
        self.db.commit()
    
    def update_status(self, new_status):
        """Update member status"""
        query = "update member_details set status = %s where cust_id = %s;"
        self.db.execute(query, (new_status, self.member_id))
        self.db.commit()
        self.status = new_status
    
    @staticmethod
    def get_all(db):
        """Get all members from the database"""
        query = "select * from member"
        db.execute(query)
        return db.fetchall()


class MemberManager:
    """Manages member operations"""
    
    def __init__(self, db):
        """Initialize MemberManager with database connection"""
        self.db = db
    
    def register_new_member(self):
        """Add a new member to the library"""
        name = input("Enter your name:....")
        print("Enter your date of birth")
        y = int(input("Enter year of birth(YYYY):....."))
        m = int(input("Enter month of birth(MM):....."))
        d = int(input("Enter date of birth(DD):....."))
        dob = dt.date(y, m, d)
        gender = input("Enter your gender (M,F,O):.....")
        contact = int(input("Enter your mobile number:....."))
        email = input("Enter your mail id:....")
        password = input("Enter a password:.....")
        
        member_id = Member.generate_unique_id(self.db)
        member = Member(self.db, member_id, name.title(), dob, gender.upper(), contact, email, password)
        
        print()
        print("Your member ID is", member_id)
        print()
        print("Your account details are", (member_id, email, password, 'active'))
        print("Your personal details are", (member_id, name.title(), dob, gender.upper(), contact))
        print("1. To confirm details, enter 'yes' ")
        print("2. To exit, enter anything else")
        ch = input("Do you confirm?\n")
        
        if ch.lower() == 'yes':
            member.save()
            print("Customer successfully registered")
            print(SEPARATOR)
            print()
        else:
            print("Registeration interupted")
            print(SEPARATOR)
            print()
    
    def change_member_status(self):
        """Change status of a member"""
        m_id = input("Enter ID of member:.....")
        print("1. Set status to active")
        print("2. Set status to not active")
        ch = int(input("Enter your choice:....."))
        
        if ch == 1:
            member = Member(self.db, member_id=m_id)
            member.update_status('active')
            print("Status of", m_id, "set to active")
            print(SEPARATOR)
            print()
        elif ch == 2:
            member = Member(self.db, member_id=m_id)
            member.update_status('not active')
            print("Status of", m_id, "set to not active")
            print(SEPARATOR)
            print()
        else:
            print("Please enter a valid choice")
            print(SEPARATOR)
            print()
    
    def display_all_members(self):
        """Display all library members"""
        members = Member.get_all(self.db)
        for member in members:
            print(member)
        print(SEPARATOR)
