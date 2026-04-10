from app.services.sharepoint_service import SharePointService
from app.services.mdm_gpt_service import MDMGPTService
from app.services.gmail_service import GmailService
from app.services.material_code_service import MaterialCodeService
from app.services.workflow_service import WorkflowService
from app.models.schemas import CaseRecord, ProsolReturnInput


def build_workflow():
    sp = SharePointService()
    mdm = MDMGPTService()
    gmail = GmailService()
    mat = MaterialCodeService(sp.material_code_exists)
    return WorkflowService(sp, mdm, gmail, mat)


def test_duplicate_path_happy():
    wf = build_workflow()
    case = CaseRecord(requestId="R1", title="t", senderEmail="a@b.com", emailSubject="s", rawInputText="Need hex bolt m8")
    wf.sharepoint.save_case(case)
    result = wf.run_match("R1")
    assert result.duplicate_confidence == 100
    wf.send_duplicate("R1")
    assert wf.sharepoint.get_case("R1").status.value == "Closed"


def test_clarification_path_happy():
    wf = build_workflow()
    case = CaseRecord(requestId="R2", title="t", senderEmail="a@b.com", emailSubject="s", rawInputText="unknown part ?")
    wf.sharepoint.save_case(case)
    wf.run_match("R2")
    wf.send_clarification("R2", "Please clarify")
    assert wf.sharepoint.get_case("R2").clarificationQuestion == "Please clarify"


def test_new_item_path_happy():
    wf = build_workflow()
    case = CaseRecord(requestId="R3", title="t", senderEmail="a@b.com", emailSubject="s", rawInputText="custom new component")
    wf.sharepoint.save_case(case)
    wf.run_match("R3")
    wf.mark_new_item_required("R3")
    wf.submit_prosol("R3", ProsolReturnInput(unspsc="12345678", shortDescription="New", longDescription="Brand new item"))
    res = wf.create_master_and_send("R3")
    assert res["case"].newABGMaterialCode is not None
    assert res["case"].status.value == "Closed"
