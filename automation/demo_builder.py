#!/usr/bin/env python3
"""
Demo Website Builder - Local Desktop App
Automates the creation of demo websites using Claude API
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
from typing import Optional, Dict, List, Any
import anthropic
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTextEdit, QLabel, QSplitter, QMessageBox,
    QComboBox, QDialog, QFormLayout, QDialogButtonBox, QGroupBox
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QUrl, QTimer
from dotenv import load_dotenv

load_dotenv()

# Configuration
DEMOS_DIR = Path(__file__).parent.parent / "demos"
TEMPLATE_DIR = DEMOS_DIR / "template"
WORKFLOW_PATH = TEMPLATE_DIR / "WORKFLOW.md"
CONFIG_PATH = Path(__file__).parent / "config.json"


class APIKeyManager:
    """Manage multiple API keys"""

    def __init__(self):
        self.config_path = CONFIG_PATH
        self.load_config()

    def load_config(self):
        """Load API keys from config file"""
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        else:
            # Create default config
            default_key = os.getenv("ANTHROPIC_API_KEY", "")
            self.config = {
                "api_keys": [
                    {"name": "Default", "key": default_key, "active": True}
                ] if default_key else [],
                "active_key_index": 0
            }
            self.save_config()

    def save_config(self):
        """Save API keys to config file"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)

    def get_keys(self) -> List[Dict[str, str]]:
        """Get all API keys"""
        return self.config.get("api_keys", [])

    def get_active_key(self) -> Optional[str]:
        """Get currently active API key"""
        keys = self.get_keys()
        active_index = self.config.get("active_key_index", 0)
        if keys and 0 <= active_index < len(keys):
            return keys[active_index]["key"]
        return None

    def get_active_key_name(self) -> Optional[str]:
        """Get name of active API key"""
        keys = self.get_keys()
        active_index = self.config.get("active_key_index", 0)
        if keys and 0 <= active_index < len(keys):
            return keys[active_index]["name"]
        return None

    def set_active_key(self, index: int):
        """Set active API key by index"""
        if 0 <= index < len(self.get_keys()):
            self.config["active_key_index"] = index
            self.save_config()

    def add_key(self, name: str, key: str):
        """Add new API key"""
        keys = self.get_keys()
        keys.append({"name": name, "key": key})
        self.config["api_keys"] = keys
        self.save_config()

    def remove_key(self, index: int):
        """Remove API key"""
        keys = self.get_keys()
        if 0 <= index < len(keys):
            keys.pop(index)
            self.config["api_keys"] = keys
            # Adjust active index if needed
            if self.config["active_key_index"] >= len(keys):
                self.config["active_key_index"] = max(0, len(keys) - 1)
            self.save_config()


class APIKeyDialog(QDialog):
    """Dialog for managing API keys"""

    def __init__(self, key_manager: APIKeyManager, parent=None):
        super().__init__(parent)
        self.key_manager = key_manager
        self.setWindowTitle("Manage API Keys")
        self.setMinimumWidth(500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Current keys list
        group = QGroupBox("API Keys")
        group_layout = QVBoxLayout(group)

        keys = self.key_manager.get_keys()
        for i, key_info in enumerate(keys):
            key_layout = QHBoxLayout()
            label = QLabel(f"{key_info['name']}: {key_info['key'][:15]}...{key_info['key'][-4:]}")
            remove_btn = QPushButton("Remove")
            remove_btn.clicked.connect(lambda checked, idx=i: self.remove_key(idx))
            key_layout.addWidget(label)
            key_layout.addWidget(remove_btn)
            group_layout.addLayout(key_layout)

        layout.addWidget(group)

        # Add new key form
        form_group = QGroupBox("Add New Key")
        form_layout = QFormLayout(form_group)

        self.name_input = QLineEdit()
        self.key_input = QLineEdit()
        self.key_input.setEchoMode(QLineEdit.EchoMode.Password)

        form_layout.addRow("Name:", self.name_input)
        form_layout.addRow("API Key:", self.key_input)

        add_btn = QPushButton("Add Key")
        add_btn.clicked.connect(self.add_key)
        form_layout.addRow(add_btn)

        layout.addWidget(form_group)

        # Close button
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        button_box.rejected.connect(self.accept)
        layout.addWidget(button_box)

    def add_key(self):
        name = self.name_input.text().strip()
        key = self.key_input.text().strip()

        if not name or not key:
            QMessageBox.warning(self, "Error", "Please enter both name and API key")
            return

        self.key_manager.add_key(name, key)
        QMessageBox.information(self, "Success", f"Added API key: {name}")
        self.accept()

    def remove_key(self, index: int):
        reply = QMessageBox.question(
            self,
            "Confirm",
            "Remove this API key?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.key_manager.remove_key(index)
            QMessageBox.information(self, "Success", "API key removed")
            self.accept()


class ClaudeWorker(QThread):
    """Background thread for Claude API calls"""
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(str, str)  # project_name, dev_url
    error_signal = pyqtSignal(str)

    def __init__(self, api_key: str, url: str, change_request: Optional[str] = None, project_name: Optional[str] = None):
        super().__init__()
        self.api_key = api_key
        self.url = url
        self.change_request = change_request
        self.project_name = project_name
        self.client = anthropic.Anthropic(api_key=api_key)
        self.conversation_history = []
        self.dev_process = None

    def log(self, message: str):
        """Emit log message to UI"""
        self.log_signal.emit(message)
        print(f"[LOG] {message}")

    def read_file(self, path: str) -> str:
        """Tool: Read file contents"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def write_file(self, path: str, content: str) -> str:
        """Tool: Write file contents"""
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"Successfully wrote to {path}"
        except Exception as e:
            return f"Error writing file: {str(e)}"

    def edit_file(self, path: str, old_string: str, new_string: str) -> str:
        """Tool: Edit file with string replacement"""
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()

            if old_string not in content:
                return f"Error: old_string not found in {path}"

            new_content = content.replace(old_string, new_string)

            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)

            return f"Successfully edited {path}"
        except Exception as e:
            return f"Error editing file: {str(e)}"

    def run_command(self, command: str, cwd: Optional[str] = None) -> str:
        """Tool: Run shell command"""
        try:
            self.log(f"Running: {command}")
            result = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=120
            )
            output = result.stdout + result.stderr
            return output[:2000]  # Limit output
        except Exception as e:
            return f"Error running command: {str(e)}"

    def start_dev_server(self, project_path: str) -> str:
        """Start npm dev server in background"""
        try:
            self.log(f"Starting dev server in {project_path}")
            self.dev_process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=project_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            time.sleep(5)  # Wait for server to start
            return "Dev server started on http://localhost:4321"
        except Exception as e:
            return f"Error starting dev server: {str(e)}"

    def stop_dev_server(self):
        """Stop dev server"""
        if self.dev_process:
            self.dev_process.terminate()
            self.dev_process = None

    def execute_tool(self, tool_name: str, tool_input: Dict[str, Any]) -> str:
        """Execute a tool call from Claude"""
        self.log(f"Executing tool: {tool_name}")

        if tool_name == "read_file":
            return self.read_file(tool_input["path"])
        elif tool_name == "write_file":
            return self.write_file(tool_input["path"], tool_input["content"])
        elif tool_name == "edit_file":
            return self.edit_file(
                tool_input["path"],
                tool_input["old_string"],
                tool_input["new_string"]
            )
        elif tool_name == "run_command":
            return self.run_command(
                tool_input["command"],
                tool_input.get("cwd")
            )
        elif tool_name == "start_dev_server":
            return self.start_dev_server(tool_input["project_path"])
        else:
            return f"Unknown tool: {tool_name}"

    def run(self):
        """Main worker thread execution"""
        try:
            # Read workflow
            workflow = self.read_file(str(WORKFLOW_PATH))

            # Build initial prompt
            if self.change_request:
                prompt = f"The user requested changes to the existing demo website:\n\n{self.change_request}\n\nPlease make the requested changes to the project at {DEMOS_DIR / self.project_name}"
            else:
                prompt = f"""Create a new demo website following the workflow below.

Original website URL: {self.url}

WORKFLOW:
{workflow}

Instructions:
1. Fetch the original website content
2. Create a new Astro project in demos/ (use domain name as project name)
3. Copy components from template
4. Customize everything according to workflow
5. Start dev server when done
6. Report back when ready for review

Important: Follow the workflow exactly. Don't forget:
- AI Chatbot personalization with primaryColor
- Use images from original site
- Update all contact info, opening hours
- Match original site structure
"""

            self.log("Sending request to Claude...")

            # Define available tools
            tools = [
                {
                    "name": "read_file",
                    "description": "Read contents of a file",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "File path"}
                        },
                        "required": ["path"]
                    }
                },
                {
                    "name": "write_file",
                    "description": "Write content to a file",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "File path"},
                            "content": {"type": "string", "description": "File content"}
                        },
                        "required": ["path", "content"]
                    }
                },
                {
                    "name": "edit_file",
                    "description": "Edit file by replacing old_string with new_string",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "path": {"type": "string", "description": "File path"},
                            "old_string": {"type": "string", "description": "String to replace"},
                            "new_string": {"type": "string", "description": "Replacement string"}
                        },
                        "required": ["path", "old_string", "new_string"]
                    }
                },
                {
                    "name": "run_command",
                    "description": "Run a shell command",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "command": {"type": "string", "description": "Command to run"},
                            "cwd": {"type": "string", "description": "Working directory"}
                        },
                        "required": ["command"]
                    }
                },
                {
                    "name": "start_dev_server",
                    "description": "Start npm dev server for preview",
                    "input_schema": {
                        "type": "object",
                        "properties": {
                            "project_path": {"type": "string", "description": "Project directory"}
                        },
                        "required": ["project_path"]
                    }
                }
            ]

            # Start conversation loop
            messages = [{"role": "user", "content": prompt}]
            max_iterations = 50

            for iteration in range(max_iterations):
                self.log(f"Iteration {iteration + 1}/{max_iterations}")

                response = self.client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=8000,
                    tools=tools,
                    messages=messages
                )

                # Process response
                if response.stop_reason == "end_turn":
                    # Claude finished
                    final_text = ""
                    for block in response.content:
                        if hasattr(block, 'text'):
                            final_text += block.text
                            self.log(f"Claude: {block.text}")

                    # Extract project name and signal completion
                    # Assume project name is in demos/ directory
                    demos = [d for d in os.listdir(DEMOS_DIR) if os.path.isdir(DEMOS_DIR / d) and d not in ["template"]]
                    if demos:
                        latest_project = sorted(demos)[-1]  # Get newest
                        self.finished_signal.emit(latest_project, "http://localhost:4321")
                    else:
                        self.error_signal.emit("No project created")
                    break

                elif response.stop_reason == "tool_use":
                    # Execute tools
                    tool_results = []

                    for block in response.content:
                        if block.type == "tool_use":
                            result = self.execute_tool(block.name, block.input)
                            tool_results.append({
                                "type": "tool_result",
                                "tool_use_id": block.id,
                                "content": result
                            })

                    # Add assistant message and tool results to conversation
                    messages.append({"role": "assistant", "content": response.content})
                    messages.append({"role": "user", "content": tool_results})

                else:
                    self.error_signal.emit(f"Unexpected stop reason: {response.stop_reason}")
                    break

        except Exception as e:
            self.error_signal.emit(str(e))


class DemoBuilderApp(QMainWindow):
    """Main application window"""

    def __init__(self):
        super().__init__()
        self.key_manager = APIKeyManager()
        self.worker: Optional[ClaudeWorker] = None
        self.current_project: Optional[str] = None
        self.dev_url: Optional[str] = None
        self.original_url: Optional[str] = None

        self.init_ui()
        self.update_key_selector()
        self.fetch_usage()

        # Auto-refresh usage every 30 seconds
        self.usage_timer = QTimer()
        self.usage_timer.timeout.connect(self.fetch_usage)
        self.usage_timer.start(30000)

    def init_ui(self):
        """Initialize UI"""
        self.setWindowTitle("Demo Website Builder")
        self.setGeometry(100, 100, 1600, 1000)

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # API Key section
        api_layout = QHBoxLayout()
        api_layout.addWidget(QLabel("API Key:"))

        self.key_selector = QComboBox()
        self.key_selector.currentIndexChanged.connect(self.on_key_changed)
        api_layout.addWidget(self.key_selector)

        manage_keys_btn = QPushButton("Manage Keys")
        manage_keys_btn.clicked.connect(self.manage_keys)
        api_layout.addWidget(manage_keys_btn)

        api_layout.addStretch()

        # Usage display
        self.usage_label = QLabel("Usage: Loading...")
        self.usage_label.setStyleSheet("color: #666; font-size: 11px;")
        api_layout.addWidget(self.usage_label)

        layout.addLayout(api_layout)

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
        self.log_text.setMaximumHeight(150)
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

        api_key = self.key_manager.get_active_key()
        if not api_key:
            QMessageBox.critical(self, "Error", "Please configure an API key first")
            return

        self.original_url = url
        self.log(f"Starting build for: {url}")
        self.start_button.setEnabled(False)
        self.preview_splitter.setVisible(False)
        self.review_widget.setVisible(False)

        # Start worker
        self.worker = ClaudeWorker(api_key, url)
        self.worker.log_signal.connect(self.log)
        self.worker.finished_signal.connect(self.build_finished)
        self.worker.error_signal.connect(self.build_error)
        self.worker.start()

    def build_finished(self, project_name: str, dev_url: str):
        """Called when build is complete"""
        self.current_project = project_name
        self.dev_url = dev_url

        self.log(f"Build complete! Project: {project_name}")
        self.log(f"Dev server: {dev_url}")

        # Show previews
        self.original_preview.setUrl(QUrl(self.original_url))
        self.new_preview.setUrl(QUrl(dev_url))
        self.preview_splitter.setVisible(True)
        self.review_widget.setVisible(True)

        self.start_button.setEnabled(True)

    def build_error(self, error: str):
        """Called when build fails"""
        self.log(f"ERROR: {error}")
        QMessageBox.critical(self, "Build Error", error)
        self.start_button.setEnabled(True)

    def request_changes(self):
        """Request changes to the demo"""
        changes = self.changes_input.text().strip()
        if not changes:
            QMessageBox.warning(self, "Error", "Please enter change requests")
            return

        api_key = self.key_manager.get_active_key()
        if not api_key:
            QMessageBox.critical(self, "Error", "Please configure an API key first")
            return

        self.log(f"Requesting changes: {changes}")
        self.review_widget.setVisible(False)
        self.changes_input.clear()

        # Start worker with changes
        self.worker = ClaudeWorker(
            api_key,
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
            self.log("Deploying to Vercel...")

            try:
                project_path = DEMOS_DIR / self.current_project

                # Build
                self.log("Building project...")
                subprocess.run(["npm", "run", "build"], cwd=project_path, check=True)

                # Deploy
                self.log("Deploying to Vercel...")
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
                        self.log(f"Deployed to: {line.strip()}")

                QMessageBox.information(self, "Success", "Deployment complete!")

            except Exception as e:
                self.log(f"Deployment error: {str(e)}")
                QMessageBox.critical(self, "Deploy Error", str(e))

    def update_key_selector(self):
        """Update API key dropdown"""
        self.key_selector.clear()
        keys = self.key_manager.get_keys()

        if not keys:
            self.key_selector.addItem("No API keys configured")
            self.start_button.setEnabled(False)
            return

        for key_info in keys:
            self.key_selector.addItem(key_info["name"])

        # Set active key
        active_index = self.key_manager.config.get("active_key_index", 0)
        self.key_selector.setCurrentIndex(active_index)
        self.start_button.setEnabled(True)

    def on_key_changed(self, index: int):
        """Handle API key selection change"""
        if index >= 0:
            self.key_manager.set_active_key(index)
            self.fetch_usage()

    def manage_keys(self):
        """Open API key management dialog"""
        dialog = APIKeyDialog(self.key_manager, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.update_key_selector()
            self.fetch_usage()

    def fetch_usage(self):
        """Fetch and display API usage"""
        api_key = self.key_manager.get_active_key()
        key_name = self.key_manager.get_active_key_name()

        if not api_key:
            self.usage_label.setText("Usage: No API key selected")
            return

        try:
            # Note: Anthropic doesn't have a public usage API endpoint yet
            # This is a placeholder - you'd need to track usage manually or use billing API
            # For now, we'll just show the active key name
            self.usage_label.setText(f"Active Key: {key_name} | Usage tracking coming soon")

            # If/when Anthropic adds usage API:
            # client = anthropic.Anthropic(api_key=api_key)
            # usage = client.usage.get()  # hypothetical
            # self.usage_label.setText(f"Active Key: {key_name} | Tokens: {usage.tokens_used}/{usage.tokens_limit}")

        except Exception as e:
            self.usage_label.setText(f"Active Key: {key_name} | Usage: Error")
            print(f"Error fetching usage: {e}")

    def closeEvent(self, event):
        """Clean up on close"""
        if self.worker:
            self.worker.stop_dev_server()
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = DemoBuilderApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
