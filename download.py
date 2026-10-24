import os
import re
import time
import zipfile
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

# ==========================================
# IKKADA MEE LOGIN DETAILS ENTER CHEYYANDI
# ==========================================
USERNAME = "user_name"
PASSWORD = "password"

# 1. Mee Desktop meeda 'SurveyStars_Downloads' ane folder create avtundi
download_folder = os.path.join(os.path.expanduser("~"), "Desktop", "SurveyStars_Downloads")
os.makedirs(download_folder, exist_ok=True)

options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_folder,
    "download.prompt_for_download": False,
    "safebrowsing.enabled": True,
    "profile.default_content_setting_values.automatic_downloads": 1,
    "profile.default_content_setting_values.popups": 0
}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(options=options)

def wait_for_all_downloads_to_finish(folder, timeout=300):
    """Chivarlo anni downloads poorthi ayye varaku Chrome close avvakunda wait chestundi"""
    print("\nBackground lo unna downloads anni complete avvadaniki wait chestondi...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        files = os.listdir(folder)
        downloading = [f for f in files if f.endswith('.crdownload') or f.endswith('.tmp')]
        if not downloading:
            print("SUCCESS! Anni zip files 100% download aipoyayi!")
            return True
        print(f"   -> Inka {len(downloading)} file(s) download avtunnayi... waiting...")
        time.sleep(3)
    return False

def unzip_and_rename_files(folder):
    """Zip files ni clean folder name tho extract chesi, underscore (_) tarvata letters remove chestundi"""
    print("\n" + "="*60)
    print("Zip files ni Rename & Unzip (Extract) chestondi...")
    print("="*60)
    
    for filename in os.listdir(folder):
        if filename.lower().endswith(".zip"):
            zip_path = os.path.join(folder, filename)
            
            # 1. '.zip' extension teeseyyadam
            name_without_ext = os.path.splitext(filename)[0]
            
            # 2. Underscore (_) daggara cut chesi mundu unna Survey No. matrame teesukovadam
            # Ex: 'IS-142219 FI__IQGCN29' -> 'IS-142219 FI'
            clean_name = name_without_ext.split('_')[0].strip()
            
            # Clean peru tho folder path tayaru cheyyadam
            extract_folder_path = os.path.join(folder, clean_name)
            os.makedirs(extract_folder_path, exist_ok=True)
            
            try:
                # 3. Zip file ni aa clean folder loki extract cheyyadam
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(extract_folder_path)
                print(f"   -> Extracted: '{filename}'  ===>  Folder: '{clean_name}'")
                
                # 4. Extract chesina folder lopala unna files ki kuda '_' tarvata letters unte remove cheyyadam
                for root, dirs, files in os.walk(extract_folder_path):
                    for f in files:
                        if '_' in f:
                            f_base, f_ext = os.path.splitext(f)
                            new_f_base = f_base.split('_')[0].strip()
                            if new_f_base:
                                old_file_path = os.path.join(root, f)
                                new_file_path = os.path.join(root, new_f_base + f_ext)
                                if not os.path.exists(new_file_path):
                                    os.rename(old_file_path, new_file_path)

                # 5. Unzip aipoyaka paatha .zip file ni delete chestundi 
                # (Okavela .zip file kuda alane undali anukunte, kindha line mundu '#' pettandi)
                os.remove(zip_path)
                
            except Exception as e:
                print(f"   -> '{filename}' unzip cheyyadam lo error: {e}")

try:
    # 2. Website open chesi Automatic ga Login avvadam
    print("Website open chestondi...")
    driver.get("https://www.surveystars.com/")
    time.sleep(4)

    print("Username mariyu Password enter chestondi...")
    try:
        pass_box = driver.find_element(By.XPATH, "//input[@type='password']")
        user_box = pass_box.find_element(By.XPATH, "./preceding::input[@type='text' or @type='email' or not(@type)][1]")

        user_box.clear()
        user_box.send_keys(USERNAME)
        time.sleep(1)

        pass_box.clear()
        pass_box.send_keys(PASSWORD)
        time.sleep(1)

        pass_box.send_keys(Keys.RETURN)
        print("Login submit cheyyabadindi! 6 seconds wait chestondi...")
        time.sleep(6)

    except Exception as e:
        print(f"Auto-login lo samasya: {e}")
        input("Dayachesi Chrome lo manual ga login ayyi, ikkada ENTER nokkandi >> ")

    # 3. Order List (Suborder) page ki velladam
    suborder_url = "https://www.surveystars.com/home.php?page=suborder&query=3"
    print("Order List page open chestondi...")
    driver.get(suborder_url)
    time.sleep(5)

    main_window = driver.current_window_handle

    # 4. Order List lo unna rows count cheyyadam
    rows_xpath = "//tr[.//input[@value='Edit'] or .//button[contains(., 'Edit')] or .//a[contains(., 'Edit')] or td[contains(., 'IS-')]]"
    rows = driver.find_elements(By.XPATH, rows_xpath)
    total_surveys = len(rows)
    
    print(f"\nOrder List lo motham {total_surveys} Jobs kanipinchayi!")
    print("Order List page nunde prathi Job ni New Tab lo open chestondi...\n")

    # =========================================================================
    # STEP 1: ORDER LIST PAGE LONE UNDI PRATHI JOB NI NEW TAB LO OPEN CHEYYADAM
    # =========================================================================
    for i in range(total_surveys):
        driver.switch_to.window(main_window)
        current_rows = driver.find_elements(By.XPATH, rows_xpath)
        if i >= len(current_rows):
            break
        row = current_rows[i]
        
        tds = row.find_elements(By.TAG_NAME, "td")
        survey_no = tds[1].text.strip() if len(tds) > 1 else f"Order_{i+1}"
        print(f"   -> [{i+1}/{total_surveys}] Order List nundi New Tab open chestondi: {survey_no}")

        edit_btns = row.find_elements(By.XPATH, ".//input[@value='Edit'] | .//button[contains(., 'Edit')] | .//a[contains(., 'Edit')]")
        target = edit_btns[0] if edit_btns else (tds[1].find_elements(By.TAG_NAME, "a")[0] if (len(tds) > 1 and tds[1].find_elements(By.TAG_NAME, "a")) else row)

        tabs_before = len(driver.window_handles)
        href = target.get_attribute("href") or ""
        onclick_str = target.get_attribute("onclick") or row.get_attribute("onclick") or (tds[1].get_attribute("onclick") if len(tds) > 1 else "") or ""

        if href and not href.startswith("javascript:") and not href.endswith("#"):
            driver.execute_script("window.open(arguments[0], '_blank');", href)
        elif "home.php" in onclick_str or "location" in onclick_str:
            match = re.search(r"['\"]([^'\"]*home\.php[^'\"]*)['\"]", onclick_str)
            if match:
                job_url = match.group(1)
                driver.execute_script("window.open(arguments[0], '_blank');", job_url)
            else:
                modified_js = onclick_str.replace("window.location.href", "window.__new_tab_url").replace("window.location", "window.__new_tab_url").replace("location.href", "window.__new_tab_url").replace("document.location", "window.__new_tab_url")
                driver.execute_script(f"""
                    window.__new_tab_url = null;
                    var el = arguments[0];
                    var form = el.closest('form');
                    if (form) {{ form.setAttribute('target', '_blank'); }}
                    {modified_js}
                    if (window.__new_tab_url) {{
                        window.open(window.__new_tab_url, '_blank');
                    }}
                """, target)
        else:
            driver.execute_script("""
                var el = arguments[0];
                var form = el.closest('form');
                if (form) { form.setAttribute('target', '_blank'); }
            """, target)
            ActionChains(driver).key_down(Keys.CONTROL).click(target).key_up(Keys.CONTROL).perform()

        time.sleep(1.5)
        
        if len(driver.window_handles) == tabs_before:
            if driver.current_url != suborder_url:
                job_url = driver.current_url
                driver.execute_script("window.open(arguments[0], '_blank');", job_url)
                driver.get(suborder_url)
                time.sleep(3)
            else:
                driver.execute_script("window.open(arguments[0], '_blank');", suborder_url)
                time.sleep(2)
                new_tab = [h for h in driver.window_handles if h != main_window][-1]
                driver.switch_to.window(new_tab)
                time.sleep(2)
                dup_rows = driver.find_elements(By.XPATH, rows_xpath)
                if i < len(dup_rows):
                    dup_btns = dup_rows[i].find_elements(By.XPATH, ".//input[@value='Edit'] | .//button[contains(., 'Edit')] | .//a[contains(., 'Edit')]")
                    if dup_btns:
                        driver.execute_script("arguments[0].click();", dup_btns[0])
                    else:
                        dup_rows[i].find_elements(By.TAG_NAME, "td")[1].click()

    print("\nAnni Jobs veru-veru Tabs lo open ayyayi! Load avvadaniki 4 seconds wait chestondi...")
    time.sleep(4)

    # =========================================================================
    # STEP 2: OPEN AINA ANNI JOB TABS LO 'DOWNLOAD AS .ZIP' CLICK CHEYYADAM
    # =========================================================================
    job_tabs = [h for h in driver.window_handles if h != main_window]
    print(f"\nMotham {len(job_tabs)} Job Tabs lo varusaga 'Download as .zip' click chestondi...")

    for idx, tab in enumerate(job_tabs, start=1):
        driver.switch_to.window(tab)
        time.sleep(1)
        zip_buttons = driver.find_elements(
            By.XPATH, 
            "//a[contains(@onclick, 'zip_order_docs') or contains(normalize-space(), 'Download as .zip')]"
        )
        if zip_buttons:
            print(f"   -> [Tab {idx}] Clicking 'Download as .zip'...")
            driver.execute_script("arguments[0].click();", zip_buttons[0])
        else:
            print(f"   -> [Tab {idx}] 'Download as .zip' button kanipinchaledu.")

    # =========================================================================
    # STEP 3: ANNI TABS LO ZIP READY AVVAGANE DOWNLOAD START CHEYYADAM
    # =========================================================================
    print("\nAnni Tabs lo Zip files ready avvagane automatic ga download chestundi...")
    pending_tabs = list(job_tabs)
    start_wait = time.time()

    while pending_tabs and (time.time() - start_wait < 60):
        for tab in list(pending_tabs):
            driver.switch_to.window(tab)
            popup_links = driver.find_elements(
                By.XPATH, 
                "//a[contains(@href, '.zip') or contains(@href, 'download') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'click here') or contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'download')]"
            )
            for p_link in popup_links:
                try:
                    if p_link.is_displayed() and "Download as .zip" not in p_link.text:
                        print(f"   -> Tab lo Zip ready ayyindi! Starting download...")
                        driver.execute_script("arguments[0].click();", p_link)
                        pending_tabs.remove(tab)
                        time.sleep(1)
                        break
                except:
                    pass
        time.sleep(1.5)

    # Chivarlo anni downloads complete ayye varaku wait chestundi
    wait_for_all_downloads_to_finish(download_folder, timeout=300)
    time.sleep(2)

    # =========================================================================
    # STEP 4: UNZIP & RENAME (UNDERSCORE TARVATA LETTERS REMOVE CHEYYADAM)
    # =========================================================================
    unzip_and_rename_files(download_folder)

    print(f"\nALL DONE! Anni folders ee path lo ready ga unnayi:\n{download_folder}")
    time.sleep(5)

finally:
    driver.quit()