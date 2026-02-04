import sys
import os
from dotenv import load_dotenv
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage
from PyQt6.QtCore import QUrl, QTimer, Qt

USER_DATA_DIR = os.path.join(os.path.expanduser("~"), "Documents", "MessengerWrapperData")

if not os.path.exists(USER_DATA_DIR):
    os.makedirs(USER_DATA_DIR)

ENV_PATH = os.path.join(USER_DATA_DIR, ".env")

load_dotenv(ENV_PATH)
LOGIN_EMAIL = os.getenv("FB_EMAIL")
LOGIN_PASS = os.getenv("FB_PASSWORD")

if not os.path.exists(ENV_PATH):
    with open(ENV_PATH, "w") as f:
        f.write("FB_EMAIL=\nFB_PASSWORD=")

class MessengerWrapper(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Messenger Wrapper")
        self.setGeometry(100, 100, 1200, 800)

        profile_path = os.path.join(USER_DATA_DIR, "messenger_profile")
        self.profile = QWebEngineProfile("MessengerProfile", self)
        self.profile.setPersistentStoragePath(profile_path)
        self.profile.setPersistentCookiesPolicy(QWebEngineProfile.PersistentCookiesPolicy.ForcePersistentCookies)
        
        self.profile.setHttpUserAgent(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

        self.browser = QWebEngineView()
        page = QWebEnginePage(self.profile, self.browser)
        self.browser.setPage(page)
        
        self.setCentralWidget(self.browser)

        self.overlay = QWidget(self)
        self.overlay.setStyleSheet("background-color: #1a1a1a;")
        self.overlay_layout = QVBoxLayout(self.overlay)
        self.overlay_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.status_label = QLabel("Initializing application...", self.overlay)
        self.status_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.sub_status_label = QLabel("Please wait...", self.overlay)
        self.sub_status_label.setStyleSheet("color: #aaaaaa; font-size: 14px;")
        self.sub_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.retry_btn = QPushButton("Show Login Screen (Manual Mode)", self.overlay)
        self.retry_btn.setStyleSheet("""
            QPushButton { background-color: #0084ff; color: white; padding: 10px 20px; border-radius: 5px; font-weight: bold; }
            QPushButton:hover { background-color: #006bcf; }
        """)
        self.retry_btn.hide()
        self.retry_btn.clicked.connect(self.hide_overlay)

        self.overlay_layout.addWidget(self.status_label)
        self.overlay_layout.addWidget(self.sub_status_label)
        self.overlay_layout.addWidget(self.retry_btn)

        self.browser.loadFinished.connect(self.on_load_finished)
        self.browser.setUrl(QUrl("https://www.messenger.com/"))

    def resizeEvent(self, event):
        self.overlay.resize(self.size())
        super().resizeEvent(event)

    def hide_overlay(self):
        self.overlay.hide()

    def update_status(self, main_text, sub_text=""):
        self.status_label.setText(main_text)
        self.sub_status_label.setText(sub_text)

    def on_load_finished(self, success):
        if not success: 
            self.update_status("Connection Error", "Check your internet.")
            self.retry_btn.show()
            return

        current_url = self.browser.url().toString()
        
        if "login" in current_url or "messenger.com" in current_url or "facebook.com" in current_url:
            if "/t/" in current_url:
                self.hide_overlay()
            else:
                self.update_status("Login panel detected", "Waiting 5 seconds (Anti-Bot Protection)...")
                QTimer.singleShot(5000, self.inject_credentials)
        else:
            self.hide_overlay()

    def inject_credentials(self):
        if not LOGIN_EMAIL or not LOGIN_PASS:
            self.update_status("Missing credentials", "Enter data in .env file or terminal.")
            self.retry_btn.show()
            return

        self.update_status("Entering credentials...", "Please do not move your mouse.")
        
        js_code = f"""
        (function() {{
            function clickCookieButton() {{
                var cookieTexts = ["Zezwól na wszystkie pliki cookie", "Allow all cookies", "Zaakceptuj wszystkie", "Akceptuj wszystkie", "Zezwól"];
                var elements = document.querySelectorAll('button, div, span, [role="button"]');
                for (var i = 0; i < elements.length; i++) {{
                    var element = elements[i];
                    if (cookieTexts.some(text => element.innerText.includes(text)) && element.offsetParent !== null) {{
                        element.click();
                        console.log("Python JS: Clicked cookie button: " + element.innerText);
                        return true;
                    }}
                }}
                return false;
            }}

            function clickKeepSignedIn() {{
                var labels = document.getElementsByTagName('label');
                for (var i = 0; i < labels.length; i++) {{
                    if (labels[i].innerText.includes("Nie wylogowuj mnie") || labels[i].innerText.includes("Keep me signed in")) {{
                        labels[i].click();
                        console.log("Python JS: Clicked Keep me signed in");
                        return true;
                    }}
                }}
                return false;
            }}

            function fillCredentials(email, password) {{
                var emailField = document.querySelector('input[name="email"]') || document.querySelector('input[id="email"]');
                var passField = document.querySelector('input[name="pass"]') || document.querySelector('input[id="pass"]');

                if (emailField && passField) {{
                    emailField.value = email;
                    emailField.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    
                    passField.value = password;
                    passField.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    
                    var loginBtn = document.querySelector('button[name="login"]') || document.querySelector('button[id="loginbutton"]');
                    if (loginBtn) {{
                         setTimeout(function() {{ loginBtn.click(); }}, 1000);
                    }}
                    return true;
                }}
                return false;
            }}

            clickCookieButton();

            setTimeout(function() {{
                clickKeepSignedIn();
                fillCredentials("{LOGIN_EMAIL}", "{LOGIN_PASS}");
            }}, 2000);
        }})();
        """
        self.browser.page().runJavaScript(js_code)
        
        QTimer.singleShot(8000, self.check_login_success)

    def check_login_success(self):
        current_url = self.browser.url().toString()
        
        if "login" in current_url or current_url == "https://www.messenger.com/" or current_url == "https://www.facebook.com/":
            self.update_status("Automatic login failed.", "Possible wrong password or 2FA verification.")
            self.retry_btn.setText("Switch to manual login")
            self.retry_btn.show()
        else:
            self.hide_overlay()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MessengerWrapper()
    window.show()
    sys.exit(app.exec())