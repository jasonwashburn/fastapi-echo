import json

from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/{path:path}")
@app.post("/{path:path}")
async def get_root(request: Request, path: str, body: bytes | None = None):
    request_headers = dict(request.headers)
    query_params = dict(request.query_params)
    request_info: dict[str, str | dict | None | bytes] = {}
    host = getattr(request.client, "host", None)
    port = getattr(request.client, "port", None)
    cookies = dict(request.cookies)
    raw_body = await request.body() or None
    decoded_body: str | None = None
    if raw_body:
        try:
            decoded_body = json.loads(raw_body.decode())
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass
    method = request.method

    request_info["method"] = method

    request_info["body"] = {"raw": raw_body, "decoded": decoded_body}
    request_info["client"] = {"host": host, "port": port}
    request_info["path"] = path
    request_info["headers"] = request_headers
    request_info["cookies"] = cookies
    request_info["query_params"] = query_params
    return {"request": request_info}
