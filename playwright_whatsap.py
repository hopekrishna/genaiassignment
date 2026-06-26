from playwright.sync_api import sync_playwright,TimeoutError
import pandas as pd
import time
import os
import json
from datetime import datetime
from openpyxl import Workbook,load_workbook

wb = Workbook()
ws = wb.active

ws.append(["Name", "Phone", "Message"])
ws.append(["sasikumaar", "+917892328094", "Hello {name}"])
ws.append(["daughter", "+919384006078", "Good Morning {name}"])

wb.save("contacts.xlsx")

contacts = pd.read_excel("contacts.xlsx")

print("contacts.xlsx created")

received_data = []
json_report=[]

with sync_playwright() as p:

    browser = p.chromium.launch_persistent_context(
        user_data_dir="whatsapp_profile",
        headless=False
    )

    page = browser.new_page()
    page.goto("https://web.whatsapp.com")
    page.wait_for_load_state("networkidle")

    print("Scan the QR code if required...")
    page.wait_for_load_state("networkidle")

    print("Login successful!")
    print("Please scan QR Code...")
    page.wait_for_load_state("networkidle")

    for index, row in contacts.iterrows():

        name = row["Name"]
        phone = str(row["Phone"])
        message = row["Message"]

        print(f"Sending message to {name}")

        whatsapp_url = (
            f"https://web.whatsapp.com/send?phone={phone}"
            f"&text={message}"
        )
        page.wait_for_load_state("networkidle")

        page.goto(whatsapp_url)
        page.wait_for_load_state("networkidle")
             

        time.sleep(5)

        try:

            message_box = page.locator('div[contenteditable="true"]').last
            page.wait_for_timeout(5000)
            message_box.click()
            message_box.fill(str(message).replace("{name}", name))
            page.keyboard.press("Enter")
            print(f"Message sent to {name}")

            time.sleep(3)
            messages = page.locator('[data-testid="msg-container"]')
            count = messages.count()

            if count > 0:
               latest_msg = messages.nth(count - 1).inner_text()
               print("Latest incoming message:", latest_msg)
            
                   
            received_data.append({
               "Name": name,
               "Phone": phone,
               "Message":latest_msg,
               "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
               })
            json_report.append({
               "Name": name,
               "Phone": phone,
               "Message Sent": str(message).replace("{name}", name),
               "Latest Reply": latest_msg if count > 0 else "",
               "Status": "Success",
               "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
               })
            
            
            folder = r"C:\Users\lallu\OneDrive\Desktop\stgrade\playwright_whatsapp_bot"
            report_name = os.path.join(
                 folder,
                 f"extracted_messages_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
            )    
            df = pd.DataFrame(received_data)
            df.to_excel(report_name, index=False)
            print("Saved:", report_name)
            print("Exists:", os.path.exists(report_name))
            folder = r"C:\Users\lallu\OneDrive\Desktop\stgrade\playwright_whatsapp_bot"
            json_file = os.path.join(
                 folder,
                 f"whatsapp_report_{datetime.now().strftime('%Y-%m-%d')}.json"
            )

            with open(json_file, "w", encoding="utf-8") as file:
                 json.dump(json_report, file, indent=4, ensure_ascii=False)
        
            
        except Exception as e:
            print(f"Failed for {name}: {e}")
            json_report.append({
               "Name": name,
               "Phone": phone,
               "Message Sent": str(message).replace("{name}", name),
               "Status": "Failed",
               "Error": str(e),
               "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            page.screenshot(
                 path=f"whatsapp_report_{datetime.now().strftime('%Y-%m-%d')}.png",
                 full_page=True
            )      
            print(f"Report saved as {report_name}")
            print("JSON report saved:", json_file)
            browser.close()
              
           