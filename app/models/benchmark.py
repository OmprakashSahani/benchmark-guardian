from pydantic import BaseModel


class BenchmarkRequest(BaseModel):
    baseline: float
    current: float
    threshold_percent: float = 5.0


class BenchmarkAnalysis(BaseModel):
    baseline: float
    current: float
    change_percent: float
    regression: bool
    severity: str


class AnalyzeResponse(BaseModel):
    analysis: BenchmarkAnalysis
    report: str
