from datetime import datetime
from models.constants import ITEM_STATUSES

class ItemReport:
    def __init__(
        self,
        item_id: str,
        report_type: str,
        title: str,
        category: str,
        location: str,
        location_detail: str,
        description: str,
        reporter_username: str,
        reporter_name: str,
        reporter_faculty: str,
        created_at: str | None = None,
        status: str = "OPEN",
        ktm_npm: str | None = None,
    ):
        self.item_id=item_id
        self.report_type=report_type
        self.title=title
        self.category=category
        self.location=location
        self.location_detail=location_detail
        self.description=description
        self.reporter_username=reporter_username
        self.reporter_name=reporter_name
        self.reporter_faculty=reporter_faculty
        self.created_at=created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status=status
        self.ktm_npm=ktm_npm

    def mark_status(self, new_status: str) -> None:
        if new_status not in ITEM_STATUSES:
            raise ValueError(f"Status '{new_status}' tidak valid!")
        else:
            self.status=new_status

    def to_dict(self) -> dict:
        return {
            'item_id': self.item_id,
            'report_type': self.report_type,
            'title': self.title,
            'category': self.category,
            'location': self.location,
            'location_detail': self.location_detail,
            'description': self.description,
            'reporter_username':self.reporter_username,
            'reporter_name':self.reporter_name,
            'reporter_faculty':self.reporter_faculty,
            'created_at': self.created_at,
            'status':self.status,
            'ktm_npm':self.ktm_npm
        }

class LostReport(ItemReport):
    def __init__(
        self,
        item_id: str,
        title: str,
        category: str,
        location: str,
        location_detail: str,
        description: str,
        reporter_username: str,
        reporter_name: str,
        reporter_faculty: str,
        lost_time_estimate: str,
        owner_contact: str,
        created_at: str | None = None,
        status: str = "OPEN",
        ktm_npm: str | None = None,
    ):
        super().__init__(
            item_id=item_id,
            report_type="LOST",
            title=title,
            category=category,
            location=location,
            location_detail=location_detail,
            description=description,
            reporter_username=reporter_username,
            reporter_name=reporter_name,
            reporter_faculty=reporter_faculty,
            created_at=created_at,
            status=status,
            ktm_npm=ktm_npm,
        )
        self.lost_time_estimate=lost_time_estimate
        self.owner_contact=owner_contact

    def to_dict(self) -> dict:
        data = super().to_dict()
        data['lost_time_estimate']=self.lost_time_estimate
        data['owner_contact']=self.owner_contact
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "LostReport":
        return cls(
            item_id=data['item_id'],
            title=data['title'],
            category=data['category'],
            location=data['location'],
            location_detail=data['location_detail'],
            description=data['description'],
            reporter_username=data['reporter_username'],
            reporter_name=data['reporter_name'],
            reporter_faculty=data['reporter_faculty'],
            lost_time_estimate=data['lost_time_estimate'],
            owner_contact=data['owner_contact'],
            created_at=data.get('created_at'),
            status=data.get('status', 'OPEN'),
            ktm_npm=data.get('ktm_npm'),
        )


class FoundReport(ItemReport):
    def __init__(
        self,
        item_id: str,
        title: str,
        category: str,
        location: str,
        location_detail: str,
        description: str,
        reporter_username: str,
        reporter_name: str,
        reporter_faculty: str,
        original_img_path: str,
        blurred_img_path: str,
        secret_question: str,
        handoff_method: str,
        finder_contact: str,
        dropoff_location_detail: str = "",
        created_at: str | None = None,
        status: str = "OPEN",
        ktm_npm: str | None = None,
    ):
        super().__init__(
            item_id=item_id, 
            report_type='FOUND',
            title=title, 
            category=category, 
            location=location, 
            location_detail=location_detail,
            description=description, 
            reporter_username=reporter_username, 
            reporter_name=reporter_name, 
            reporter_faculty=reporter_faculty,
            created_at=created_at,
            status=status,
            ktm_npm=ktm_npm
            )
        self.original_img_path=original_img_path
        self.blurred_img_path=blurred_img_path
        self.secret_question=secret_question
        self.handoff_method=handoff_method
        self.finder_contact=finder_contact
        self.dropoff_location_detail=dropoff_location_detail

    def to_dict(self) -> dict:
        data=super().to_dict()
        data['original_img_path']=self.original_img_path
        data['blurred_img_path']=self.blurred_img_path
        data['secret_question']=self.secret_question
        data['handoff_method']=self.handoff_method
        data['finder_contact']=self.finder_contact
        data['dropoff_location_detail']=self.dropoff_location_detail
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "FoundReport":
        return cls(
            item_id=data['item_id'],
            title=data["title"],
            category=data["category"],
            location=data["location"],
            location_detail=data["location_detail"],
            description=data["description"],
            reporter_username=data["reporter_username"],
            reporter_name=data["reporter_name"],
            reporter_faculty=data["reporter_faculty"],
            original_img_path=data["original_img_path"],
            blurred_img_path=data["blurred_img_path"],
            secret_question=data["secret_question"],
            handoff_method=data["handoff_method"],
            finder_contact=data["finder_contact"],
            dropoff_location_detail=data.get("dropoff_location_detail", ""),
            created_at=data.get("created_at"),
            status=data.get("status", "OPEN"),
            ktm_npm=data.get("ktm_npm"),
        )


def item_from_dict(data: dict) -> ItemReport:
    # Cek data.get("report_type") -> "LOST" atau "FOUND"
    report_type= data.get('report_type')
    if report_type == 'LOST':
        return LostReport.from_dict(data)
    elif report_type == 'FOUND':
        return FoundReport.from_dict(data)
    raise ValueError(f'Tipe laporan tidak valid: {report_type}')