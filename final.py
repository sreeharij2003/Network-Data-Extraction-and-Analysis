import json
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()

class EmploymentType(Base):
    __tablename__ = 'employment_type'
    id = Column(Integer, primary_key=True)
    type = Column(String)

class Company(Base):
    __tablename__ = 'company'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Department(Base):
    __tablename__ = 'department'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class JobType(Base):
    __tablename__ = 'job_type'
    id = Column(Integer, primary_key=True)
    type = Column(String)

class Location(Base):
    __tablename__ = 'location'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Recruiter(Base):
    __tablename__ = 'recruiter'
    id = Column(Integer, primary_key=True)
    name = Column(String)

class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    title = Column(String)

class Opportunity(Base):
    __tablename__ = 'opportunity'
    id = Column(Integer, primary_key=True, autoincrement=True)
    job_title = Column(String)
    posted_date = Column(String)
    job_description = Column(Text)
    source = Column(String)
    experience_min = Column(Integer)
    experience_max = Column(Integer)
    employment_type_id = Column(Integer, ForeignKey('employment_type.id'))
    company_id = Column(Integer, ForeignKey('company.id'))
    department_id = Column(Integer, ForeignKey('department.id'))
    job_type_id = Column(Integer, ForeignKey('job_type.id'))
    recruiter_id = Column(Integer, ForeignKey('recruiter.id'))

    employment_type = relationship('EmploymentType')
    company = relationship('Company')
    department = relationship('Department')
    job_type = relationship('JobType')
    recruiter = relationship('Recruiter')

engine = create_engine('sqlite:///mydatabase.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

session.query(Opportunity).delete()
session.query(Role).delete()
session.query(Recruiter).delete()
session.query(Location).delete()
session.query(JobType).delete()
session.query(Department).delete()
session.query(Company).delete()
session.query(EmploymentType).delete()

json_data = '''
{
  "opportunity": {
    "job_title": "Senior SAC Consultant",
    "posted_date": "2024-08-06T12:34:56Z",
    "employment_type": [
      {
        "id": 1,
        "type": "Full-time"
      }
    ],
    "job_description": "<p><strong>What you will do at TekLink</strong></p>...",
    "company": {
      "id": 1,
      "name": "Hinduja Global Solutions Limited"
    },
    "department": {
      "id": 1,
      "name": "IT"
    },
    "source": "FoundIt",
    "job_type": {
      "id": 1,
      "type": "Permanent"
    },
    "skills": ["SAP Cloud Analytics", "SAC", "Hana"],
    "location": [
      {
        "id": 1,
        "name": "Hyderabad / Secunderabad, Telangana"
      },
      {
        "id": 2,
        "name": "Bengaluru / Bangalore"
      }
    ],
    "experience_years": {
      "minimum": 4,
      "maximum": 8
    },
    "recruiter": {
      "id": 986391,
      "name": "Naresh Rathikrinda"
    },
    "role": [
      {
        "id": 1,
        "title": "Software Engineer/Programmer"
      }
    ]
  }
}
'''

data = json.loads(json_data)

for emp_type in data['opportunity']['employment_type']:
    session.add(EmploymentType(id=emp_type['id'], type=emp_type['type']))

company_data = data['opportunity']['company']
session.add(Company(id=company_data['id'], name=company_data['name']))

department_data = data['opportunity']['department']
session.add(Department(id=department_data['id'], name=department_data['name']))

job_type_data = data['opportunity']['job_type']
session.add(JobType(id=job_type_data['id'], type=job_type_data['type']))

for location in data['opportunity']['location']:
    session.add(Location(id=location['id'], name=location['name']))

recruiter_data = data['opportunity']['recruiter']
session.add(Recruiter(id=recruiter_data['id'], name=recruiter_data['name']))

for role in data['opportunity']['role']:
    session.add(Role(id=role['id'], title=role['title']))

opp = data['opportunity']
session.add(Opportunity(
    job_title=opp['job_title'],
    posted_date=opp['posted_date'],
    job_description=opp['job_description'],
    source=opp['source'],
    experience_min=opp['experience_years']['minimum'],
    experience_max=opp['experience_years']['maximum'],
    employment_type_id=opp['employment_type'][0]['id'],
    company_id=opp['company']['id'],
    department_id=opp['department']['id'],
    job_type_id=opp['job_type']['id'],
    recruiter_id=opp['recruiter']['id']
))

session.commit()

print("Employment Types:")
for emp in session.query(EmploymentType).all():
    print(f"ID: {emp.id}, Type: {emp.type}")

print("\nCompanies:")
for comp in session.query(Company).all():
    print(f"ID: {comp.id}, Name: {comp.name}")

print("\nDepartments:")
for dept in session.query(Department).all():
    print(f"ID: {dept.id}, Name: {dept.name}")

print("\nJob Types:")
for job in session.query(JobType).all():
    print(f"ID: {job.id}, Type: {job.type}")

print("\nLocations:")
for loc in session.query(Location).all():
    print(f"ID: {loc.id}, Name: {loc.name}")

print("\nRecruiters:")
for rec in session.query(Recruiter).all():
    print(f"ID: {rec.id}, Name: {rec.name}")

print("\nRoles:")
for role in session.query(Role).all():
    print(f"ID: {role.id}, Title: {role.title}")

print("\nOpportunities:")
for opp in session.query(Opportunity).all():
    print(f"ID: {opp.id}, Job Title: {opp.job_title}, Posted Date: {opp.posted_date}, Job Description: {opp.job_description[:50]}")

print("\nSkills:")
for skill in data['opportunity']['skills']:
    print(f"- {skill}")

experience_years = data['opportunity']['experience_years']
print(f"\nExperience Years: Minimum: {experience_years['minimum']}, Maximum: {experience_years['maximum']}")
