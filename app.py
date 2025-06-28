import asyncio
import json
from collections.abc import AsyncGenerator
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sse_starlette.sse import EventSourceResponse

app = FastAPI(
    title="FastAPI SSE Streaming Example",
    description="A comprehensive example demonstrating Server-Sent Events (SSE) streaming with FastAPI",
    version="1.0.0",
)

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Main page with SSE examples"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/stream/simple")
async def simple_stream() -> EventSourceResponse:
    """Simple SSE stream that sends 10 messages with 1-second intervals"""

    async def event_generator() -> AsyncGenerator[dict, None]:
        for i in range(10):
            # Simulate some processing time
            await asyncio.sleep(1)

            data = {
                "message": f"Simple message #{i + 1}",
                "timestamp": datetime.now().isoformat(),
                "count": i + 1,
            }

            yield {"event": "message", "data": json.dumps(data)}

        # Send completion event
        yield {
            "event": "complete",
            "data": json.dumps({"message": "Stream completed successfully"}),
        }

    return EventSourceResponse(event_generator())


@app.get("/stream/progress")
async def progress_stream() -> EventSourceResponse:
    """Progress bar simulation with percentage updates"""

    async def event_generator() -> AsyncGenerator[dict, None]:
        total_steps = 20

        for i in range(total_steps + 1):
            await asyncio.sleep(0.5)

            percentage = (i / total_steps) * 100
            status = "processing"

            if i == total_steps:
                status = "completed"
            elif percentage > 50:
                status = "almost_done"

            data = {
                "percentage": round(percentage, 1),
                "current_step": i,
                "total_steps": total_steps,
                "status": status,
                "message": f"Processing step {i}/{total_steps}",
                "timestamp": datetime.now().isoformat(),
            }

            yield {"event": "progress", "data": json.dumps(data)}

    return EventSourceResponse(event_generator())


@app.get("/stream/realtime")
async def realtime_stream() -> EventSourceResponse:
    """Real-time data stream (simulates sensor data or live updates)"""

    async def event_generator() -> AsyncGenerator[dict, None]:
        import random

        for _ in range(30):  # Stream for 30 seconds
            await asyncio.sleep(1)

            # Simulate sensor data
            temperature = round(random.uniform(20, 30), 2)
            humidity = round(random.uniform(40, 80), 2)
            pressure = round(random.uniform(1000, 1020), 2)

            data = {
                "temperature": temperature,
                "humidity": humidity,
                "pressure": pressure,
                "timestamp": datetime.now().isoformat(),
                "unit": {"temperature": "°C", "humidity": "%", "pressure": "hPa"},
            }

            yield {"event": "sensor_data", "data": json.dumps(data)}

    return EventSourceResponse(event_generator())


@app.get("/stream/chat")
async def chat_stream() -> EventSourceResponse:
    """Chat message simulation with typing indicators"""

    async def event_generator() -> AsyncGenerator[dict, None]:
        messages = [
            "Hello! How can I help you today?",
            "I'm here to assist with any questions you might have.",
            "Feel free to ask anything about our services.",
            "I hope you're having a great day!",
            "Is there anything specific you'd like to know?",
        ]

        for i, message in enumerate(messages):
            # Send typing indicator
            yield {
                "event": "typing",
                "data": json.dumps(
                    {
                        "is_typing": True,
                        "message": "Bot is typing...",
                        "timestamp": datetime.now().isoformat(),
                    }
                ),
            }

            # Simulate typing time
            await asyncio.sleep(2)

            # Send the actual message
            yield {
                "event": "message",
                "data": json.dumps(
                    {
                        "id": i + 1,
                        "text": message,
                        "sender": "bot",
                        "timestamp": datetime.now().isoformat(),
                    }
                ),
            }

            # Stop typing indicator
            yield {
                "event": "typing",
                "data": json.dumps(
                    {"is_typing": False, "timestamp": datetime.now().isoformat()}
                ),
            }

            await asyncio.sleep(1)

        # Send completion
        yield {
            "event": "complete",
            "data": json.dumps(
                {"message": "Chat session completed", "total_messages": len(messages)}
            ),
        }

    return EventSourceResponse(event_generator())


@app.get("/stream/logs")
async def log_stream() -> EventSourceResponse:
    """Log streaming simulation with different log levels"""

    async def event_generator() -> AsyncGenerator[dict, None]:
        import random

        log_levels = ["INFO", "WARNING", "ERROR", "DEBUG"]
        log_messages = [
            "Application started successfully",
            "Database connection established",
            "User authentication successful",
            "Cache miss - fetching from database",
            "API rate limit approaching",
            "Background task completed",
            "Memory usage: 45%",
            "Network request timeout",
            "Configuration updated",
            "Service health check passed",
        ]

        for i in range(15):
            await asyncio.sleep(0.8)

            level = random.choice(log_levels)
            message = random.choice(log_messages)

            data = {
                "level": level,
                "message": message,
                "timestamp": datetime.now().isoformat(),
                "line_number": i + 1,
                "service": "api-server",
            }

            yield {"event": "log", "data": json.dumps(data)}

    return EventSourceResponse(event_generator())


@app.get("/stream/datetime")
async def datetime_stream() -> EventSourceResponse:
    """Infinite datetime stream that sends current datetime every 30 seconds"""

    async def event_generator() -> AsyncGenerator[dict, None]:
        while True:  # Infinite loop to keep the stream alive
            # Send current datetime
            data = {
                "datetime": datetime.now().isoformat(),
                "message": "Current server time",
                "interval": "30 seconds",
            }

            yield {"event": "datetime", "data": json.dumps(data)}

            # Wait 30 seconds before next update
            await asyncio.sleep(30)

    return EventSourceResponse(event_generator())


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "FastAPI SSE Streaming Server",
    }
