from sqlalchemy import Column, Integer, String, Boolean, DateTime,ForeignKey 
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base 
from .jobs import jobs, jobCategory  #  import jobs and jobCategory models

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100),  index=True, nullable=False)
    password = Column(String(100), nullable=False)   # hashed password
    firstname = Column(String(100),   index=True, nullable=False)
    middlename = Column(String(100), nullable=True)
    lastname = Column(String(100),   index=True, nullable=False)
    emailAddy = Column(String(100), unique=True, index=True, nullable=False)   
    isVerifiedEmail = Column(Boolean, default=False)    
    dateTimeCreated = Column(DateTime, default=datetime.utcnow)
    vTokens = relationship('vTokens', back_populates='user')
    passResetTokens = relationship('passResetTokens', back_populates='user')     
    staff = relationship('Staff', back_populates='user')
    students = relationship('Students', back_populates='user')
    admins = relationship('Admins', back_populates='user')
    jobs = relationship("jobs", back_populates="owner")  #  user who posted the job
    job_category = relationship("jobCategory", back_populates="user")  #  user who created the job category
    applications = relationship("applications", back_populates="user")  #  user who applied for the job
   
    
class vTokens(Base):  # verification tokens are stored in this table per Users account
    __tablename__ =  'vTokens'
    emailVerificationToken = Column(String(100), primary_key= True, nullable=False)  #  remove record after verification is completed
    user_id =  Column(Integer,  ForeignKey("users.id"), unique=True, nullable= False) # must be a user  
    user = relationship('Users', back_populates='vTokens') 
class passResetTokens(Base):  # password reset tokens are stored in this table per Users account
    __tablename__ =  'passResetTokens'
    pToken = Column(String(100), primary_key= True, nullable=False)  #  remove record after [password reset] is completed
    user_id =  Column(Integer,  ForeignKey("users.id"), unique=True, nullable= False) # must be a user  
    user = relationship('Users', back_populates='passResetTokens')   
class Staff(Base):
    __tablename__ = 'staff'  #  staff account...
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)     
    is_Active = Column(Boolean, default=True)
    designation =Column(String(100), nullable=False)
    department =Column(String(100), nullable=False)
    dateTimeCreated = Column(DateTime, default=datetime.utcnow)
    user_id =  Column(Integer,  ForeignKey("users.id"), unique=True, nullable= False) # must be a user   
    user = relationship('Users', back_populates='staff')
class Students(Base):
    __tablename__ = 'students'  #  students account...
    id = Column(Integer, primary_key=True, index=True, autoincrement=True) 
    programme =Column(String(100), nullable=False) # programme code, eg CMP, BCH, etc.      
    level = Column(Integer, nullable=False)  
    is_Active = Column(Boolean, default=True)
    is_UG = Column(Boolean, default=True)  # default is undergraduate
    dateTimeCreated = Column(DateTime, default=datetime.utcnow)
    user_id =  Column(Integer,  ForeignKey("users.id"), unique=True,nullable= False) # must be a user  
    user = relationship('Users', back_populates='students')
class Admins(Base):  
    __tablename__ = 'admins'  #  they will use the admin dashboard
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)    
    is_Active = Column(Boolean, default=False)  # not active by default
    dateTimeCreated = Column(DateTime, default=datetime.utcnow)
    user_id =  Column(Integer,  ForeignKey("users.id"), unique=True,nullable= False) 
                # must be a user  (staff or student)
    user = relationship('Users', back_populates='admins')
    super_admin = relationship('SuperAdmin', back_populates='admin')  #  one admin can have one super admin

class SuperAdmin(Base):  
    __tablename__ = 'super_admins'  #  they will use the admin dashboard
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)    
    is_Active = Column(Boolean, default=False)  # not active by default
    dateTimeCreated = Column(DateTime, default=datetime.utcnow)
    admin_id =  Column(Integer,  ForeignKey("admins.id"), unique=True,nullable= False) 
                # must be a user  (staff or student)
    admin = relationship('Admins', back_populates='super_admin')
