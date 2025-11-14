#!/usr/bin/env python3
"""
Demo Website Builder - Simple Version
Shows you the prompt, you paste it to Claude Code, app monitors for completion
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
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QUrl, QTimer
# No external clipboard library needed - Qt has it built-in!

# Configuration
DEMOS_DIR = Path(__file__).parent.parent / "demos"
TEMPLATE_DIR = DEMOS_DIR / "template"
WORKFLOW_PATH = TEMPLATE_DIR / "WORKFLOW.md"


class ProjectMonitor(QThread):
    """Monitor demos folder for new projects and dev servers"""
    project_found = pyqtSignal(str, str)  # project_name, dev_url
    log_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.running = True
        self.initial_projects = set()
        self.start_time = time.time()

    def run(self):
        # Get initial project list
        if DEMOS_DIR.exists():
            self.initial_projects = {d.name for d in DEMOS_DIR.iterdir()
                                    if d.is_dir() and d.name != "template"}

        self.log_signal.emit("👀 Monitoring demos folder for new projects...")
        self.log_signal.emit(f"📁 Watching: {DEMOS_DIR}")
        self.log_signal.emit(f"📂 Existing projects (will be ignored): {', '.join(self.initial_projects) or 'none'}")
        self.log_signal.emit("")
        self.log_signal.emit("💡 Paste the prompt to Claude now and start monitoring will begin...")
        self.log_signal.emit("")

        found_new_project = False
        new_project_name = None

        while self.running:
            time.sleep(2)  # Check every 2 seconds

            if not DEMOS_DIR.exists():
                continue

            # Check for new projects (created AFTER monitoring started)
            current_projects = {d.name for d in DEMOS_DIR.iterdir()
                              if d.is_dir() and d.name != "template"}
            new_projects = current_projects - self.initial_projects

            # Found a new project!
            if new_projects and not found_new_project:
                for project in new_projects:
                    project_path = DEMOS_DIR / project
                    # Check if it was created after we started monitoring
                    creation_time = project_path.stat().st_ctime
                    if creation_time > self.start_time:
                        self.log_signal.emit(f"📦 New project detected: {project}")
                        found_new_project = True
                        new_project_name = project
                        self.initial_projects.add(project)
                        break

            # Only check for dev server if we found a new project
            if found_new_project:
                result = subprocess.run(
                    ["lsof", "-ti:4321"],
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    # Dev server is running!
                    self.log_signal.emit(f"🚀 Dev server started for {new_project_name}!")
                    self.project_found.emit(new_project_name, "http://localhost:4321")
                    self.running = False
                    return
                else:
                    # Still waiting for dev server
                    if not hasattr(self, '_waiting_logged'):
                        self.log_signal.emit(f"⏳ Waiting for dev server to start...")
                        self._waiting_logged = True

    def stop(self):
        self.running = False


class DemoBuilderApp(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.monitor: Optional[ProjectMonitor] = None
        self.current_project: Optional[str] = None
        self.dev_url: Optional[str] = None
        self.original_url: Optional[str] = None

        self.init_ui()

    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("Demo Website Builder (Simple - No API Costs!)")
        self.setGeometry(100, 100, 1600, 1000)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Info banner
        info_label = QLabel(
            "💰 FREE VERSION - Copy prompt → Paste in Claude Code → Done!"
        )
        info_label.setStyleSheet(
            "background-color: #d4edda; color: #155724; padding: 10px; "
            "border-radius: 5px; font-weight: bold; font-size: 14px;"
        )
        layout.addWidget(info_label)

        # Input section
        input_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter website URL (e.g., https://www.example.com)")
        self.generate_button = QPushButton("Generate Prompt")
        self.generate_button.clicked.connect(self.generate_prompt)

        input_layout.addWidget(QLabel("Website URL:"))
        input_layout.addWidget(self.url_input)
        input_layout.addWidget(self.generate_button)

        layout.addLayout(input_layout)

        # Prompt display
        prompt_label = QLabel("📋 Prompt (Copy this and paste into Claude Code):")
        layout.addWidget(prompt_label)

        self.prompt_text = QTextEdit()
        self.prompt_text.setReadOnly(True)
        self.prompt_text.setMaximumHeight(300)
        layout.addWidget(self.prompt_text)

        # Action buttons
        action_layout = QHBoxLayout()
        self.copy_button = QPushButton("📋 Copy Prompt")
        self.copy_button.clicked.connect(self.copy_prompt)
        self.copy_button.setEnabled(False)
        self.copy_button.setStyleSheet(
            "QPushButton { background-color: #28a745; color: white; padding: 10px; "
            "font-weight: bold; font-size: 14px; }"
            "QPushButton:disabled { background-color: #ccc; }"
        )

        self.start_monitoring_button = QPushButton("👀 Start Monitoring")
        self.start_monitoring_button.clicked.connect(self.start_monitoring)
        self.start_monitoring_button.setEnabled(False)

        action_layout.addWidget(self.copy_button)
        action_layout.addWidget(self.start_monitoring_button)
        action_layout.addStretch()

        layout.addLayout(action_layout)

        # Log section
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        layout.addWidget(QLabel("Status Log:"))
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

        review_layout.addWidget(self.approve_button)

        self.review_widget = QWidget()
        self.review_widget.setLayout(review_layout)
        self.review_widget.setVisible(False)

        layout.addWidget(self.review_widget)

    def log(self, message: str):
        """Add message to log"""
        self.log_text.append(message)

    def generate_prompt(self):
        """Generate the prompt for Claude"""
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Error", "Please enter a website URL")
            return

        self.original_url = url

        # Read workflow
        with open(WORKFLOW_PATH, 'r') as f:
            workflow = f.read()

        # Generate prompt
        prompt = f"""Create a new demo website following the workflow below.

Original website URL: {url}

WORKFLOW:
{workflow}

Instructions:
1. Change directory to: {DEMOS_DIR}
2. Fetch the original website content from {url}
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

        self.prompt_text.setPlainText(prompt)
        self.copy_button.setEnabled(True)
        self.start_monitoring_button.setEnabled(True)

        self.log("✅ Prompt generated!")
        self.log("")
        self.log("📋 Next steps:")
        self.log("1. Click 'Copy Prompt' button")
        self.log("2. Open your terminal")
        self.log("3. Type: claude")
        self.log(f"4. Paste the prompt (Cmd+V)")
        self.log("5. Click 'Start Monitoring' in this app")
        self.log("6. Wait for Claude to finish!")

    def copy_prompt(self):
        """Copy prompt to clipboard"""
        prompt = self.prompt_text.toPlainText()
        clipboard = QApplication.clipboard()
        clipboard.setText(prompt)
        self.log("✅ Prompt copied to clipboard!")
        QMessageBox.information(
            self,
            "Copied!",
            "Prompt copied to clipboard!\n\n"
            "Now:\n"
            "1. Open terminal\n"
            "2. Run: claude\n"
            "3. Paste (Cmd+V)\n"
            "4. Click 'Start Monitoring'"
        )

    def start_monitoring(self):
        """Start monitoring for project completion"""
        self.log("")
        self.log("=" * 60)
        self.start_monitoring_button.setEnabled(False)

        self.monitor = ProjectMonitor()
        self.monitor.log_signal.connect(self.log)
        self.monitor.project_found.connect(self.project_completed)
        self.monitor.start()

    def project_completed(self, project_name: str, dev_url: str):
        """Called when project is detected"""
        self.current_project = project_name
        self.dev_url = dev_url

        self.log("")
        self.log("=" * 60)
        self.log(f"✅ Project complete: {project_name}")
        self.log(f"🚀 Dev server: {dev_url}")
        self.log("")

        # Show previews
        self.original_preview.setUrl(QUrl(self.original_url))
        self.new_preview.setUrl(QUrl(dev_url))
        self.preview_splitter.setVisible(True)
        self.review_widget.setVisible(True)

        QMessageBox.information(
            self,
            "Build Complete!",
            f"Demo website is ready!\n\n"
            f"Project: {project_name}\n"
            f"URL: {dev_url}\n\n"
            f"Review it and click 'Approve & Deploy' when ready!"
        )

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
                self.log("☁️  Deploying...")
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
                        self.log(f"✅ Deployed: {line.strip()}")

                QMessageBox.information(self, "Success", "Deployment complete!")

            except Exception as e:
                self.log(f"❌ Error: {str(e)}")
                QMessageBox.critical(self, "Error", str(e))

    def closeEvent(self, event):
        """Clean up on close"""
        if self.monitor:
            self.monitor.stop()
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = DemoBuilderApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
