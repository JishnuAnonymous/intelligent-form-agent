from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from . import config
from .utils import setup_logger

logger = setup_logger('storage')

Base = declarative_base()

class Form(Base):
    __tablename__ = 'forms'

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    extracted_data = Column(Text) # JSON string
    raw_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Extracted fields columns for easier querying
    name = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    dob = Column(String, nullable=True)
    signature_detected = Column(Boolean, default=False)

class StorageManager:
    def __init__(self):
        self.engine = create_engine(f'sqlite:///{config.DB_PATH}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def save_form(self, filename, raw_text, extracted_data):
        session = self.Session()
        try:
            import json
            form = Form(
                filename=filename,
                raw_text=raw_text,
                extracted_data=json.dumps(extracted_data),
                name=extracted_data.get('name'),
                email=extracted_data.get('email'),
                phone=extracted_data.get('phone'),
                dob=extracted_data.get('dob'),
                signature_detected=extracted_data.get('signature_detected', False)
            )
            session.add(form)
            session.commit()
            logger.info(f"Saved form {filename} to database with ID {form.id}")
            return form.id
        except Exception as e:
            logger.error(f"Failed to save form: {e}")
            session.rollback()
            return None
        finally:
            session.close()

    def get_form(self, form_id):
        session = self.Session()
        try:
            form = session.query(Form).filter_by(id=form_id).first()
            return form
        finally:
            session.close()

    def get_all_forms(self):
        session = self.Session()
        try:
            return session.query(Form).all()
        finally:
            session.close()
