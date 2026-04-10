from fastapi import APIRouter, Depends, HTTPException
from app.dependencies import get_workflow_service
from app.models.schemas import CaseRecord, APIResponse

router = APIRouter(prefix="/cases", tags=["cases"])


@router.get("", response_model=list[CaseRecord])
def list_cases(workflow=Depends(get_workflow_service)):
    return workflow.sharepoint.list_cases()


@router.post("", response_model=CaseRecord)
def create_case(case: CaseRecord, workflow=Depends(get_workflow_service)):
    return workflow.sharepoint.save_case(case)


@router.get("/{request_id}", response_model=CaseRecord)
def get_case(request_id: str, workflow=Depends(get_workflow_service)):
    case = workflow.sharepoint.get_case(request_id)
    if not case:
        raise HTTPException(404, "Case not found")
    return case


@router.post("/{request_id}/match", response_model=APIResponse)
def run_match(request_id: str, workflow=Depends(get_workflow_service)):
    try:
        result = workflow.run_match(request_id)
        return APIResponse(success=True, message="MDM-GPT analysis complete", data=result.model_dump())
    except Exception as e:
        raise HTTPException(400, str(e))
