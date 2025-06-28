# FastAPI SSE Streaming Examples

A comprehensive FastAPI application demonstrating Server-Sent Events (SSE) streaming with multiple real-world examples and a beautiful, modern web interface.
This is an educational project by matlon GmbH

## 🚀 Features

- **Multiple SSE Stream Types**: Simple messages, progress tracking, real-time sensor data, chat simulation, and log streaming
- **Modern Web UI**: Beautiful, responsive interface built with Tailwind CSS
- **Real-time Updates**: Live data streaming with proper event handling
- **Interactive Examples**: Click-to-start streaming demos with visual feedback
- **API Documentation**: Auto-generated OpenAPI/Swagger documentation
- **Health Monitoring**: Built-in health check endpoint

## 📋 Prerequisites

- Python 3.8+
- pip (Python package installer)

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd streaming_sse
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv .venv
   ```

3. **Activate the virtual environment**:
   - **Windows**:
     ```bash
     .venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Running the Application

### Development Server
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Production Server
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Docker
```bash
# Build and run with Docker
docker build -t sse-streaming .
docker run -p 8000:8000 sse-streaming

# Or use docker-compose
docker-compose up
```

### Using the Windows Batch File
```bash
start.bat
```

## 🌐 Access Points

- **Web Interface**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📡 SSE Endpoints

### 1. Simple Stream (`/stream/simple`)
Basic SSE stream that sends 10 messages with 1-second intervals.

**Events:**
- `message`: Regular stream messages
- `complete`: Stream completion notification

**Example Response:**
```json
{
  "message": "Simple message #1",
  "timestamp": "2024-01-15T10:30:00.123456",
  "count": 1
}
```

### 2. Progress Stream (`/stream/progress`)
Progress bar simulation with percentage updates and status changes.

**Events:**
- `progress`: Progress updates with percentage and status

**Example Response:**
```json
{
  "percentage": 50.0,
  "current_step": 10,
  "total_steps": 20,
  "status": "almost_done",
  "message": "Processing step 10/20",
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

### 3. Real-time Data (`/stream/realtime`)
Simulated sensor data stream with temperature, humidity, and pressure readings.

**Events:**
- `sensor_data`: Real-time sensor readings

**Example Response:**
```json
{
  "temperature": 24.5,
  "humidity": 65.2,
  "pressure": 1013.8,
  "timestamp": "2024-01-15T10:30:00.123456",
  "unit": {
    "temperature": "°C",
    "humidity": "%",
    "pressure": "hPa"
  }
}
```

### 4. Chat Stream (`/stream/chat`)
Chat message simulation with typing indicators and realistic timing.

**Events:**
- `typing`: Typing indicator status
- `message`: Chat messages
- `complete`: Chat session completion

**Example Response:**
```json
{
  "id": 1,
  "text": "Hello! How can I help you today?",
  "sender": "bot",
  "timestamp": "2024-01-15T10:30:00.123456"
}
```

### 5. Log Stream (`/stream/logs`)
Application log streaming with different severity levels.

**Events:**
- `log`: Log entries with various levels

**Example Response:**
```json
{
  "level": "INFO",
  "message": "Application started successfully",
  "timestamp": "2024-01-15T10:30:00.123456",
  "line_number": 1,
  "service": "api-server"
}
```

## 🎯 Usage Examples

### JavaScript Client Example
```javascript
// Connect to a simple stream
const eventSource = new EventSource('/stream/simple');

eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
};

eventSource.addEventListener('complete', function(event) {
    const data = JSON.parse(event.data);
    console.log('Stream completed:', data.message);
    eventSource.close();
};

eventSource.onerror = function() {
    console.error('Connection error');
    eventSource.close();
};
```

### Python Client Example
```python
import requests
import json

# Stream data from the API
response = requests.get('http://localhost:8000/stream/simple', stream=True)

for line in response.iter_lines():
    if line:
        # Parse SSE format
        if line.startswith(b'data: '):
            data = json.loads(line[6:].decode('utf-8'))
            print(f"Received: {data}")
```

### Curl Examples
```bash
# Test simple stream
curl -N http://localhost:8000/stream/simple

# Test progress stream
curl -N http://localhost:8000/stream/progress

# Test realtime data
curl -N http://localhost:8000/stream/realtime

# Test chat stream
curl -N http://localhost:8000/stream/chat

# Test log stream
curl -N http://localhost:8000/stream/logs
```

## 🏗️ Project Structure

```
streaming_sse/
├── app.py              # FastAPI application with SSE endpoints
├── requirements.txt     # Python dependencies
├── README.md           # This file
├── templates/
│   └── index.html      # Main web interface
├── static/
│   └── style.css       # Additional CSS styles
├── test_sse.py         # Automated testing script
├── example_client.py   # Example client for consuming SSE streams
├── Dockerfile          # Container deployment
├── docker-compose.yml  # Easy development setup
├── start.bat          # Windows startup script
└── .gitignore          # Git ignore file
```

## 🔧 Configuration

The application can be configured through environment variables:

- `HOST`: Server host (default: 0.0.0.0)
- `PORT`: Server port (default: 8000)
- `RELOAD`: Enable auto-reload (default: True in development)

### Environment Variables Example
```bash
export HOST=127.0.0.1
export PORT=8080
uvicorn app:app --reload --host $HOST --port $PORT
```

## 🧪 Testing

### Manual Testing
1. Start the server: `uvicorn app:app --reload --host 0.0.0.0 --port 8000`
2. Open http://localhost:8000 in your browser
3. Click on different stream buttons to test each SSE endpoint
4. Monitor the real-time updates in the web interface

### API Testing
1. Start the server and open http://localhost:8000/docs
2. Use the interactive Swagger UI to test endpoints
3. Use tools like curl or Postman to test SSE streams

### Automated Testing
```bash
# Run the test script
python test_sse.py

# Run the example client
python example_client.py
```

## 🚀 Deployment

### Docker Deployment
```bash
# Build the image
docker build -t sse-streaming .

# Run the container
docker run -p 8000:8000 sse-streaming

# Or use docker-compose
docker-compose up -d
```

### Production Considerations
- Use a production ASGI server like Gunicorn with Uvicorn workers
- Implement proper error handling and logging
- Add authentication and rate limiting for production use
- Consider using Redis or similar for scaling SSE across multiple instances

### Production with Gunicorn
```bash
# Install gunicorn
pip install gunicorn

# Run with multiple workers
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [SSE-Starlette](https://github.com/sysid/sse-starlette) - SSE implementation
- [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS framework
- [Font Awesome](https://fontawesome.com/) - Icons
