from ibm_watsonx_ai.foundation_models import Model
from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
from ibm_watsonx_ai.credentials import Credentials
from app.config import IBM_API_KEY, IBM_CLOUD_URL, IBM_PROJECT_ID, IBM_SPACE_ID

def initialize_watsonx_ai():
    return Model(
    model_id=ModelTypes.GRANITE_13B_CHAT_V2,
    params={
        GenParams.MAX_NEW_TOKENS: 900,
        GenParams.RETURN_OPTIONS: {
            "input_text": True,
            "generated_tokens": True,
        },
    },
    credentials=Credentials(
        api_key=IBM_API_KEY,
        url=IBM_CLOUD_URL,
    ),
    project_id=IBM_PROJECT_ID
)