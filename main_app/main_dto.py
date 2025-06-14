from pydantic import BaseModel
from typing import Optional, Dict

class RenderConfig(BaseModel):
    formato: str      # TEX, PDF, GIF, D3
    paleta: Optional[str] = None

class AnaliseRequest(BaseModel):
    render: RenderConfig
    analises: Dict[str, bool]