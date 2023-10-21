from sqlalchemy import Column, Integer
from myapp import server

class Patient(server.Base):
    __tablename__ = 'test_patient'
    patient_id = Column(Integer, primary_key=Trues)
