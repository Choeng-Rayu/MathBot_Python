#!/usr/bin/env python3
"""
Development server with auto-restart functionality
Similar to nodemon for Node.js
"""

import os
import sys
import time
import subprocess
import signal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class BotRestartHandler(FileSystemEventHandler):
    def __init__(self, script_path):
        self.script_path = script_path
        self.process = None
        self.restart_bot()
        
    def on_modified(self, event):
        if event.is_directory:
            return
            
        # Only restart for Python files
        if event.src_path.endswith('.py'):
            print(f"\n🔄 File changed: {event.src_path}")
            print("🔄 Restarting bot...")
            self.restart_bot()
    
    def restart_bot(self):
        # Kill existing process
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
            except:
                pass
        
        # Start new process
        try:
            print(f"🚀 Starting bot: python {self.script_path}")
            self.process = subprocess.Popen([sys.executable, self.script_path])
            print(f"✅ Bot started with PID: {self.process.pid}")
        except Exception as e:
            print(f"❌ Failed to start bot: {e}")
    
    def stop(self):
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait()
            except:
                pass

def main():
    script_path = "run.py"  # Your main bot script
    
    if not os.path.exists(script_path):
        print(f"❌ Script not found: {script_path}")
        return
    
    print("🔧 Python Bot Development Server")
    print("=" * 40)
    print(f"📁 Watching: {os.getcwd()}")
    print(f"🎯 Script: {script_path}")
    print("🔄 Auto-restart enabled")
    print("🛑 Press Ctrl+C to stop")
    print("=" * 40)
    
    # Create event handler
    event_handler = BotRestartHandler(script_path)
    
    # Create observer
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping development server...")
        event_handler.stop()
        observer.stop()
        print("✅ Development server stopped")
    
    observer.join()

if __name__ == "__main__":
    main()
