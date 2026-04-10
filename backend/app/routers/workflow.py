from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.dependencies import get_workflow_service
from app.models.schemas import APIResponse, ProsolReturnInput

router = APIRouter(prefix="/workflow", tags=["workflow"])


class ClarificationBody(BaseModel):
    question: str


@router.post("/{request_id}/duplicate/send", response_model=APIResponse)
def send_duplicate(request_id: str, workflow=Depends(get_workflow_service)):
    try:
        sent = workflow.send_duplicate(request_id)
        return APIResponse(success=True, message="Duplicate email sent", data=sent)
    except Exception as e:
        raise HTTPException(400, str(e))


@router.post("/{request_id}/clarification/send", response_model=APIResponse)
def send_clarification(request_id: str, body: ClarificationBody, workflow=Depends(get_workflow_service)):
    try:
        sent = workflow.send_clarification(request_id, body.question)
        return APIResponse(success=True, message="Clarification email sent", data=sent)
    except Exception as e:
        raise HTTPException(400, str(e))


@router.post("/{request_id}/mark-new", response_model=APIResponse)
def mark_new(request_id: str, workflow=Depends(get_workflow_service)):
    try:
        case = workflow.mark_new_item_required(request_id)
        return APIResponse(success=True, message="Marked as new record required", data=case.model_dump())
    except Exception as e:
        raise HTTPException(400, str(e))


@router.post("/{request_id}/prosol", response_model=APIResponse)
def submit_prosol(request_id: str, payload: ProsolReturnInput, workflow=Depends(get_workflow_service)):
    try:
        case = workflow.submit_prosol(request_id, payload)
        return APIResponse(success=True, message="PROSOL output saved", data=case.model_dump())
    except Exception as e:
        raise HTTPException(400, str(e))


@router.post("/{request_id}/finalize", response_model=APIResponse)
def finalize_new_record(request_id: str, workflow=Depends(get_workflow_service)):
    try:
        result = workflow.create_master_and_send(request_id)
        return APIResponse(success=True, message="New master record created and email sent", data={"newCode": result['case'].newABGMaterialCode})
    except Exception as e:
        raise HTTPException(400, str(e))
