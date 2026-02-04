# 🔵 Messenger Wrapper (macOS)

This tool turns the **Messenger website** into a standalone, native-looking macOS application. It features **automatic login**, a loading screen to hide the browser process, and removes the need to keep a browser tab open.

---

## 🛠 Step 1: Requirements (What you need)

Before you start, your Mac must have **Python 3** installed.

1.  Open **Terminal** (Press `Command + Space`, type "Terminal", and hit Enter).
2.  Type this command and hit **Enter**:
    ```bash
    python3 --version
    ```
3.  **If you see a number** (e.g., `Python 3.12.0`) — Great! You are ready.
4.  **If you see an error** — Go to [python.org/downloads](https://www.python.org/downloads/) and install the latest version of Python.

---

## 📂 Step 2: Check your files

Make sure all these files are in **the same folder**:

1.  `messenger_wrapper.py` (The main application code)
2.  `start.command` (The script to build the app)
3.  `uninstall.command` (The script to remove the app)
4.  `requirements.txt` (List of required libraries)
    - _If you don't have this file, create a text file named `requirements.txt` and paste this inside:_
      ```text
      PyQt6
      PyQt6-WebEngine
      python-dotenv
      pyinstaller
      ```
5.  `app_icon.icns` (**Optional**: If you want a custom icon)

---

## 🔐 Step 3: Grant Permissions (Very Important!)

By default, macOS blocks script files. You need to unlock them once.

1.  Open **Terminal**.
2.  Type the following command **(but DO NOT press Enter yet)**:
    ```bash
    chmod +x
    ```
    _(⚠️ Note: There is a **space** after the `x`!)_
3.  Open your project folder in **Finder**.
4.  **Drag and drop** both `start.command` and `uninstall.command` from Finder directly into the Terminal window.

- _The terminal will automatically fill in the correct path to the files._

You can also fill that manually

```bash
chmod +x start.command
```

and

```bash
chmod +x uninstall.command
```

5.  Now, press **Enter**.

---

## 🚀 Step 4: Build the App

1.  Double-click on **`start.command`**.
2.  A terminal window will open.
3.  **First Run:** It will ask for your Facebook **Email** and **Password**.
    - _🔐 Note: When typing your password, **you won't see the characters**. This is a security feature. Just type it and press Enter._
4.  Wait a minute... The script will download necessary libraries and build the app.
5.  When finished, a folder named `dist` will open automatically. Inside, you will see **Messenger Wrapper.app**.

---

## 📱 Step 5: Using the App

1.  You can drag **Messenger Wrapper.app** to your **Applications** folder or keep it anywhere you like.
2.  Double-click the app to open it.
3.  **First Launch Behavior:**
    - You will see a black screen saying **"Initializing application..."**.
    - **⚠️ Do not touch your mouse.** The app is simulating a human user to click "Accept Cookies" and log you in automatically.
    - This process takes about **5-8 seconds**.
4.  Once logged in, the chat interface will appear, and the black screen will vanish.

---

## 🗑 Step 6: How to Uninstall

If you want to remove the app and delete your saved login data:

1.  Double-click on **`uninstall.command`**.
2.  It will delete the app and clear your saved credentials from your Documents folder (`~/Documents/MessengerWrapperData`).

---

### ❓ Troubleshooting

- **"App is damaged and can't be opened":**
  - Sometimes macOS security is too strict with custom apps.
  - **Fix:** Right-click the App -> Select **Open** -> Click **Open** in the popup window.
- **Login fails or gets stuck:**
  - If you have **2-Factor Authentication (2FA)** enabled (SMS code), the auto-login might time out.
  - **Fix:** Wait for the error message on the black screen, then click the button **"Show Login Screen"** to enter your code manually.
