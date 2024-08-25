from endpoints import login_to_auca, download_transcript
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

app = FastAPI()


class UserCredentials(BaseModel):
    username: str
    password: str


def authenticate_user(credentials: UserCredentials):
    # Basic username and password check (customize this logic)
    if credentials.username == "23455" and credentials.password == "cedricaganzelucie":
        return True
    return False


@app.post("/get-transcript/")
async def get_file(credentials: UserCredentials):
    if authenticate_user(credentials):
        response = await login_to_auca(credentials.username, credentials.password)
        session_id = str(response.get("session_id"))
        file_response = await download_transcript(session_id)

        if "pdf_content" in file_response:
            return Response(
                content=file_response["pdf_content"],
                media_type="application/pdf",
                headers={
                    "Content-Disposition": "attachment; filename=transcript.pdf"}
            )
        else:
            partial_response = str(file_response.get(
                "response_text", "No response text available"))

            raise HTTPException(
                status_code=500,
                detail=(
                    f"Failed to retrieve the PDF. Here is the partial response: "
                    f"{partial_response}"
                )
            )

    raise HTTPException(status_code=401, detail="Invalid credentials")

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
