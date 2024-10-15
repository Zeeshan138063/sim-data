import json
import logging
import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk

from curl_cffi import requests

from bs4 import BeautifulSoup
from requests.exceptions import RequestException

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("sim_info_extractor.log"),
        logging.StreamHandler()
    ]
)


class SimInfoExtractor:
    def __init__(self, phone_no):
        self.phone_no = phone_no
        self.final_data = {}
        logging.info(f"Initialized SimInfoExtractor for phone number: {self.phone_no}")

    def siminfo(self):
        logging.info("Fetching SimInfo data...")
        cookies = {
            '_lscache_vary': '335b5e8105efef74544d3968d6a2b4be',
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)',
        }
        data = {
            'phoneNumber': self.phone_no,
            'submit': 'submit',
        }
        try:
            response = requests.post('https://simsinfopk.com/sim-info-3', cookies=cookies, headers=headers, data=data,
                                     timeout=10)
            response.raise_for_status()
            logging.info("SimInfo data fetched successfully.")
            self.parse_siminfo(response.text)
        except RequestException as e:
            logging.error(f"Error fetching SimInfo data: {e}")
            messagebox.showerror("Network Error", f"Failed to fetch SimInfo data.\n{e}")

    def parse_siminfo(self, html_content):
        logging.info("Parsing SimInfo data...")
        try:
            soup = BeautifulSoup(html_content, 'lxml')
            results = soup.find_all('div', class_='container')
            sim_data = []
            for result in results:
                mobile_number = result.find('dt', string='Mobile #').find_next_sibling('dd').get_text(strip=True)
                name = result.find('dt', string='Name').find_next_sibling('dd').get_text(strip=True)
                cnic = result.find('dt', string='CNIC').find_next_sibling('dd').get_text(strip=True)
                address = result.find('dt', string='Address').find_next_sibling('dd').get_text(strip=True)
                operator = result.find('dt', string='Operator').find_next_sibling('dd').get_text(strip=True)
                sim_data.append({
                    'Mobile Number': mobile_number,
                    'Name': name,
                    'CNIC': cnic,
                    'Address': address,
                    'Operator': operator
                })
            self.final_data['SimInfo'] = sim_data
            logging.info("SimInfo data parsed successfully.")
        except AttributeError as e:
            logging.error(f"Error parsing SimInfo data: {e}")
            messagebox.showerror("Parsing Error", f"Failed to parse SimInfo data.\n{e}")

    def simownerdata(self):
        logging.info("Fetching SimOwnerData...")
        cookies = {
            '_ga': 'GA1.1.2125757576.1725458150',
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)',
        }
        data = {
            'action': 'get_number_data',
            'get_number_data': f'searchdata={self.phone_no}'
        }
        try:
            response = requests.post('https://simownerdata.com.pk/wp-admin/admin-ajax.php', cookies=cookies,
                                     headers=headers, data=data, timeout=10)
            response.raise_for_status()
            html_data = response.json().get('data')
            if html_data:
                self.parse_simownerdata(html_data)
                logging.info("SimOwnerData fetched and parsed successfully.")
            else:
                logging.warning("No data found in SimOwnerData response.")
                messagebox.showwarning("No Data", "No SimOwnerData found for the provided phone number.")
        except RequestException as e:
            logging.error(f"Error fetching SimOwnerData: {e}")
            messagebox.showerror("Network Error", f"Failed to fetch SimOwnerData.\n{e}")
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding SimOwnerData JSON: {e}")
            messagebox.showerror("Data Error", f"Invalid JSON response for SimOwnerData.\n{e}")

    def parse_simownerdata(self, html_content):
        logging.info("Parsing SimOwnerData...")
        try:
            soup = BeautifulSoup(html_content, 'lxml')
            result_cards = soup.find_all('div', class_='result-card')
            owner_data = []
            for card in result_cards:
                full_name = card.find('label', string='FULL NAME').find_next('div').get_text(strip=True)
                phone = card.find('label', string='PHONE #').find_next('div').get_text(strip=True)
                cnic = card.find('label', string='CNIC #').find_next('div').get_text(strip=True)
                address = card.find('label', string='ADDRESS').find_next('div').get_text(strip=True)
                owner_data.append({
                    'Full Name': full_name,
                    'Phone': phone,
                    'CNIC': cnic,
                    'Address': address
                })
            self.final_data['SimOwnerData'] = owner_data
            logging.info("SimOwnerData parsed successfully.")
        except AttributeError as e:
            logging.error(f"Error parsing SimOwnerData: {e}")
            messagebox.showerror("Parsing Error", f"Failed to parse SimOwnerData.\n{e}")

    def simdatabaseinfo(self):
        logging.info("Fetching SimDatabaseInfo...")
        cookies = {
            'ci_session': 'f5973b05d17e58b65a5b7d0de24662db7077e49b',
        }
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)',
        }
        data = {
            'query': self.phone_no,
        }
        try:
            response = requests.post('https://simdatabase.info/result', cookies=cookies, headers=headers, data=data,
                                     timeout=10)
            response.raise_for_status()
            self.simdatabaseinfo_parser(response.text)
            logging.info("SimDatabaseInfo fetched successfully.")
        except RequestException as e:
            logging.error(f"Error fetching SimDatabaseInfo: {e}")
            messagebox.showerror("Network Error", f"Failed to fetch SimDatabaseInfo.\n{e}")

    def simdatabaseinfo_parser(self, html_content):
        logging.info("Parsing SimDatabaseInfo...")
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            results = soup.find_all('div', class_='container bg-light w-100 my-5')
            sim_data = []
            for result in results:
                mobile_number = result.find('dt', string='Mobile #').find_next_sibling('dd').get_text(strip=True)
                name = result.find('dt', string='Name').find_next_sibling('dd').get_text(strip=True)
                cnic = result.find('dt', string='CNIC').find_next_sibling('dd').get_text(strip=True)
                address = result.find('dt', string='Address').find_next_sibling('dd').get_text(strip=True) or "N/A"
                operator = result.find('dt', string='Operator').find_next_sibling('dd').get_text(strip=True)
                sim_data.append({
                    'Mobile Number': mobile_number,
                    'Name': name,
                    'CNIC': cnic,
                    'Address': address,
                    'Operator': operator
                })
            self.final_data['SimDatabaseInfo'] = sim_data
            logging.info("SimDatabaseInfo parsed successfully.")
        except AttributeError as e:
            logging.error(f"Error parsing SimDatabaseInfo: {e}")
            messagebox.showerror("Parsing Error", f"Failed to parse SimDatabaseInfo.\n{e}")

    def export_to_json(self):
        filename = f"{self.phone_no}_sim_data.json"
        try:
            with open(filename, 'w') as json_file:
                json.dump(self.final_data, json_file, indent=4)
            logging.info(f"Data exported to JSON file: {filename}")
            return filename
        except IOError as e:
            logging.error(f"Error writing to JSON file {filename}: {e}")
            messagebox.showerror("File Error", f"Failed to write data to {filename}.\n{e}")
            return "Error"


class SimInfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sim Info Extractor")
        self.root.geometry("700x600")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(False, False)

        # Style configuration
        style = ttk.Style()
        style.configure('TButton', font=('Arial', 12))
        style.configure('TLabel', font=('Arial', 12))
        style.configure('Header.TLabel', font=('Arial', 16, 'bold'))

        # Header Label
        self.header_label = ttk.Label(root, text="SIM Information Extractor", style='Header.TLabel',
                                      background="#f0f0f0")
        self.header_label.pack(pady=20)

        # Frame for input
        self.input_frame = ttk.Frame(root, padding="10 10 10 10")
        self.input_frame.pack(pady=10)

        # Label for phone number
        self.label = ttk.Label(self.input_frame, text="Enter Phone Number:")
        self.label.grid(row=0, column=0, padx=5, pady=5, sticky='E')

        # Entry for phone number
        self.entry = ttk.Entry(self.input_frame, width=30, font=("Arial", 12))
        self.entry.grid(row=0, column=1, padx=5, pady=5)

        # Button to fetch data
        self.button = ttk.Button(root, text="Get Sim Info", command=self.get_sim_info)
        self.button.pack(pady=10)

        # Separator
        self.separator = ttk.Separator(root, orient='horizontal')
        self.separator.pack(fill='x', pady=10)

        # Scrolled Text to display results
        self.result_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20, font=("Arial", 10))
        self.result_display.pack(pady=10)

    def get_sim_info(self):
        phone_no = self.entry.get().strip()
        if not phone_no:
            messagebox.showerror("Input Error", "Please enter a valid phone number.")
            logging.warning("User attempted to fetch data without entering a phone number.")
            return

        # Clear previous results
        self.result_display.delete(1.0, tk.END)
        self.result_display.insert(tk.END, "Fetching data...\n")
        logging.info(f"User initiated data extraction for phone number: {phone_no}")

        # Create an instance of SimInfoExtractor
        sim_info_extractor = SimInfoExtractor(phone_no)

        # Fetch and parse data
        sim_info_extractor.siminfo()
        sim_info_extractor.simownerdata()
        sim_info_extractor.simdatabaseinfo()

        # Check if data was successfully fetched
        if sim_info_extractor.final_data:
            # Display the data in the scrolled text widget
            self.result_display.delete(1.0, tk.END)  # Clear previous text
            for key, value in sim_info_extractor.final_data.items():
                self.result_display.insert(tk.END, f"{key}:\n")
                for item in value:
                    self.result_display.insert(tk.END, json.dumps(item, indent=4))
                    self.result_display.insert(tk.END, "\n")
            # Export to JSON
            filename = sim_info_extractor.export_to_json()
            if filename != "Error":
                messagebox.showinfo("Success", f"Data extracted and saved to {filename}")
            else:
                messagebox.showerror("Export Error", "Data extraction succeeded but failed to save to JSON.")
        else:
            self.result_display.delete(1.0, tk.END)
            self.result_display.insert(tk.END, "No data found or an error occurred during data extraction.\n")
            logging.warning("No data extracted for the provided phone number.")


if __name__ == '__main__':
    try:
        root = tk.Tk()
        app = SimInfoApp(root)
        root.mainloop()
    except Exception as e:
        logging.critical(f"Unhandled exception: {e}")
        messagebox.showerror("Application Error", f"An unexpected error occurred.\n{e}")
