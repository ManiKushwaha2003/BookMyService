from langchain.tools import tool
from apps.services.models import Service

@tool
def get_service():
    """Get all available service names from the BookMyService database."""

    return list(Service.objects.values_list("name",flat=True))


