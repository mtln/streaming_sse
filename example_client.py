#!/usr/bin/env python3
"""
Example Client for FastAPI SSE Streaming
This script demonstrates how to consume SSE streams from the FastAPI server.
"""

import json
import time

import requests


class SSEClient:
    """Simple SSE client for consuming server-sent events"""

    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def stream_simple(self):
        """Consume the simple stream"""
        print("🔗 Connecting to simple stream...")
        response = requests.get(f"{self.base_url}/stream/simple", stream=True)

        if response.status_code == 200:
            print("✅ Connected! Receiving messages...")
            for line in response.iter_lines():
                if line:
                    line_str = line.decode("utf-8")
                    if line_str.startswith("data: "):
                        data = json.loads(line_str[6:])
                        print(f"📨 [{data['timestamp']}] {data['message']}")

                        if data.get("count", 0) == 10:
                            print("✅ Simple stream completed!")
                            break
        else:
            print(f"❌ Failed to connect: {response.status_code}")

    def stream_progress(self):
        """Consume the progress stream"""
        print("🔗 Connecting to progress stream...")
        response = requests.get(f"{self.base_url}/stream/progress", stream=True)

        if response.status_code == 200:
            print("✅ Connected! Tracking progress...")
            for line in response.iter_lines():
                if line:
                    line_str = line.decode("utf-8")
                    if line_str.startswith("event: progress"):
                        # Get the data line
                        data_line = next(response.iter_lines()).decode("utf-8")
                        if data_line.startswith("data: "):
                            data = json.loads(data_line[6:])
                            print(f"📊 {data['message']} - {data['percentage']}%")

                            if data["percentage"] == 100.0:
                                print("✅ Progress completed!")
                                break
        else:
            print(f"❌ Failed to connect: {response.status_code}")

    def stream_realtime(self, duration=10):
        """Consume the realtime stream for a specified duration"""
        print(f"🔗 Connecting to realtime stream for {duration} seconds...")
        response = requests.get(f"{self.base_url}/stream/realtime", stream=True)

        if response.status_code == 200:
            print("✅ Connected! Receiving sensor data...")
            start_time = time.time()

            for line in response.iter_lines():
                if line:
                    line_str = line.decode("utf-8")
                    if line_str.startswith("event: sensor_data"):
                        # Get the data line
                        data_line = next(response.iter_lines()).decode("utf-8")
                        if data_line.startswith("data: "):
                            data = json.loads(data_line[6:])
                            print(
                                f"🌡️  T: {data['temperature']}°C | 💧 H: {data['humidity']}% | 📊 P: {data['pressure']}hPa"
                            )

                            if time.time() - start_time > duration:
                                print(
                                    f"✅ Realtime stream completed after {duration} seconds!"
                                )
                                break
        else:
            print(f"❌ Failed to connect: {response.status_code}")

    def stream_chat(self):
        """Consume the chat stream"""
        print("🔗 Connecting to chat stream...")
        response = requests.get(f"{self.base_url}/stream/chat", stream=True)

        if response.status_code == 200:
            print("✅ Connected! Chat session started...")
            messages_received = 0

            for line in response.iter_lines():
                if line:
                    line_str = line.decode("utf-8")
                    if line_str.startswith("event: message"):
                        # Get the data line
                        data_line = next(response.iter_lines()).decode("utf-8")
                        if data_line.startswith("data: "):
                            data = json.loads(data_line[6:])
                            messages_received += 1
                            print(f"💬 Bot: {data['text']}")

                            if messages_received >= 5:
                                print("✅ Chat session completed!")
                                break
        else:
            print(f"❌ Failed to connect: {response.status_code}")

    def stream_logs(self, max_logs=10):
        """Consume the log stream"""
        print(f"🔗 Connecting to log stream (max {max_logs} logs)...")
        response = requests.get(f"{self.base_url}/stream/logs", stream=True)

        if response.status_code == 200:
            print("✅ Connected! Receiving logs...")
            logs_received = 0

            for line in response.iter_lines():
                if line:
                    line_str = line.decode("utf-8")
                    if line_str.startswith("event: log"):
                        # Get the data line
                        data_line = next(response.iter_lines()).decode("utf-8")
                        if data_line.startswith("data: "):
                            data = json.loads(data_line[6:])
                            logs_received += 1

                            # Color coding for log levels
                            level_emoji = {
                                "INFO": "ℹ️",
                                "WARNING": "⚠️",
                                "ERROR": "❌",
                                "DEBUG": "🐛",
                            }
                            emoji = level_emoji.get(data["level"], "📝")

                            print(f"{emoji} [{data['level']}] {data['message']}")

                            if logs_received >= max_logs:
                                print(f"✅ Log stream completed after {max_logs} logs!")
                                break
        else:
            print(f"❌ Failed to connect: {response.status_code}")


def main():
    """Run example client"""
    print("🚀 FastAPI SSE Streaming Client Example")
    print("=" * 50)

    client = SSEClient()

    # Test health endpoint first
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Server is running!")
        else:
            print("❌ Server is not responding properly")
            return
    except Exception as e:
        print(f"❌ Cannot connect to server: {e}")
        print("Please make sure the server is running on http://localhost:8000")
        print("Start it with: uvicorn app:app --reload --host 0.0.0.0 --port 8000")
        return

    print("\nChoose a stream to test:")
    print("1. Simple Stream")
    print("2. Progress Stream")
    print("3. Real-time Data Stream")
    print("4. Chat Stream")
    print("5. Log Stream")
    print("6. Run All Streams")

    try:
        choice = input("\nEnter your choice (1-6): ").strip()

        if choice == "1":
            client.stream_simple()
        elif choice == "2":
            client.stream_progress()
        elif choice == "3":
            duration = input("Enter duration in seconds (default 10): ").strip()
            duration = int(duration) if duration.isdigit() else 10
            client.stream_realtime(duration)
        elif choice == "4":
            client.stream_chat()
        elif choice == "5":
            max_logs = input("Enter max number of logs (default 10): ").strip()
            max_logs = int(max_logs) if max_logs.isdigit() else 10
            client.stream_logs(max_logs)
        elif choice == "6":
            print("\n" + "=" * 50)
            print("Running all streams sequentially...")

            print("\n1️⃣ Simple Stream:")
            client.stream_simple()

            print("\n2️⃣ Progress Stream:")
            client.stream_progress()

            print("\n3️⃣ Real-time Data Stream:")
            client.stream_realtime(5)

            print("\n4️⃣ Chat Stream:")
            client.stream_chat()

            print("\n5️⃣ Log Stream:")
            client.stream_logs(5)

            print("\n🎉 All streams completed!")
        else:
            print("❌ Invalid choice. Please run the script again.")

    except KeyboardInterrupt:
        print("\n⏹️  Client stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
