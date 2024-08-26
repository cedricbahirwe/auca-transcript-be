from endpoints import login_to_auca, download_transcript
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

app = FastAPI()


class UserCredentials(BaseModel):
    username: str
    password: str


def is_user_valid(credentials: UserCredentials):
    # Basic username and password check (customize this logic)
    # if credentials.username == "23455" and credentials.password == "cedricaganzelucie":
    #     return True
    return True


@app.post("/get-transcript/")
async def get_file(credentials: UserCredentials):
    if is_user_valid(credentials):
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
