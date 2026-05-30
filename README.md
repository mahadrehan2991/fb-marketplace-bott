# 🤖 Facebook Marketplace Auto-Poster Bot

This bot is designed to automatically post your listings to Facebook Marketplace. It features a modern **CustomTkinter GUI** and robust **Playwright Automation**.

---

## ✨ Features

- **🛡️ Safe Session Login**: No need to enter your email/password every time. The bot saves your browser profile locally.
- **📂 Bulk Listing**: Upload unlimited items from an Excel or CSV file.
- **🖼️ Multiple Images**: Supports uploading multiple photos for each listing.
- **⏱️ Anti-Ban Delay**: Custom delay between posts to keep your account safe.
- **🎨 Modern Dark Mode UI**: Simple and gorgeous user interface.

---

## 🛠️ Requirements & Setup

1. **Install Python**:
   - If Python is not installed on your PC, download it from [Python.org](https://www.python.org/downloads/).
   - **IMPORTANT**: Make sure to check the **"Add Python to PATH"** box during installation.

2. **Setup the Bot**:
   - Open your project folder.
   - Simply double-click the file: **`run_bot.bat`**
   - This script will automatically install all required libraries (`customtkinter`, `playwright`, `pandas`) and set up the browser environment. Then, the Bot GUI will launch.

---

## 🚀 How to Use the Bot

### Step 1: Facebook Login (First Time Only)
1. Once the Bot GUI opens, click the blue button: **"1. Login to FB First"**.
2. A new browser window will open. Log in to your Facebook account (complete 2FA if prompted).
3. Once logged in and your home feed loads, **close the browser window**.
4. Your login session is now saved in the `fb_profile` folder. You won't need to log in manually again!

### Step 2: Prepare your Listing Data
1. Open the **`listings_template.csv`** file in Excel or a text editor.
2. Populate your product details:
   - **title**: Product name (e.g., `iPhone 13 Pro Max - 128GB`)
   - **price**: Price value (e.g., `150000`)
   - **category**: Sahi (exact) category name as it appears on Facebook Marketplace (e.g., `Mobile Phones`, `Men's Clothing`, `Furniture`).
   - **condition**: Choose one of: `New`, `Like New`, `Very Good`, `Good`, or `Fair`.
   - **description**: Product description details.
   - **location**: City/Town name (e.g., `Lahore, Pakistan`).
   - **images**: Product image filenames separated by commas (e.g., `iphone1.jpg, iphone2.jpg`).
3. Save all your product photos in a single folder.

### Step 3: Start Auto-Posting
1. **Listings CSV/Excel**: Click "Browse" and select your CSV or Excel file.
2. **Images Directory**: Click "Browse" and select the folder containing your product photos.
3. **Delay (seconds)**: Default is `60` seconds (to prevent account flags). You can adjust this (recommended: 60-120 seconds).
4. **Start Posting**: Click the green button: **"2. Start Posting"**.
5. The bot will automatically open the browser and start posting your products one by one. Live progress will be displayed in the **Console Log** at the bottom.

---

## ⚠️ Important Precautions

- **Browser Profile**: Do not delete the `fb_profile` folder. If deleted, you will have to complete Step 1 (login) again.
- **Account Safety**: Avoid posting more than 10-15 listings per day. Facebook limits posting activity if done excessively.
- **Delay**: Always keep the delay above 60 seconds so the Facebook algorithm does not flag your automation.
