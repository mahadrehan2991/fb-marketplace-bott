# 🤖 Facebook Marketplace Auto-Poster Bot

Yeh bot aapki listings ko Facebook Marketplace par automatically post karne ke liye banaya gaya hai. Isme modern **CustomTkinter GUI** aur **Playwright Automation** use ki gayi hai.

---

## ✨ Features

- **🛡️ Safe Session Login**: Har baar email/password dalne ki zaroorat nahi. Bot browser profile ko local save rakhta hai.
- **📂 Bulk Listing**: Excel ya CSV file se unlimited items upload karein.
- **🖼️ Multiple Images**: Har listing ke liye multiple photos support karta hai.
- **⏱️ Anti-Ban Delay**: Posts ke darmiyan custom delay taake account safe rahe.
- **🎨 Modern Dark Mode UI**: Simple aur gorgeous interface.

---

## 🛠️ Requirements & Setup

1. **Python Install Karein**:
   - Agar aapke PC me Python installed nahi hai, toh [Python.org](https://www.python.org/downloads/) se download karein.
   - **IMPORTANT**: Install karte waqt **"Add Python to PATH"** waale box ko check zaroor karein.

2. **Bot Setup Karein**:
   - Pure project folder ko check karein.
   - Simply double-click karein file par: **`run_bot.bat`**
   - Yeh file automatically saari libraries (`customtkinter`, `playwright`, `pandas`) install karegi aur browser support setup karegi. Phir Bot GUI open ho jayega.

---

## 🚀 Bot Ko Use Karne Ka Tareeqa

### Step 1: Facebook Login (Pehli Baar)
1. Bot GUI open hone ke baad, blue button click karein: **"1. Login to FB First"**.
2. Ek naya browser window khulega. Apne Facebook account me log in karein (2FA code agar zaroorat ho toh enter karein).
3. Jab aap login ho jayein aur home feed load ho jaye, toh **browser window ko close (band) kar dein**.
4. Aapka login session `fb_profile` folder me save ho chuka hai. Ab dobara login karne ki zaroorat nahi hogi!

### Step 2: Listing Data Tayyar Karein
1. **`listings_template.csv`** file ko Excel ya Notepad me open karein.
2. Usme apni products ki details dalein:
   - **title**: Product ka naam (e.g., `iPhone 13 Pro Max - 128GB`)
   - **price**: Qeemat (e.g., `150000`)
   - **category**: Category ka sahi naam jo FB par hoti hai (e.g., `Mobile Phones`, `Men's Clothing`, `Furniture`). Category spelling sahi honi chahiye!
   - **condition**: `New`, `Like New`, `Very Good`, `Good`, ya `Fair` me se koi ek likhein.
   - **description**: Product ki detail.
   - **location**: City/Town name (e.g., `Lahore, Pakistan`).
   - **images**: Images ke filenames comma (,) ke sath separate kar ke likhein (e.g., `iphone1.jpg, iphone2.jpg`).
3. Apni saari product photos ko ek specific folder me save kar lein.

### Step 3: Auto-Posting Shuru Karein
1. **Listings CSV/Excel**: "Browse" par click karein aur apni CSV file select karein.
2. **Images Directory**: "Browse" click kar ke woh folder select karein jisme aapne product photos rakhi hain.
3. **Delay (seconds)**: Default `60` seconds hai (taake account block na ho). Aap isko tabdeel kar sakte hain (recommended: 60-120 seconds).
4. **Start Posting**: Green button click karein **"2. Start Posting"**.
5. Bot automatic browser open karega aur ek-ek kar ke saare products post karna shuru kar dega. Live progress neeche **Console Log** me nazar aayegi.

---

## ⚠️ Important Precautions (Ahmiat)

- **Browser Profile**: `fb_profile` folder ko delete na karein. Agar delete karenge toh aapko dobara step 1 (login) karna parega.
- **Account Safety**: Aik din me 10-15 se zyada posts na karein. Facebook zyaada posting par account limit kar deta hai.
- **Delay**: Delay ko hamesha 60 seconds se zyada rakhein taake Facebook algorithm ko shak na ho.
