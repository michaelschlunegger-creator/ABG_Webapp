from pydantic import BaseModel
import os


class Settings(BaseModel):
    app_name: str = os.getenv("APP_NAME", "ABG Web App")
    env: str = os.getenv("ENV", "development")
    mock_mode: bool = os.getenv("MOCK_MODE", "true").lower() == "true"
    internal_api_key: str = os.getenv("INTERNAL_API_KEY", "dev-internal-key")

    sharepoint_site_url: str = os.getenv("SHAREPOINT_SITE_URL", "")
    sharepoint_tenant_id: str = os.getenv("SHAREPOINT_TENANT_ID", "")
    sharepoint_client_id: str = os.getenv("SHAREPOINT_CLIENT_ID", "")
    sharepoint_client_secret: str = os.getenv("SHAREPOINT_CLIENT_SECRET", "")
    sharepoint_master_list: str = os.getenv("SHAREPOINT_MASTER_LIST", "ABG_Master_Reference")
    sharepoint_request_list: str = os.getenv("SHAREPOINT_REQUEST_LIST", "ABG_Cataloguing_Request_Log")

    gmail_client_id: str = os.getenv("GMAIL_CLIENT_ID", "")
    gmail_client_secret: str = os.getenv("GMAIL_CLIENT_SECRET", "")
    gmail_refresh_token: str = os.getenv("GMAIL_REFRESH_TOKEN", "")
    gmail_sender: str = os.getenv("GMAIL_SENDER", "")

    mdm_gpt_api_url: str = os.getenv("MDM_GPT_API_URL", "")
    mdm_gpt_api_key: str = os.getenv("MDM_GPT_API_KEY", "")


settings = Settings()
