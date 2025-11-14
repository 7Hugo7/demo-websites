#!/usr/bin/env python3
"""
Demo Website Builder - CLI Version (Uses Claude Code CLI instead of API)
Much cheaper! Uses your existing Claude Code subscription.
"""

import os
import sys
import subprocess
import time
from pathlib import Path
from typing import Optional
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTextEdit, QLabel, QSplitter, QMessageBox
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QUrl, QProcess

# Configuration
DEMOS_DIR = Path(__file__).parent.parent / "demos"
TEMPLATE_DIR = DEMOS_DIR / "template"
WORKFLOW_PATH = TEMPLATE_DIR / "WORKFLOW.md"


class ClaudeWorker(QThread):
    """Background thread for Claude CLI"""
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(str, str)  # project_name, dev_url
    error_signal = pyqtSignal(str)

    def __init__(self, url: str, change_request: Optional[str] = None, project_name: Optional[str] = None):
        super().__init__()
        self.url = url
        self.change_request = change_request
        self.project_name = project_name
        self.process = None
        self.dev_process = None

    def log(self, message: str):
        """Emit log message to UI"""
        self.log_signal.emit(message)
        print(f"[LOG] {message}")

    def run(self):
        """Main worker thread execution"""
        try:
            # Check if claude CLI is available
            result = subprocess.run(
                ["which", "claude"],
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                self.error_signal.emit(
                    "Claude CLI not found. Please install Claude Code:\n"
                    "https://docs.anthropic.com/claude/docs/claude-code"
                )
                return

            # Read workflow
            with open(WORKFLOW_PATH, 'r') as f:
                workflow = f.read()

            # Build prompt
            if self.change_request:
                prompt = f"""I need you to make changes to an existing demo website.

Project location: {DEMOS_DIR / self.project_name}

Change request:
{self.change_request}

Please make the requested changes to the project files and restart the dev server when done.
"""
            else:
                prompt = f"""Create a new demo website following the workflow below.

Original website URL: {self.url}

WORKFLOW:
{workflow}

Instructions:
1. Change directory to: {DEMOS_DIR}
2. Fetch the original website content from {self.url}
3. Create a new Astro project (use domain name as project name, e.g., "example-com")
4. Copy components from the template directory
5. Customize everything according to the workflow
6. Start the dev server with: cd [project-name] && npm run dev
7. Tell me when it's ready for review

IMPORTANT:
- Follow the workflow exactly
- Don't forget AI Chatbot personalization with primaryColor
- Use images from the original site
- Update all contact info and opening hours
- The dev server should run on port 4321

Start working now!
"""

            self.log("Starting Claude Code...")
            self.log(f"Working directory: {DEMOS_DIR}")
            self.log("")

            # Save prompt to temporary file
            prompt_file = DEMOS_DIR / ".demo_builder_prompt.txt"
            with open(prompt_file, 'w') as f:
                f.write(prompt)

            self.log("Executing Claude with prompt...")
            self.log("=" * 60)

            # Run claude with prompt from file
            # This is more reliable than stdin
            self.process = subprocess.Popen(
                ["claude", "--", f"$(cat {prompt_file})"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                shell=True,
                cwd=str(DEMOS_DIR)
            )

            # Read output in real-time
            while True:
                line = self.process.stdout.readline()
                if not line and self.process.poll() is not None:
                    break

                if line:
                    line = line.rstrip()
                    self.log(line)

                    # Check if dev server started
                    if "localhost:4321" in line.lower() or "local:" in line.lower():
                        self.log("")
                        self.log("✅ Dev server detected!")

                        # Wait a bit for server to fully start
                        time.sleep(3)

                        # Find the project name
                        demos = [d for d in os.listdir(DEMOS_DIR)
                                if os.path.isdir(DEMOS_DIR / d) and d not in ["template"]]
                        if demos:
                            latest_project = sorted(demos,
                                key=lambda x: os.path.getmtime(DEMOS_DIR / x))[-1]
                            self.finished_signal.emit(latest_project, "http://localhost:4321")
                        return

            # If we get here, process ended
            self.log("")
            self.log("Claude finished. Checking for dev server...")

            # Check if dev server is running
            check = subprocess.run(
                ["lsof", "-ti:4321"],
                capture_output=True,
                text=True
            )

            if check.returncode == 0:
                # Dev server is running
                demos = [d for d in os.listdir(DEMOS_DIR)
                        if os.path.isdir(DEMOS_DIR / d) and d not in ["template"]]
                if demos:
                    latest_project = sorted(demos,
                        key=lambda x: os.path.getmtime(DEMOS_DIR / x))[-1]
                    self.finished_signal.emit(latest_project, "http://localhost:4321")
                else:
                    self.error_signal.emit("No project found in demos/")
            else:
                self.error_signal.emit("Dev server not started. Check the logs above.")

        except Exception as e:
            self.error_signal.emit(f"Error: {str(e)}")

    def stop(self):
        """Stop the Claude process"""
        if self.process:
            self.process.terminate()
            self.process = None


class DemoBuilderApp(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.worker: Optional[ClaudeWorker] = None
        self.current_project: Optional[str] = None
        self.dev_url: Optional[str] = None
        self.original_url: Optional[str] = None

        self.init_ui()

    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("Demo Website Builder (Claude CLI)")
        self.setGeometry(100, 100, 1600, 1000)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Info banner
        info_label = QLabel("💰 Using Claude Code CLI - No API costs!")
        info_label.setStyleSheet("background-color: #d4edda; color: #155724; padding: 10px; border-radius: 5px; font-weight: bold;")
        layout.addWidget(info_label)

        # Input section
        input_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter website URL (e.g., https://www.example.com)")
        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_build)

        input_layout.addWidget(QLabel("Website URL:"))
        input_layout.addWidget(self.url_input)
        input_layout.addWidget(self.start_button)

        layout.addLayout(input_layout)

        # Log section
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        layout.addWidget(QLabel("Build Log:"))
        layout.addWidget(self.log_text)

        # Preview section (hidden initially)
        self.preview_splitter = QSplitter(Qt.Orientation.Horizontal)

        # Original site preview
        original_container = QWidget()
        original_layout = QVBoxLayout(original_container)
        original_layout.addWidget(QLabel("Original Website"))
        self.original_preview = QWebEngineView()
        original_layout.addWidget(self.original_preview)

        # New site preview
        new_container = QWidget()
        new_layout = QVBoxLayout(new_container)
        new_layout.addWidget(QLabel("Demo Website"))
        self.new_preview = QWebEngineView()
        new_layout.addWidget(self.new_preview)

        self.preview_splitter.addWidget(original_container)
        self.preview_splitter.addWidget(new_container)
        self.preview_splitter.setVisible(False)

        layout.addWidget(self.preview_splitter)

        # Review section (hidden initially)
        review_layout = QHBoxLayout()
        self.approve_button = QPushButton("Approve & Deploy")
        self.approve_button.clicked.connect(self.approve_and_deploy)
        self.changes_input = QLineEdit()
        self.changes_input.setPlaceholderText("Enter change requests...")
        self.request_changes_button = QPushButton("Request Changes")
        self.request_changes_button.clicked.connect(self.request_changes)

        review_layout.addWidget(self.approve_button)
        review_layout.addWidget(self.changes_input)
        review_layout.addWidget(self.request_changes_button)

        self.review_widget = QWidget()
        self.review_widget.setLayout(review_layout)
        self.review_widget.setVisible(False)

        layout.addWidget(self.review_widget)

    def log(self, message: str):
        """Add message to log"""
        self.log_text.append(message)

    def start_build(self):
        """Start building demo website"""
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a website URL")
            return

        # Check if claude CLI is available
        result = subprocess.run(["which", "claude"], capture_output=True)
        if result.returncode != 0:
            QMessageBox.critical(
                self,
                "Claude CLI Not Found",
                "Please install Claude Code:\n"
                "https://docs.anthropic.com/claude/docs/claude-code\n\n"
                "Or install via: npm install -g @anthropic-ai/claude-code"
            )
            return

        self.original_url = url
        self.log(f"Starting build for: {url}")
        self.log(f"Using Claude Code CLI (free!)")
        self.start_button.setEnabled(False)
        self.preview_splitter.setVisible(False)
        self.review_widget.setVisible(False)

        # Start worker
        self.worker = ClaudeWorker(url)
        self.worker.log_signal.connect(self.log)
        self.worker.finished_signal.connect(self.build_finished)
        self.worker.error_signal.connect(self.build_error)
        self.worker.start()

    def build_finished(self, project_name: str, dev_url: str):
        """Called when build is complete"""
        self.current_project = project_name
        self.dev_url = dev_url

        self.log(f"✅ Build complete! Project: {project_name}")
        self.log(f"🚀 Dev server: {dev_url}")

        # Show previews
        self.original_preview.setUrl(QUrl(self.original_url))
        self.new_preview.setUrl(QUrl(dev_url))
        self.preview_splitter.setVisible(True)
        self.review_widget.setVisible(True)

        self.start_button.setEnabled(True)

    def build_error(self, error: str):
        """Called when build fails"""
        self.log(f"❌ ERROR: {error}")
        QMessageBox.critical(self, "Build Error", error)
        self.start_button.setEnabled(True)

    def request_changes(self):
        """Request changes to the demo"""
        changes = self.changes_input.text().strip()
        if not changes:
            QMessageBox.warning(self, "Error", "Please enter change requests")
            return

        self.log(f"📝 Requesting changes: {changes}")
        self.review_widget.setVisible(False)
        self.changes_input.clear()

        # Start worker with changes
        self.worker = ClaudeWorker(
            self.original_url,
            change_request=changes,
            project_name=self.current_project
        )
        self.worker.log_signal.connect(self.log)
        self.worker.finished_signal.connect(self.build_finished)
        self.worker.error_signal.connect(self.build_error)
        self.worker.start()

    def approve_and_deploy(self):
        """Approve and deploy to Vercel"""
        if not self.current_project:
            return

        reply = QMessageBox.question(
            self,
            "Deploy",
            f"Deploy {self.current_project} to Vercel?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.log("🚀 Deploying to Vercel...")

            try:
                project_path = DEMOS_DIR / self.current_project

                # Build
                self.log("📦 Building project...")
                subprocess.run(["npm", "run", "build"], cwd=project_path, check=True)

                # Deploy
                self.log("☁️  Deploying to Vercel...")
                result = subprocess.run(
                    ["npx", "vercel", "--prod", "--yes"],
                    cwd=project_path,
                    capture_output=True,
                    text=True
                )

                self.log(result.stdout)

                # Extract URL
                for line in result.stdout.split('\n'):
                    if 'https://' in line and 'vercel.app' in line:
                        self.log(f"✅ Deployed to: {line.strip()}")

                QMessageBox.information(self, "Success", "Deployment complete!")

            except Exception as e:
                self.log(f"❌ Deployment error: {str(e)}")
                QMessageBox.critical(self, "Deploy Error", str(e))

    def closeEvent(self, event):
        """Clean up on close"""
        if self.worker:
            self.worker.stop()
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = DemoBuilderApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
