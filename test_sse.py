#!/usr/bin/env python3
"""
Test script for FastAPI SSE Streaming Examples
This script tests all SSE endpoints to ensure they work correctly.
"""

import json
import time

import requests


def test_health_endpoint():
    """Test the health check endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data['status']}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False


def test_simple_stream():
    """Test the simple stream endpoint"""
    print("\n🔍 Testing simple stream...")
    try:
        response = requests.get("http://localhost:8000/stream/simple", stream=True)
        if response.status_code == 200:
            message_count = 0
            for line in response.iter_lines():
                if line:
                    line_str = line.decode("utf-8")
                    if line_str.startswith("data: "):
                        data = json.loads(line_str[6:])
                        message_count += 1
                        print(f"📨 Message {message_count}: {data['message']}")

                        if data.get("count", 0) == 10:
                            print("✅ Simple stream completed successfully")
                            return True
            print("❌ Simple stream did not complete as expected")
            return False
        else:
            print(f"❌ Simple stream failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Simple stream error: {e}")
        return False


def test_progress_stream():
    """Test the progress stream endpoint"""
    print("\n🔍 Testing progress stream...")
    try:
        response = requests.get("http://localhost:8000/stream/progress", stream=True)
        if response.status_code == 200:
            progress_events = 0
            iterator = response.iter_lines()
            for line in iterator:
                if line:
                    line_str = line.decode("utf-8")
                    if line_str.startswith("event: progress"):
                        # Get the next line which should contain the data
                        try:
                            next_line = next(iterator)
                            if next_line:
                                next_line_str = next_line.decode("utf-8")
                                if next_line_str.startswith("data: "):
                                    data = json.loads(next_line_str[6:])
                                    progress_events += 1
                                    print(
                                        f"📊 Progress {data['percentage']}%: {data['message']}"
                                    )

                                    if data["percentage"] == 100.0:
                                        print("✅ Progress stream completed successfully")
                                        return True
                        except StopIteration:
                            break
            print("❌ Progress stream did not complete as expected")
            return False
        else:
            print(f"❌ Progress stream failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Progress stream error: {e}")
        return False


def test_realtime_stream():
    """Test the realtime stream endpoint"""
    print("\n🔍 Testing realtime stream...")
    try:
        response = requests.get("http://localhost:8000/stream/realtime", stream=True)
        if response.status_code == 200:
            sensor_events = 0
            start_time = time.time()
            iterator = response.iter_lines()
            
            for line in iterator:
                if line:
                    line_str = line.decode("utf-8")
                    if line_str.startswith("event: sensor_data"):
                        # Get the next line which should contain the data
                        try:
                            next_line = next(iterator)
                            if next_line:
                                next_line_str = next_line.decode("utf-8")
                                if next_line_str.startswith("data: "):
                                    data = json.loads(next_line_str[6:])
                                    sensor_events += 1
                                    print(
                                        f"🌡️ Sensor data {sensor_events}: {data['temperature']}°C, {data['humidity']}%, {data['pressure']}hPa"
                                    )
                                    
                                    # Test for 5 seconds
                                    if time.time() - start_time > 5:
                                        print(
                                            "✅ Realtime stream working (tested for 5 seconds)"
                                        )
                                        return True
                        except StopIteration:
                            break
            print("❌ Realtime stream did not work as expected")
            return False
        else:
            print(f"❌ Realtime stream failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Realtime stream error: {e}")
        return False


def test_chat_stream():
    """Test the chat stream endpoint"""
    print("\n🔍 Testing chat stream...")
    try:
        response = requests.get("http://localhost:8000/stream/chat", stream=True)
        if response.status_code == 200:
            messages_received = 0
            iterator = response.iter_lines()
            for line in iterator:
                if line:
                    line_str = line.decode("utf-8")
                    if line_str.startswith("event: message"):
                        # Get the next line which should contain the data
                        try:
                            next_line = next(iterator)
                            if next_line:
                                next_line_str = next_line.decode("utf-8")
                                if next_line_str.startswith("data: "):
                                    data = json.loads(next_line_str[6:])
                                    messages_received += 1
                                    print(
                                        f"💬 Chat message {messages_received}: {data['text'][:50]}..."
                                    )
                                    
                                    if messages_received >= 5:
                                        print("✅ Chat stream completed successfully")
                                        return True
                        except StopIteration:
                            break
            print("❌ Chat stream did not complete as expected")
            return False
        else:
            print(f"❌ Chat stream failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Chat stream error: {e}")
        return False


def test_log_stream():
    """Test the log stream endpoint"""
    print("\n🔍 Testing log stream...")
    try:
        response = requests.get("http://localhost:8000/stream/logs", stream=True)
        if response.status_code == 200:
            log_events = 0
            iterator = response.iter_lines()
            for line in iterator:
                if line:
                    line_str = line.decode("utf-8")
                    if line_str.startswith("event: log"):
                        # Get the next line which should contain the data
                        try:
                            next_line = next(iterator)
                            if next_line:
                                next_line_str = next_line.decode("utf-8")
                                if next_line_str.startswith("data: "):
                                    data = json.loads(next_line_str[6:])
                                    log_events += 1
                                    print(
                                        f"📝 Log {log_events} [{data['level']}]: {data['message']}"
                                    )
                                    
                                    if log_events >= 10:
                                        print("✅ Log stream working (received 10+ logs)")
                                        return True
                        except StopIteration:
                            break
            print("❌ Log stream did not work as expected")
            return False
        else:
            print(f"❌ Log stream failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Log stream error: {e}")
        return False


def main():
    """Run all tests"""
    print("🚀 Starting FastAPI SSE Streaming Tests")
    print("=" * 50)

    # Check if server is running
    if not test_health_endpoint():
        print("\n❌ Server is not running. Please start the server first:")
        print("   python main.py")
        return

    # Run all stream tests
    tests = [
        test_simple_stream,
        test_progress_stream,
        test_realtime_stream,
        test_chat_stream,
        test_log_stream,
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except KeyboardInterrupt:
            print("\n⏹️  Tests interrupted by user")
            break
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! SSE streaming is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the server logs.")


if __name__ == "__main__":
    main()
