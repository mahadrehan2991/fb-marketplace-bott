import os
import sys
import time
import threading
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from playwright.sync_api import sync_playwright

# Set theme and color options
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class FBMarketplaceBotApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("Facebook Marketplace Auto-Poster Bot")
        self.geometry("850x650")
        
        # Grid Configuration
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # State variables
        self.csv_path = tk.StringVar(value="")
        self.images_dir = tk.StringVar(value="")
        self.profile_dir = tk.StringVar(value=os.path.join(os.getcwd(), "fb_profile"))
        self.delete_keyword = tk.StringVar(value="")
        self.delay_between_posts = tk.IntVar(value=60)
        self.headless = tk.BooleanVar(value=False)
        self.is_running = False
        self.bot_thread = None
        
        # Sidebar Frame
        self.sidebar_frame = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="FB Market Bot", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        # Open Browser Session button
        self.btn_login = ctk.CTkButton(self.sidebar_frame, text="1. Login to FB First", command=self.open_login_browser, fg_color="#1877F2", hover_color="#166FE5")
        self.btn_login.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        # Start and Stop Buttons
        self.btn_start = ctk.CTkButton(self.sidebar_frame, text="2. Start Posting", command=self.start_posting, fg_color="#2eb85c", hover_color="#22994e")
        self.btn_start.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_stop = ctk.CTkButton(self.sidebar_frame, text="Stop Posting", command=self.stop_posting, fg_color="#e55353", hover_color="#d93737", state="disabled")
        self.btn_stop.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        # Theme switcher at bottom of sidebar
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Dark", "Light"], command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(0, 20))
        
        # Main Dashboard Frame
        self.main_frame = ctk.CTkFrame(self, corner_radius=15)
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(3, weight=1)
        
        # Configuration Settings Frame inside Main Frame
        self.config_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.config_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        self.config_frame.grid_columnconfigure(1, weight=1)
        
        # Select Automation Type
        self.lbl_auto_type = ctk.CTkLabel(self.config_frame, text="Select Automation Type:", anchor="w")
        self.lbl_auto_type.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")
        self.auto_type = tk.StringVar(value="Post Listings (Standard)")
        self.entry_auto_type = ctk.CTkOptionMenu(
            self.config_frame, 
            values=[
                "Post Listings (Standard)",
                "Post Listings (New Accounts - Slower)",
                "Renew Facebook Listings",
                "Delete Duplicate Listings",
                "Delete Specific Listing",
                "Delete All Listings"
            ],
            variable=self.auto_type,
            command=self.on_automation_type_change
        )
        self.entry_auto_type.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # CSV Path Field
        self.lbl_csv = ctk.CTkLabel(self.config_frame, text="Listings CSV/Excel:", anchor="w")
        self.lbl_csv.grid(row=1, column=0, padx=(0, 10), pady=5, sticky="w")
        self.entry_csv = ctk.CTkEntry(self.config_frame, textvariable=self.csv_path, placeholder_text="Select listings CSV or Excel file...")
        self.entry_csv.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.btn_browse_csv = ctk.CTkButton(self.config_frame, text="Browse", width=80, command=self.browse_csv)
        self.btn_browse_csv.grid(row=1, column=2, padx=(5, 0), pady=5)
        
        # Images Directory Field
        self.lbl_images = ctk.CTkLabel(self.config_frame, text="Images Directory:", anchor="w")
        self.lbl_images.grid(row=2, column=0, padx=(0, 10), pady=5, sticky="w")
        self.entry_images = ctk.CTkEntry(self.config_frame, textvariable=self.images_dir, placeholder_text="Select directory containing product images...")
        self.entry_images.grid(row=2, column=1, padx=5, pady=5, sticky="ew")
        self.btn_browse_images = ctk.CTkButton(self.config_frame, text="Browse", width=80, command=self.browse_images_dir)
        self.btn_browse_images.grid(row=2, column=2, padx=(5, 0), pady=5)
        
        # Session Path Field
        self.lbl_profile = ctk.CTkLabel(self.config_frame, text="FB Session Path:", anchor="w")
        self.lbl_profile.grid(row=3, column=0, padx=(0, 10), pady=5, sticky="w")
        self.entry_profile = ctk.CTkEntry(self.config_frame, textvariable=self.profile_dir)
        self.entry_profile.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.btn_browse_profile = ctk.CTkButton(self.config_frame, text="Browse", width=80, command=self.browse_profile_dir)
        self.btn_browse_profile.grid(row=3, column=2, padx=(5, 0), pady=5)
        
        # Specific Delete Keyword Field
        self.lbl_keyword = ctk.CTkLabel(self.config_frame, text="Delete Keyword / Title:", anchor="w")
        self.lbl_keyword.grid(row=4, column=0, padx=(0, 10), pady=5, sticky="w")
        self.entry_keyword = ctk.CTkEntry(self.config_frame, textvariable=self.delete_keyword, placeholder_text="Type specific listing title or keyword to delete...", state="disabled")
        self.entry_keyword.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        
        # Other Controls Frame (Delay and Headless)
        self.controls_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.controls_frame.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        
        self.lbl_delay = ctk.CTkLabel(self.controls_frame, text="Delay (seconds):")
        self.lbl_delay.pack(side="left", padx=(0, 10))
        self.entry_delay = ctk.CTkEntry(self.controls_frame, textvariable=self.delay_between_posts, width=60)
        self.entry_delay.pack(side="left", padx=(0, 30))
        
        self.cb_headless = ctk.CTkCheckBox(self.controls_frame, text="Run Headless (Hidden Browser)", variable=self.headless)
        self.cb_headless.pack(side="left")
        
        # Progress Bar and Status Label
        self.status_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.status_frame.grid(row=2, column=0, padx=20, pady=(10, 5), sticky="ew")
        
        self.lbl_status = ctk.CTkLabel(self.status_frame, text="Status: Ready", font=ctk.CTkFont(weight="bold"))
        self.lbl_status.pack(side="left")
        
        self.progress_bar = ctk.CTkProgressBar(self.main_frame)
        self.progress_bar.grid(row=3, column=0, padx=20, pady=(5, 10), sticky="ew")
        self.progress_bar.set(0)
        
        # Live Log Console
        self.log_label = ctk.CTkLabel(self.main_frame, text="Live Log Console", font=ctk.CTkFont(size=14, weight="bold"), anchor="w")
        self.log_label.grid(row=4, column=0, padx=20, pady=(10, 0), sticky="w")
        
        self.log_textbox = ctk.CTkTextbox(self.main_frame, height=250)
        self.log_textbox.grid(row=5, column=0, padx=20, pady=(5, 20), sticky="nsew")
        self.log_textbox.configure(state="disabled")
        
        self.log("Welcome to FB Marketplace Auto-Poster Bot!")
        self.log("Step 1: Click 'Login to FB First' to log in to your account manually and save session.")
        self.log("Step 2: Prepare your listings CSV, choose images, and click 'Start Posting'.\n")

    def log(self, message):
        """Append messages to the custom log textbox in GUI."""
        self.log_textbox.configure(state="normal")
        self.log_textbox.insert("end", f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_textbox.see("end")
        self.log_textbox.configure(state="disabled")

    def change_appearance_mode(self, new_appearance_mode: str):
        ctk.set_appearance_mode(new_appearance_mode)

    def on_automation_type_change(self, choice):
        if "Post Listings" in choice:
            self.entry_csv.configure(state="normal")
            self.btn_browse_csv.configure(state="normal")
            self.entry_images.configure(state="normal")
            self.btn_browse_images.configure(state="normal")
            self.entry_keyword.configure(state="disabled")
            self.log(f"Automation set to: {choice}. CSV and Images fields enabled.")
        elif choice == "Delete Specific Listing":
            self.entry_csv.configure(state="disabled")
            self.btn_browse_csv.configure(state="disabled")
            self.entry_images.configure(state="disabled")
            self.btn_browse_images.configure(state="disabled")
            self.entry_keyword.configure(state="normal")
            self.log(f"Automation set to: {choice}. Delete Keyword field enabled. Please type keyword/title to delete.")
        else:
            self.entry_csv.configure(state="disabled")
            self.btn_browse_csv.configure(state="disabled")
            self.entry_images.configure(state="disabled")
            self.btn_browse_images.configure(state="disabled")
            self.entry_keyword.configure(state="disabled")
            self.log(f"Automation set to: {choice}. CSV, Images, and Keyword fields disabled.")

    def browse_csv(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx *.xls"), ("All Files", "*.*")]
        )
        if file_path:
            self.csv_path.set(file_path)
            self.log(f"Selected Listing File: {file_path}")

    def browse_images_dir(self):
        folder = filedialog.askdirectory()
        if folder:
            self.images_dir.set(folder)
            self.log(f"Selected Images Folder: {folder}")

    def browse_profile_dir(self):
        folder = filedialog.askdirectory()
        if folder:
            self.profile_dir.set(folder)
            self.log(f"Selected Session Profile Folder: {folder}")

    def open_login_browser(self):
        """Open a non-headless browser to let the user log in once."""
        p_dir = self.profile_dir.get()
        if not p_dir:
            messagebox.showerror("Error", "Please specify a valid Session Path!")
            return
            
        os.makedirs(p_dir, exist_ok=True)
        self.log("Opening Chrome for login...")
        self.lbl_status.configure(text="Status: Logging in manually...")
        
        # Disable buttons during login process
        self.btn_login.configure(state="disabled")
        self.btn_start.configure(state="disabled")
        
        def run_browser():
            try:
                with sync_playwright() as p:
                    self.log("Launching browser with your profile...")
                    # Launch persistent chromium context
                    context = p.chromium.launch_persistent_context(
                        user_data_dir=p_dir,
                        headless=False,
                        args=["--disable-blink-features=AutomationControlled"]
                    )
                    page = context.new_page()
                    page.goto("https://www.facebook.com")
                    self.log("Browser opened. Please login to Facebook in the browser window.")
                    self.log("IMPORTANT: Do NOT close the browser manually until you log in fully.")
                    self.log("Once logged in and page loads, you can close the Chrome window to save the session.")
                    
                    # Keep browser open until user closes it
                    while True:
                        try:
                            if page.is_closed():
                                break
                            page.wait_for_timeout(500)
                        except Exception:
                            break
                    
                    try:
                        context.close()
                    except Exception:
                        pass
                self.log("Browser closed. Session saved successfully!")
            except Exception as e:
                self.log(f"Error opening browser: {e}")
            finally:
                self.lbl_status.configure(text="Status: Ready")
                self.btn_login.configure(state="normal")
                self.btn_start.configure(state="normal")
                
        threading.Thread(target=run_browser, daemon=True).start()

    def start_posting(self):
        choice = self.auto_type.get()
        profile = self.profile_dir.get()
        
        if not profile:
            messagebox.showerror("Error", "Please specify a valid FB Session Path!")
            return
            
        if "Post Listings" in choice:
            csv = self.csv_path.get()
            images = self.images_dir.get()
            if not csv or not os.path.exists(csv):
                messagebox.showerror("Error", "Please select a valid CSV/Excel file!")
                return
            if not images or not os.path.exists(images):
                messagebox.showerror("Error", "Please select a valid Images directory!")
                return
        
        if choice == "Delete Specific Listing":
            kw = self.delete_keyword.get().strip()
            if not kw:
                messagebox.showerror("Error", "Please enter a specific Listing Title or Keyword to delete!")
                return
                
        self.is_running = True
        self.btn_start.configure(state="disabled")
        self.btn_stop.configure(state="normal")
        self.btn_login.configure(state="disabled")
        self.lbl_status.configure(text=f"Status: Running ({choice})...")
        self.progress_bar.set(0)
        
        # Start automation in a background thread
        self.bot_thread = threading.Thread(target=self.run_bot_logic, daemon=True)
        self.bot_thread.start()

    def stop_posting(self):
        self.is_running = False
        self.log("Stopping bot... Please wait for current post to complete/exit.")
        self.lbl_status.configure(text="Status: Stopping...")

    def run_bot_logic(self):
        choice = self.auto_type.get()
        csv_file = self.csv_path.get()
        images_folder = self.images_dir.get()
        profile_folder = self.profile_dir.get()
        delay = self.delay_between_posts.get()
        is_headless = self.headless.get()
        
        try:
            with sync_playwright() as p:
                self.log("Launching automation browser...")
                context = p.chromium.launch_persistent_context(
                    user_data_dir=profile_folder,
                    headless=is_headless,
                    args=["--disable-blink-features=AutomationControlled"]
                )
                page = context.new_page()
                
                # Verify Login
                page.goto("https://www.facebook.com")
                time.sleep(3)
                if "login" in page.url or page.locator("input[name='email']").is_visible():
                    self.log("Error: You are not logged in! Please close and click 'Login to FB First' to log in.")
                    context.close()
                    self.reset_ui_state()
                    return
                
                if "Post Listings" in choice:
                    slower_mode = "New Accounts - Slower" in choice
                    
                    # Read Listings
                    if csv_file.endswith('.csv'):
                        df = pd.read_csv(csv_file)
                    else:
                        df = pd.read_excel(csv_file)
                        
                    df = df.fillna("")
                    total_items = len(df)
                    if total_items == 0:
                        self.log("Error: No items found in the data file.")
                        context.close()
                        self.reset_ui_state()
                        return
                        
                    self.log(f"Loaded {total_items} items. Starting posting...")
                    
                    for index, row in df.iterrows():
                        if not self.is_running:
                            self.log("Posting stopped by user.")
                            break
                            
                        self.log(f"--- Posting Item {index + 1} of {total_items} ---")
                        self.log(f"Product: {row['title']} | Price: {row['price']}")
                        
                        try:
                            # Navigate to create listing
                            self.log("Opening Marketplace creation page...")
                            page.goto("https://www.facebook.com/marketplace/create/item")
                            page.wait_for_selector("label:has-text('Title'), label[aria-label='Title']", timeout=20000)
                            time.sleep(2)
                            
                            # 1. Add Photos
                            photo_filenames = [x.strip() for x in str(row['images']).split(",") if x.strip()]
                            valid_photos = []
                            for filename in photo_filenames:
                                path = os.path.join(images_folder, filename)
                                if os.path.exists(path):
                                    valid_photos.append(path)
                                else:
                                    self.log(f"Warning: Image file not found: {path}")
                                    
                            if valid_photos:
                                self.log(f"Uploading {len(valid_photos)} image(s)...")
                                file_input = page.locator("input[type='file'][accept*='image']").first
                                try:
                                    file_input.set_input_files(valid_photos)
                                except Exception:
                                    with page.expect_file_chooser() as fc_info:
                                        page.locator("div[role='button']:has-text('Add Photos')").first.click()
                                    file_chooser = fc_info.value
                                    file_chooser.set_files(valid_photos)
                                time.sleep(3)
                            else:
                                raise Exception("No valid images found. Facebook Marketplace requires at least 1 image. Please check that filenames and extensions (like .png vs .jpg) match exactly.")
                                
                            # Human-like typing helper function to support "Slower" mode
                            def fill_field(locator, text):
                                locator.click()
                                page.keyboard.press("Control+A")
                                page.keyboard.press("Backspace")
                                time.sleep(0.5)
                                if slower_mode:
                                    # Type character by character with 100ms delay to mimic human
                                    locator.press_sequentially(str(text), delay=100)
                                else:
                                    locator.fill(str(text))
                                time.sleep(1)
                                
                            # 2. Fill Title
                            self.log("Filling Title...")
                            title_input = page.locator("label:has-text('Title') input, label[aria-label='Title'] input, input[aria-label='Title']").first
                            fill_field(title_input, row['title'])
                            
                            # 3. Fill Price
                            self.log("Filling Price...")
                            price_input = page.locator("label:has-text('Price') input, label[aria-label='Price'] input, input[aria-label='Price']").first
                            fill_field(price_input, int(row['price']))
                            
                            # 4. Fill Category
                            self.log("Selecting Category...")
                            category_select = page.locator("label:has-text('Category'), label[aria-label='Category']").first
                            category_select.click()
                            time.sleep(2 if not slower_mode else 4)
                            
                            category_name = str(row['category'])
                            option = page.get_by_role("option", name=category_name, exact=False).first
                            if option.is_visible():
                                option.click()
                            else:
                                page.locator("span").get_by_text(category_name, exact=False).first.click()
                            time.sleep(1.5 if not slower_mode else 3)
                            
                            # 5. Fill Condition
                            self.log("Selecting Condition...")
                            condition_select = page.locator("label:has-text('Condition'), label[aria-label='Condition']").first
                            condition_select.click()
                            time.sleep(2 if not slower_mode else 4)
                            
                            condition_val = str(row['condition']).lower()
                            condition_options = {
                                "new": ["New", "Naya"],
                                "like new": ["Used - Like New", "Used - Like new", "Like New"],
                                "very good": ["Used - Very Good", "Used - Very good", "Very Good"],
                                "good": ["Used - Good", "Used - Good", "Good"],
                                "fair": ["Used - Fair", "Used - Fair", "Fair"]
                            }
                            
                            match_found = False
                            possible_matches = condition_options.get(condition_val, ["New"])
                            for opt_name in possible_matches:
                                opt_locator = page.get_by_role("option", name=opt_name, exact=False).first
                                if opt_locator.is_visible():
                                    opt_locator.click()
                                    match_found = True
                                    break
                            if not match_found:
                                page.get_by_role("option").first.click()
                            time.sleep(1.5 if not slower_mode else 3)
                            
                            # 6. Fill Description
                            self.log("Filling Description...")
                            desc_input = page.locator("label:has-text('Description') textarea, label[aria-label='Description'] textarea, textarea[aria-label='Description']").first
                            fill_field(desc_input, row['description'])
                            
                            # 7. Fill Location
                            if 'location' in row and str(row['location']).strip():
                                self.log("Setting Location...")
                                loc_input = page.locator("label:has-text('Location') input, label[aria-label='Location'] input, input[aria-label='Location']").first
                                loc_input.click()
                                time.sleep(1)
                                page.keyboard.press("Control+A")
                                page.keyboard.press("Backspace")
                                time.sleep(0.5)
                                page.keyboard.type(str(row['location']))
                                time.sleep(4 if slower_mode else 3) # Wait for suggestions
                                
                                suggestion = page.locator("ul[role='listbox'] li, div[role='option']").first
                                if suggestion.is_visible():
                                    suggestion.click()
                                else:
                                    page.keyboard.press("Enter")
                                time.sleep(2)
                                
                            # 8. Click Next
                            self.log("Clicking Next...")
                            next_btn = page.locator("button:has-text('Next'), span:has-text('Next')").first
                            next_btn.click()
                            time.sleep(3 if not slower_mode else 5)
                            
                            # 9. Click Publish
                            self.log("Publishing Listing...")
                            publish_btn = page.locator("button:has-text('Publish'), span:has-text('Publish'), button:has-text('Post')").first
                            publish_btn.click()
                            
                            self.log("Waiting for listing to save...")
                            try:
                                page.wait_for_url("**/marketplace/**", timeout=15000)
                            except Exception:
                                time.sleep(8)
                            
                            self.log(f"Successfully posted Item {index + 1}!")
                            
                        except Exception as e:
                            screenshot_name = f"error_item_{index+1}.png"
                            screenshot_path = os.path.join(os.getcwd(), screenshot_name)
                            try:
                                page.screenshot(path=screenshot_path)
                                self.log(f"Saved error screenshot to: {screenshot_path}")
                            except Exception as screenshot_err:
                                self.log(f"Could not take screenshot: {screenshot_err}")
                            self.log(f"Error posting Item {index + 1}: {e}")
                            
                        # Update progress bar
                        progress = (index + 1) / total_items
                        self.progress_bar.set(progress)
                        
                        # Delay before next post
                        if index < total_items - 1 and self.is_running:
                            post_delay = delay if not slower_mode else (delay + 30) # Add extra 30s delay if slower mode is selected
                            self.log(f"Waiting {post_delay} seconds before posting next item...")
                            for d in range(post_delay):
                                if not self.is_running:
                                    break
                                time.sleep(1)
                                
                elif "Renew Facebook Listings" in choice:
                    self.log("Navigating to Selling Dashboard...")
                    page.goto("https://www.facebook.com/marketplace/you/selling")
                    page.wait_for_load_state("domcontentloaded")
                    time.sleep(6)
                    
                    self.log("Scanning for listings that can be renewed...")
                    renew_buttons = page.locator("button:has-text('Renew'), span:has-text('Renew'), div[role='button']:has-text('Renew')").all()
                    
                    total_renewed = 0
                    total_buttons = len(renew_buttons)
                    self.log(f"Found {total_buttons} renew buttons.")
                    
                    for i, btn in enumerate(renew_buttons):
                        if not self.is_running:
                            self.log("Renew process stopped by user.")
                            break
                        try:
                            if btn.is_visible():
                                btn.click()
                                time.sleep(4)
                                total_renewed += 1
                                self.log(f"Successfully renewed listing #{total_renewed}!")
                        except Exception as e:
                            self.log(f"Failed to click renew button #{i+1}: {e}")
                            
                        progress = (i + 1) / total_buttons if total_buttons > 0 else 1
                        self.progress_bar.set(progress)
                        
                    self.log(f"Renewal automation finished. Total listings renewed: {total_renewed}")
                    
                elif "Delete Duplicate Listings" in choice:
                    self.log("Navigating to Selling Dashboard...")
                    page.goto("https://www.facebook.com/marketplace/you/selling")
                    self.log("Waiting for listings to load...")
                    try:
                        page.wait_for_selector('div[aria-label*="More"], div[aria-label*="Manage"], button[aria-label*="More"], button[aria-label*="Manage"]', timeout=20000)
                    except Exception:
                        pass
                    time.sleep(4)
                    
                    self.log("Scanning listings for duplicates...")
                    deleted_count = 0
                    
                    while self.is_running:
                        # 1. Self-healing check: Is a deletion modal already open from a previous crash/run?
                        if self.confirm_deletion_dialog(page):
                            self.log("Self-healing: Dialog resolved. Refreshing page listings...")
                            time.sleep(2)
                            continue
                            
                        # Scroll down to load listings
                        for _ in range(2):
                            page.keyboard.press("PageDown")
                            time.sleep(1)
                            
                        buttons = page.locator('div[aria-label*="More"], div[aria-label*="Manage"], button[aria-label*="More"], button[aria-label*="Manage"]').all()
                        
                        seen_titles = set()
                        found_dup = False
                        
                        for btn in buttons:
                            try:
                                parent = btn
                                card_text = ""
                                for _ in range(6):
                                    parent = parent.locator("xpath=..")
                                    txt = parent.text_content()
                                    if txt and ("Active" in txt or "Listed" in txt or "Renew" in txt or "Delete" in txt or "Draft" in txt or "PKR" in txt):
                                        card_text = txt.strip()
                                        break
                                
                                if card_text:
                                    lines = [l.strip() for l in card_text.split("\n") if l.strip()]
                                    if lines:
                                        title = lines[0]
                                        if title not in ["Marketplace", "Inbox", "Selling", "Buying", "Active", "Renew", "Delete"]:
                                            if title in seen_titles:
                                                # Duplicate found! Delete immediately and break to refresh list
                                                self.log(f"Deleting duplicate listing: {title}")
                                                try:
                                                    page.evaluate("el => el.click()", btn.element_handle())
                                                except Exception:
                                                    btn.click(force=True)
                                                time.sleep(2.5)
                                                
                                                delete_opt = page.locator("span:has-text('Delete listing'), span:has-text('Delete Listing'), div[role='menuitem']:has-text('Delete')").first
                                                if delete_opt.is_visible():
                                                    try:
                                                        page.evaluate("el => el.click()", delete_opt.element_handle())
                                                    except Exception:
                                                        delete_opt.click(force=True)
                                                    time.sleep(3)
                                                    
                                                    if self.confirm_deletion_dialog(page):
                                                        deleted_count += 1
                                                        self.log(f"Deleted duplicate #{deleted_count} ({title})")
                                                        time.sleep(3)
                                                        found_dup = True
                                                        break
                                            else:
                                                seen_titles.add(title)
                            except Exception as dup_err:
                                self.log(f"Error checking duplicate element: {dup_err}")
                                continue
                                
                        if not found_dup:
                            self.log("No more duplicate listings found.")
                            break
                            
                elif choice == "Delete Specific Listing":
                    target_kw = self.delete_keyword.get().strip().lower()
                    self.log(f"Navigating to Selling Dashboard to delete items containing: '{target_kw}'...")
                    page.goto("https://www.facebook.com/marketplace/you/selling")
                    self.log("Waiting for listings to load...")
                    try:
                        page.wait_for_selector('div[aria-label*="More"], div[aria-label*="Manage"], button[aria-label*="More"], button[aria-label*="Manage"]', timeout=20000)
                    except Exception:
                        pass
                    time.sleep(4)
                    
                    deleted_count = 0
                    
                    while self.is_running:
                        # 1. Self-healing check: Is a deletion modal already open from a previous crash/run?
                        if self.confirm_deletion_dialog(page):
                            self.log("Self-healing: Dialog resolved. Refreshing page listings...")
                            time.sleep(2)
                            continue
                            
                        # Scroll down a few times to load listings
                        for _ in range(2):
                            page.keyboard.press("PageDown")
                            time.sleep(1)
                            
                        buttons = page.locator('div[aria-label*="More"], div[aria-label*="Manage"], button[aria-label*="More"], button[aria-label*="Manage"]').all()
                        found_match = False
                        
                        for btn in buttons:
                            try:
                                parent = btn
                                card_text = ""
                                for _ in range(6):
                                    parent = parent.locator("xpath=..")
                                    txt = parent.text_content()
                                    if txt and ("Active" in txt or "Listed" in txt or "Renew" in txt or "Delete" in txt or "Draft" in txt or "PKR" in txt):
                                        card_text = txt.strip()
                                        break
                                
                                if card_text and target_kw in card_text.lower():
                                    lines = [l.strip() for l in card_text.split("\n") if l.strip()]
                                    title = lines[0] if lines else "Matching Listing"
                                    # Avoid system lines
                                    if title not in ["Marketplace", "Inbox", "Selling", "Buying", "Active", "Renew", "Delete"]:
                                        self.log(f"Deleting matching listing: {title}")
                                        try:
                                            page.evaluate("el => el.click()", btn.element_handle())
                                        except Exception:
                                            btn.click(force=True)
                                        time.sleep(2.5)
                                        
                                        delete_opt = page.locator("span:has-text('Delete listing'), span:has-text('Delete Listing'), div[role='menuitem']:has-text('Delete')").first
                                        if delete_opt.is_visible():
                                            try:
                                                page.evaluate("el => el.click()", delete_opt.element_handle())
                                            except Exception:
                                                delete_opt.click(force=True)
                                            time.sleep(3)
                                            
                                            if self.confirm_deletion_dialog(page):
                                                deleted_count += 1
                                                self.log(f"Deleted listing #{deleted_count} ({title})")
                                                time.sleep(3)
                                                found_match = True
                                                break
                            except Exception as inner_err:
                                self.log(f"Error during item deletion process: {inner_err}")
                                continue
                                
                        if not found_match:
                            self.log("No more matching listings found.")
                            break
                    
                elif "Delete All Listings" in choice:
                    self.log("Navigating to Selling Dashboard...")
                    page.goto("https://www.facebook.com/marketplace/you/selling")
                    self.log("Waiting for listings to load...")
                    try:
                        page.wait_for_selector('div[aria-label*="More"], div[aria-label*="Manage"], button[aria-label*="More"], button[aria-label*="Manage"], div[role="button"][aria-label*="Manage"]', timeout=20000)
                    except Exception:
                        pass
                    time.sleep(4)
                    
                    self.log("Starting Deletion of All Listings...")
                    deleted_count = 0
                    
                    while self.is_running:
                        # 1. Self-healing check: Is a deletion modal already open from a previous crash/run?
                        if self.confirm_deletion_dialog(page):
                            self.log("Self-healing: Dialog resolved. Refreshing page listings...")
                            time.sleep(2)
                            continue
                            
                        btn = page.locator('div[aria-label*="More"], div[aria-label*="Manage"], button[aria-label*="More"], button[aria-label*="Manage"], div[role="button"][aria-label*="Manage"]').first
                        if not btn.is_visible():
                            # Scroll down once to check if more load
                            page.keyboard.press("PageDown")
                            time.sleep(2)
                            btn = page.locator('div[aria-label*="More"], div[aria-label*="Manage"], button[aria-label*="More"], button[aria-label*="Manage"], div[role="button"][aria-label*="Manage"]').first
                            if not btn.is_visible():
                                self.log("No more listings found to delete.")
                                break
                                
                        try:
                            # Try to extract title for logging
                            try:
                                parent = btn
                                card_text = ""
                                for _ in range(6):
                                    parent = parent.locator("xpath=..")
                                    txt = parent.text_content()
                                    if txt and ("Active" in txt or "Listed" in txt or "Renew" in txt or "Delete" in txt or "Draft" in txt or "PKR" in txt):
                                        card_text = txt.strip()
                                        break
                                lines = [l.strip() for l in card_text.split("\n") if l.strip()]
                                title_text = lines[0] if lines else "Unknown Item"
                            except Exception:
                                title_text = "Unknown Item"
                                
                            self.log(f"Deleting item: {title_text}")
                            try:
                                page.evaluate("el => el.click()", btn.element_handle())
                            except Exception:
                                btn.click(force=True)
                            time.sleep(2.5)
                            
                            delete_opt = page.locator("span:has-text('Delete listing'), span:has-text('Delete Listing'), div[role='menuitem']:has-text('Delete')").first
                            if delete_opt.is_visible():
                                try:
                                    page.evaluate("el => el.click()", delete_opt.element_handle())
                                except Exception:
                                    delete_opt.click(force=True)
                                time.sleep(3)
                                
                                if self.confirm_deletion_dialog(page):
                                    deleted_count += 1
                                    self.log(f"Deleted listing #{deleted_count} ({title_text})")
                                    time.sleep(2)
                            else:
                                page.mouse.click(10, 10)
                        except Exception as e:
                            self.log(f"Error during delete operation: {e}")
                            break
                            
                    self.log(f"Delete All Listings finished. Total deleted: {deleted_count}")
                    
                context.close()
                self.log("All automation activities finished.")
                
        except Exception as general_err:
            self.log(f"An unexpected error occurred: {general_err}")
            
        self.reset_ui_state()

    def confirm_deletion_dialog(self, page):
        """Resolve a Facebook deletion confirmation dialog using keyboard navigation."""
        try:
            time.sleep(2)
            
            # --- Find the correct dialog (the one with actual delete confirmation) ---
            all_dialogs = page.locator("div[role='dialog']").all()
            target_dialog = None
            for dlg in all_dialogs:
                try:
                    dlg_text = dlg.text_content().lower()
                    if "sure you want to delete" in dlg_text or ("delete" in dlg_text and "cancel" in dlg_text):
                        target_dialog = dlg
                        break
                except Exception:
                    continue
            
            if target_dialog is None:
                return False
            
            self.log("Confirmation dialog found. Attempting to resolve...")
            
            # --- Strategy 1: Playwright get_by_role (most reliable, handles div[role=button] too) ---
            try:
                delete_btn = page.get_by_role("button", name="Delete", exact=True)
                if delete_btn.count() > 0:
                    self.log("Strategy 1: Found Delete button via get_by_role. Clicking...")
                    delete_btn.first.click(force=True)
                    time.sleep(5)
                    return True
            except Exception as e1:
                self.log(f"Strategy 1 failed: {e1}")

            # --- Strategy 2: Pure JavaScript — scan ALL clickable elements for exact "Delete" text ---
            try:
                result = page.evaluate("""
                    () => {
                        const candidates = document.querySelectorAll('[role="dialog"] [role="button"], [role="dialog"] button');
                        for (const el of candidates) {
                            if (el.innerText && el.innerText.trim() === 'Delete') {
                                el.click();
                                return true;
                            }
                        }
                        return false;
                    }
                """)
                if result:
                    self.log("Strategy 2: Clicked Delete via pure JS scan.")
                    time.sleep(5)
                    return True
            except Exception as e2:
                self.log(f"Strategy 2 failed: {e2}")
            
            # --- Strategy 3: Target dialog's last clickable element (Delete is always after Cancel) ---
            try:
                clickables = target_dialog.locator("[role='button'], button").all()
                self.log(f"Strategy 3: Found {len(clickables)} clickable(s) in dialog.")
                for el in reversed(clickables):
                    try:
                        txt = el.text_content().strip()
                        self.log(f"  Candidate: '{txt}'")
                        if txt == "Delete":
                            page.evaluate("el => el.click()", el.element_handle())
                            self.log("Strategy 3: Clicked last Delete element via JS.")
                            time.sleep(5)
                            return True
                    except Exception:
                        continue
            except Exception as e3:
                self.log(f"Strategy 3 failed: {e3}")

            self.log("All strategies failed — dialog could not be resolved.")
            return False

        except Exception as err:
            self.log(f"Error inside confirm_deletion_dialog: {err}")
            return False


    def reset_ui_state(self):
        self.is_running = False
        self.btn_start.configure(state="normal")
        self.btn_stop.configure(state="disabled")
        self.btn_login.configure(state="normal")
        self.lbl_status.configure(text="Status: Ready")

if __name__ == "__main__":
    # Check if playwright chromium is installed, if not try to install it
    try:
        app = FBMarketplaceBotApp()
        app.mainloop()
    except Exception as err:
        print(f"Error starting GUI: {err}")
        input("Press Enter to exit...")
