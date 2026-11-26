from datetime import datetime
from models.constants import CLAIM_STATUSES

class Claim:
    def __init__(
            self,
            claim_id: str,
            item_id: str,
            claimer_username: str,
            claimer_name: str,
            claimer_faculty: str,
            claimer_contact: str,
            secret_answer: str,
            created_at: str | None=None,
            status: str = 'PENDING'
                 ):
            self.claim_id= claim_id
            self.item_id=item_id
            self.claimer_username=claimer_username
            self.claimer_name=claimer_name
            self.claimer_faculty=claimer_faculty
            self.claimer_contact=claimer_contact
            self.secret_answer=secret_answer
            self.created_at=created_at or datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.status=status

    def decide(self, new_status: str)->None:
        if new_status not in CLAIM_STATUSES or new_status == "PENDING":
            raise ValueError(f"Keputusan klaim '{new_status}' tidak valid! Harus APPROVED atau REJECTED.")
        self.status = new_status
    def to_dict(self)->dict:
         return{
            'claim_id': self.claim_id,
            'item_id': self.item_id,
            'claimer_username': self.claimer_username,
            'claimer_name': self.claimer_name,
            'claimer_faculty':self.claimer_faculty,
            'claimer_contact':self.claimer_contact,
            'secret_answer':self.secret_answer,
            'created_at':self.created_at,
            'status':self.status,
         }          

    @classmethod
    def from_dict(cls, data: dict)->'Claim':
        return cls(
            claim_id=data['claim_id'],
            item_id=data['item_id'],
            claimer_username=data['claimer_username'],
            claimer_name=data['claimer_name'],
            claimer_faculty=data['claimer_faculty'],
            claimer_contact=data['claimer_contact'],
            secret_answer=data['secret_answer'],
            created_at=data.get('created_at'),
            status=data.get('status','PENDING'),
        )