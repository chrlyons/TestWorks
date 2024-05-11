from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState
from jose import jwt, JWTError
from app.crud import SECRET_KEY, ALGORITHM, redis_client, get_user_by_username
import asyncio
import json

websocket_router = APIRouter()


@websocket_router.websocket("/ws/{email}")
async def websocket_endpoint(websocket: WebSocket, email: str):
    await websocket.accept()
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)
        return "Token is required"

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email_in_token = payload.get("sub")
        if email != email_in_token:
            await websocket.close(code=1003)
            return "Invalid email or token mismatch"
    except JWTError as e:
        await websocket.close(code=1008)
        return f"JWT Error: {str(e)}"

    user = get_user_by_username(username=email)
    if user is None:
        await websocket.close(code=1008)
        return "User not found"

    try:
        redis_key = str(user.id)
        while websocket.client_state != WebSocketState.DISCONNECTED:
            exists = redis_client.exists(redis_key)
            ttl = redis_client.ttl(redis_key)
            if exists and ttl != -2:
                message = json.dumps(
                    {"message": f"Remaining session time: {ttl} seconds"}
                )
            else:
                message = json.dumps({"message": "Session expired or not found"})
            await websocket.send_text(message)
            await asyncio.sleep(60)
    except WebSocketDisconnect:
        print(f"WebSocket disconnected for user {user.username}")
    except Exception as e:
        print(f"WebSocket error for user {user.username}: {e}")
    finally:
        if websocket.client_state != WebSocketState.DISCONNECTED:
            await websocket.close()
            print(f"WebSocket forcibly closed for user {user.username}")
