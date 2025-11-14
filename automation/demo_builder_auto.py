#!/usr/bin/env python3
"""
Demo Website Builder - Auto Version
Automatically opens Terminal, runs claude, sends prompt, monitors for completion
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
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QUrl

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
        self.log_signal.emit(f"📂 Existing projects (ignored): {', '.join(self.initial_projects) or 'none'}")
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
        self.setWindowTitle("Demo Website Builder - Fully Automated (FREE!)")
        self.setGeometry(100, 100, 1600, 1000)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Info banner
        info_label = QLabel(
            "🤖 FULLY AUTOMATED - Just enter URL and click Start! (FREE - No API costs)"
        )
        info_label.setStyleSheet(
            "background-color: #d4edda; color: #155724; padding: 12px; "
            "border-radius: 5px; font-weight: bold; font-size: 14px;"
        )
        layout.addWidget(info_label)

        # Input section
        input_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter website URL (e.g., https://www.example.com)")
        self.start_button = QPushButton("🚀 Start Building")
        self.start_button.clicked.connect(self.start_build)
        self.start_button.setStyleSheet(
            "QPushButton { background-color: #28a745; color: white; padding: 12px; "
            "font-weight: bold; font-size: 16px; }"
            "QPushButton:hover { background-color: #218838; }"
        )

        input_layout.addWidget(QLabel("Website URL:"))
        input_layout.addWidget(self.url_input)
        input_layout.addWidget(self.start_button)

        layout.addLayout(input_layout)

        # Instructions
        instructions = QLabel(
            "ℹ️ How it works:\n"
            "1. Enter the website URL above\n"
            "2. Click 'Start Building'\n"
            "3. A Terminal window will open automatically with Claude Code\n"
            "4. Wait for the build to complete (you'll see progress in Terminal)\n"
            "5. Preview will appear automatically when ready!"
        )
        instructions.setStyleSheet(
            "background-color: #e7f3ff; padding: 10px; border-radius: 5px; "
            "border-left: 4px solid #2196F3; color: #333; font-size: 12px;"
        )
        layout.addWidget(instructions)

        # Log section
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(200)
        layout.addWidget(QLabel("Build Status:"))
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
        self.approve_button = QPushButton("✅ Approve & Deploy to Vercel")
        self.approve_button.clicked.connect(self.approve_and_deploy)
        self.approve_button.setStyleSheet(
            "QPushButton { background-color: #007bff; color: white; padding: 10px; "
            "font-weight: bold; font-size: 14px; }"
        )

        review_layout.addWidget(self.approve_button)

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

        self.original_url = url
        self.start_button.setEnabled(False)
        self.preview_splitter.setVisible(False)
        self.review_widget.setVisible(False)

        self.log("🚀 Starting automated build...")
        self.log(f"📍 URL: {url}")
        self.log("")

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
3. Create a new Astro project (use domain name as project name)
4. Copy components from the template directory
5. Customize everything according to the workflow
6. Start the dev server with: cd [project-name] && npm run dev
7. Tell me when it's ready for review

IMPORTANT:
- Follow the workflow exactly
- AI Chatbot personalization with primaryColor
- Use images from the original site
- Update all contact info and opening hours
- Dev server should run on port 4321

Start working now!
"""

        # Save prompt to temp file
        prompt_file = "/tmp/claude_demo_prompt.txt"
        with open(prompt_file, 'w') as f:
            f.write(prompt)

        self.log("💾 Prompt generated and saved")
        self.log("🖥️  Opening Terminal with Claude Code...")
        self.log("")

        # Create AppleScript to open Terminal, run claude, and send prompt
        applescript = f'''
tell application "Terminal"
    activate

    -- Create new tab or window
    if (count of windows) is 0 then
        do script ""
    else
        tell application "System Events" to keystroke "t" using command down
        delay 0.5
    end if

    -- Get the new tab
    set currentTab to selected tab of front window

    -- Change to demos directory
    do script "cd {DEMOS_DIR}" in currentTab
    delay 0.5

    -- Run claude
    do script "claude" in currentTab
    delay 2

    -- Send the prompt
    do script "$(cat {prompt_file})" in currentTab

end tell
'''

        # Execute AppleScript
        try:
            result = subprocess.run(
                ["osascript", "-e", applescript],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode != 0:
                # Permission error or other issue
                error_msg = result.stderr.lower()

                if "not allowed" in error_msg or "permission" in error_msg:
                    self.log("❌ Permission denied!")
                    self.log("")
                    self.log("🔐 You need to grant permissions:")
                    self.log("1. Open System Settings")
                    self.log("2. Go to Privacy & Security")
                    self.log("3. Click 'Automation'")
                    self.log("4. Enable Python/Terminal to control Terminal")
                    self.log("")

                    QMessageBox.critical(
                        self,
                        "Permission Required",
                        "AppleScript needs permission to control Terminal.\n\n"
                        "Please:\n"
                        "1. Open System Settings\n"
                        "2. Privacy & Security → Automation\n"
                        "3. Find 'Python' or this app\n"
                        "4. Enable 'Terminal' checkbox\n"
                        "5. Try again\n\n"
                        "OR: Just manually paste this prompt to Claude:\n"
                        f"cat {prompt_file}"
                    )
                else:
                    self.log(f"❌ AppleScript error: {result.stderr}")
                    QMessageBox.warning(
                        self,
                        "Automation Failed",
                        f"Couldn't automate Terminal.\n\n"
                        f"Error: {result.stderr[:200]}\n\n"
                        f"Manual workaround:\n"
                        f"1. Open Terminal\n"
                        f"2. cd {DEMOS_DIR}\n"
                        f"3. claude\n"
                        f"4. cat {prompt_file}"
                    )

                self.start_button.setEnabled(True)
                return

            self.log("✅ Terminal opened successfully!")
            self.log("✅ Claude Code started automatically!")
            self.log("✅ Prompt sent to Claude!")
            self.log("")
            self.log("📺 Watch the Terminal window to see Claude working...")
            self.log("⏳ Monitoring for project completion...")
            self.log("")

            # Start monitoring
            self.monitor = ProjectMonitor()
            self.monitor.log_signal.connect(self.log)
            self.monitor.project_found.connect(self.project_completed)
            self.monitor.start()

        except subprocess.TimeoutExpired:
            self.log("⚠️  AppleScript timed out (might still work)")
            self.log("Check if Terminal opened...")

            # Start monitoring anyway
            self.monitor = ProjectMonitor()
            self.monitor.log_signal.connect(self.log)
            self.monitor.project_found.connect(self.project_completed)
            self.monitor.start()

        except Exception as e:
            self.log(f"❌ Unexpected error: {e}")
            QMessageBox.critical(
                self,
                "Error",
                f"Failed to automate Terminal.\n\n"
                f"Error: {str(e)}\n\n"
                f"Manual workaround:\n"
                f"1. Open Terminal\n"
                f"2. cd {DEMOS_DIR}\n"
                f"3. claude\n"
                f"4. cat {prompt_file}"
            )
            self.start_button.setEnabled(True)

    def project_completed(self, project_name: str, dev_url: str):
        """Called when project is detected"""
        self.current_project = project_name
        self.dev_url = dev_url

        self.log("")
        self.log("=" * 60)
        self.log(f"🎉 BUILD COMPLETE!")
        self.log(f"📦 Project: {project_name}")
        self.log(f"🚀 Dev server: {dev_url}")
        self.log("=" * 60)
        self.log("")

        # Show previews
        self.original_preview.setUrl(QUrl(self.original_url))
        self.new_preview.setUrl(QUrl(dev_url))
        self.preview_splitter.setVisible(True)
        self.review_widget.setVisible(True)
        self.start_button.setEnabled(True)

        QMessageBox.information(
            self,
            "Build Complete! 🎉",
            f"Demo website is ready!\n\n"
            f"Project: {project_name}\n"
            f"URL: {dev_url}\n\n"
            f"Review it and click 'Approve & Deploy' when satisfied!"
        )

    def approve_and_deploy(self):
        """Approve and deploy to Vercel"""
        if not self.current_project:
            return

        reply = QMessageBox.question(
            self,
            "Deploy to Vercel?",
            f"Deploy {self.current_project} to production?\n\n"
            f"This will:\n"
            f"1. Build the project\n"
            f"2. Deploy to Vercel\n"
            f"3. Create a production URL",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.log("")
            self.log("🚀 Deploying to Vercel...")
            self.log("")

            try:
                project_path = DEMOS_DIR / self.current_project

                # Build
                self.log("📦 Building project...")
                result = subprocess.run(
                    ["npm", "run", "build"],
                    cwd=project_path,
                    capture_output=True,
                    text=True
                )

                if result.returncode != 0:
                    raise Exception(f"Build failed: {result.stderr}")

                self.log("✅ Build successful!")
                self.log("")

                # Deploy
                self.log("☁️  Deploying to Vercel...")
                result = subprocess.run(
                    ["npx", "vercel", "--prod", "--yes"],
                    cwd=project_path,
                    capture_output=True,
                    text=True
                )

                # Extract and show URLs
                for line in result.stdout.split('\n'):
                    if 'https://' in line and 'vercel.app' in line:
                        self.log(f"✅ Deployed: {line.strip()}")

                self.log("")
                self.log("🎉 Deployment complete!")

                QMessageBox.information(
                    self,
                    "Success!",
                    "Deployment complete!\n\nCheck the build log for the URL."
                )

            except Exception as e:
                self.log(f"❌ Error: {str(e)}")
                QMessageBox.critical(self, "Deployment Error", str(e))

    def closeEvent(self, event):
        """Clean up on close"""
        if self.monitor:
            self.monitor.stop()

        # Clean up temp file
        try:
            os.remove("/tmp/claude_demo_prompt.txt")
        except:
            pass

        event.accept()


def main():
    app = QApplication(sys.argv)
    window = DemoBuilderApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
