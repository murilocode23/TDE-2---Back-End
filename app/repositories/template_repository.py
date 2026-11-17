from app.models.template import Template
from app.repositories.base_repository import BaseRepository


class TemplateRepository(BaseRepository):
    model = Template
