import httpx
from fastapi import HTTPException


async def login_to_auca(username: str, password: str):
    url = 'https://registration.auca.ac.rw/Login'

    headers = {
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://registration.auca.ac.rw',
        'Referer': 'https://registration.auca.ac.rw/Login',
        'Upgrade-Insecure-Requests': '1',
    }

    # TODO: Understand how these work
    data = {
        '__VIEWSTATE': 'pS1CVcZ7wFj+gTORwRe96e5sGVp6XgkKUf4g7GetO2nwQjC2vliFZVyp6IFIUyLN4SU7jxyFA05i1xhPea8zXHm5QZCy7fFtX+0KTUkPoZ2sjEnyo5UZQXCVu/lm8Q77xXFooUHWYpA1obMyvL1iJJPvLeuwbq1DKPfA5uYz9ys=',
        '__VIEWSTATEGENERATOR': 'C2EE9ABB',
        '__EVENTVALIDATION': 'FjFD/5o2QCPG5DNFfp2LLYhP+uSfppzcLSuqQHONXwsP0006rWBw/bk92Mti3nM7G0wb+WqSz4JygXGoTbm1Nd2kVhGq6QWoCaoOOJ3bKJwncRIKje86z1k1dJqoLwAIYGcm3zlCqJdm9Z2VfY1xXRokJiWPvUHCR/gWfWt/kLpIFr7q1tj6E+mKIRwK/1sy',
        'txtUsername': username,
        'txtPassword': password,
        'btnLogin': 'Sign In'
    }

    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(url, headers=headers, data=data)

        # Extract cookies from the response
        cookies = client.cookies.jar

        # Look for the ASP.NET_SessionId cookie
        session_id = client.cookies.get('ASP.NET_SessionId')

        # Return the response text, cookies, and the session ID
        return {
            "status_code": response.status_code,
            "response_text": response.text,
            "cookies": cookies,
            "session_id": session_id
        }


async def download_transcript(session_id: str):
    file_url = 'https://registration.auca.ac.rw/StudentHome'

    file_headers = {
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': f'ASP.NET_SessionId={session_id}',
        'Origin': 'https://registration.auca.ac.rw',
        'Referer': 'https://registration.auca.ac.rw/StudentHome',
        'Upgrade-Insecure-Requests': '1',
    }

    # TODO: Understand how these work
    file_data = {
        '__EVENTTARGET': 'lbTranscript',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': 'mk+WcNPa7WJ+qMjBgcIDF4B7XtHceojTVarA1VU0R0dnLKaWWVJphiPZCnwvBrQjnlzX9sGqp+gZxFxqpbw54MyrVbx6668v2LaH/63OCJBaC5zNJBcepJAhrm7whuNN8rN21ItPpITK+9a/5gll1FrQAje6+KFJDEME/SfW/ZzODaGyXa8X7E7OqRC0blo/O+4e4rA+wxMWnRNt4zXeJAxO9eDcVlWRf26lFScA1HIRYoStqjUlUCjzs2Qbkn+xY8w1A8/QspawJxoBLRsLvsNDY+2ge3+XCVHeJFWFgoUjTwwGJE0ayU2k/lQjaL6G8JzIApy41S+uI6HKp0J9oMJiz8TAfzBq0gJKCH7zH6N9PPKRQdsUktK2WAdFtqrrnncsgc+eTlHnYBITR7Vbjjg3SBFs63wbs0jt3HUD/NfSAiVJzvYMgd8FwKBTso2DmOtnSST3KouQLiSz/go8o5+qMJ8nr3AUwDQ4mS6E0eX0FlLsdbCD6CIYV4+XtOy3qZB083sYamQlzoYe1Frm9CV3ieREJ5vKJMqcdDzL/mnd8XBDeK/ErDeWF7OJr5Yn2h5fmnbF5xyy478kWi7xxjGBAbTrJ96kbvcigdreKUMJLiMEyykHFmBF1jMngJ8L6ot2ajKkNHdROxPeDelwU33blzL/lkBz8fy0O5zTX7S6OXxWiDz+pk0gH0Fwcy/AyuO/dsIno/VkYbjxymvHRJ5beA4bALgqS1h/Zq4aC5siYC0iQvyepUjuBJZLkdqZo/SKvx+8u+KQ7kwYjbMIv9XuxbWRvfs15vaRzBULuztSya/5KOvl1Q5/P7h7sdOSR+YkffMeF0ZL+PoNVYnOKNted0h22ha7AHV+l3OJyKxl+zecBbAxw5MP9cv03wwY5sa5D3viqcrtdmejI4NVEL89SLbaU/+rumg1GoQANQXsRoc2o682wh4lD88um1/qHbWrj86ORqNsuyFfrN0doqOfx3ciwxtVHhy99/1uUEwrg6V4skTpIwTlXa7Yuz/TSKtLXMYSOQOd28mH4ZugEQPBixl1Y7a85f4MMSt0Ob2VDdqruVb+wZg6+zL4OwO2pveDMpS5wzbJ4zUrSvbn5jTIRSOqJq7S9CZBtm1eOH3C7uXuSmBQkbJ8xP0UEq2+uJBsT7NVM7eR1Vmy4sIYEobPTTrmwZnT/mP0jKTisvTi7LauIxuQYbykFNwkf9X/xhDMLrqArQquKZ+WA4KWJpXXRUJj1L6u6BF1idUFtLGVEVo3qOeReMpXAaKBKsIwv8sMwAAo+GZ0xT6QGWohVhfnCbtBYnimwVaXB/5nOJBIZZXKj3NCe1xxs+tLPt7Ds3AVshQhl0JG6mGHhhFfqe49DV275oGxlEmYDsh8+xoqNIQBnCp6AOUSrl4M/ii2g7aTwZ6L9TPpTtPYgu/qEol2j/NB7hissHG1msOhb1ZP+/A7JuCtB7JKBw0DG2mig1OoXCE0skT4MDvy4CrVVVSZ67yJpEtouH0adPOkeS5SgKJKQSXff8T/zvwMTEd6r16TExsmpfz7c0Osvm78UHAOSnLV3Uig9F0OetZHB7nI0X+cPbkFIgzoV6fwTDG5KdmbbNVFGiKyC3r9yQx6CA==',
        '__VIEWSTATEGENERATOR': 'BDF28829',
        '__EVENTVALIDATION': 'DJ9kjoSUySbRa3674iSsrdJtj0uNpobT/T5qx6uVB/zYykZpaZsW92sCFka331RqEm49rdGNLRTZ7IHhfEDDvGH4i6tS405wqgieM4wAWykv+Np+Ab2sJdP/hippufeQA76VmkhY9Cn/7mDxqSeehtjqMsyiS3M8bwBVRxLk+6FZ7Nmun5MvuwLXJgtQpx7X9gZhUNg9mdE4ApGZHUxEWAZYtQSA6nuurHJMGzEsLUcYQIsVOWnzHuTHkjmTjCmGpXf9A+CzKfSZocNsRYd4F/8l4e3hfS5AoWTKvNk7RQbGKh8GiOCyfixQ2NjeDFOp'
    }

    async with httpx.AsyncClient(verify=False) as client:
        response = await client.post(file_url, headers=file_headers, data=file_data, follow_redirects=True)

        # Check if the response is a PDF
        content_type = response.headers.get('Content-Type', '')
        if 'application/pdf' in content_type:
            return {
                "status_code": response.status_code,
                "content_type": content_type,
                "pdf_content": response.content
            }
            # Save the PDF to testing purpose
            # with open('transcript.pdf', 'wb') as f:
            #     f.write(response.content)
            # return "PDF saved as transcript.pdf"
        else:
            # Throw an HTTPException if the response is not a PDF
            raise HTTPException(
                status_code=500,
                detail=f"Expected a PDF but received a response with Content-Type: {
                    content_type}. Here is the partial response: {response.text[:500]}"
            )
