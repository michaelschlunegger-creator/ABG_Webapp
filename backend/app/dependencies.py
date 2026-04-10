from functools import lru_cache
from app.core.config import settings
from app.services.sharepoint_service import SharePointService
from app.services.mdm_gpt_service import MDMGPTService
from app.services.gmail_service import GmailService
from app.services.material_code_service import MaterialCodeService
from app.services.workflow_service import WorkflowService


@lru_cache
def get_workflow_service() -> WorkflowService:
    sp = SharePointService(mock_mode=settings.mock_mode)
    mdm = MDMGPTService(mock_mode=settings.mock_mode)
    gmail = GmailService(mock_mode=settings.mock_mode)
    material = MaterialCodeService(sp.material_code_exists)
    return WorkflowService(sp, mdm, gmail, material)
