#!/usr/bin/env python
import sys
import warnings
from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from assistant.crew import Assistant
from pydantic import BaseModel

class CommitPayload(BaseModel):
    commit: str

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

app = FastAPI()

@app.post("/run")
def run_api(payload: CommitPayload):
    """
    Expose generate as an API endpoint.
    Expects JSON: { "commit": "your commit message" }
    """
    try:
        message = payload.commit
        rap = generate(message)
        return JSONResponse(content={"status": "success", "response": rap})
    except Exception as e:
        return JSONResponse(content={"status": "error", "detail": str(e)}, status_code=500)

def run():
    """
    Run the crew.
    """

def generate(message):
    inputs = {
        'msg': message
    }
    try:
        result = Assistant().crew().kickoff(inputs=inputs)
        if not hasattr(result, 'raw') or not isinstance(result.raw, str):
            return "No rap verse was generated."
        return result.raw
    except Exception as e:
        return f"❌ Error: {e}"
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("commit_rapper.main:app", host="0.0.0.0", port=8000, reload=True)



