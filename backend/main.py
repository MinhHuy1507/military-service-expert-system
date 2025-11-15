from fastapi import FastAPI
from models.query_models import CitizenFacts
from inference_engine_v4 import InferenceEngine

app = FastAPI(title="Hệ cơ sở tri thức hỗ trợ tuyển chọn và tư vấn nghĩa vụ quân sự", version="1.0.0")

try:
    engine = InferenceEngine("data/CSTT_v5.json")
except Exception as e:
    print(f"Không thể nạp Bộ suy diễn. Lỗi: {e}")
    engine = None

@app.get("/")
def read_root():
    return ["Chào mừng đến với Backend của hệ cơ sở tri thức hỗ trợ tuyển chọn và tư vấn nghĩa vụ quân sự!"]

@app.post("/consult")
def run_consultation(facts: CitizenFacts):
    """
    Main endpoint for running the consultation.
    Accepts 32 input facts and returns the inference results.
    """
    if not engine:
        return {"error": "Lỗi: Bộ suy diễn chưa được nạp. Kiểm tra file CSTT_v4.json."}
    
    initial_facts = facts.dict()
    ket_luan, giai_thich, solution_trace = engine.evaluate(initial_facts)
    
    # Filter intermediate rules to send to the frontend
    relevant_rules = [
        rule for rule in solution_trace.values() 
        if not rule['id'].startswith("R_FINAL")
    ]
    
    return {
        "ket_luan": ket_luan,
        "giai_thich": giai_thich,
        "trace": relevant_rules
    }