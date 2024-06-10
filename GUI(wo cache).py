import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from ttkthemes import ThemedStyle
import requests
import time
import json

class CustomDialog(simpledialog.Dialog):
    def __init__(self, parent, title=None):
        self.token = ''
        self.style = ThemedStyle(parent)
        self.style.set_theme("arc")
        super().__init__(parent, title=title)

    def body(self, master):
        self.configure(bg='#2b2b2b')
        ttk.Label(master, text="Enter 'exit' to exit the program or provide a new GitHub token:", background='#2b2b2b', foreground='white').pack(pady=10)
        self.token_entry = ttk.Entry(master, width=50, style="Custom.TEntry")
        self.token_entry.pack(pady=10)
        self.token_entry.focus_set()
        return self.token_entry

    def buttonbox(self):
        box = ttk.Frame(self)
        box.configure(bg='#2b2b2b')  
        ok_button = ttk.Button(box, text="OK", command=self.ok, style="Custom.TButton")
        ok_button.pack(side="left", padx=5, pady=5)
        cancel_button = ttk.Button(box, text="Cancel", command=self.cancel, style="Custom.TButton")
        cancel_button.pack(side="left", padx=5, pady=5)
        self.bind("<Return>", self.ok) 
        self.bind("<Escape>", self.cancel) 
        box.pack()

    def validate(self):
        token = self.token_entry.get()
        if token.strip().lower() == 'exit':
            messagebox.showinfo("Exiting", "Exiting program...")
            self.result = 'exit'
            self.cancel()
            return False
        elif not token.strip():
            messagebox.showwarning("Warning", "Please enter a token.")
            return False
        else:
            self.result = token
            return True

    def show_token_dialog(self):
        self.wait_window()
        return self.result

class GitHubSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GitHub Repository Search")

        self.token = ''
        self.search_query = ''

        self.style = ThemedStyle(self.root)
        self.style.set_theme("arc")

        self.label_token = ttk.Label(root, text="GitHub Token:")
        self.label_token.pack()

        self.token_entry = ttk.Entry(root, width=50, style="Custom.TEntry") 
        self.token_entry.pack(pady=(0, 10))

        self.label_query = ttk.Label(root, text="Search Query:")
        self.label_query.pack()

        self.query_entry = ttk.Entry(root, width=50, style="Custom.TEntry")
        # self.query_entry.insert(0, "times-model")
        self.query_entry.pack(pady=(0, 10))

        self.label_search_file = ttk.Label(root, text="Search File in Root (Default: 'SysSettings.xlsx'):")
        self.label_search_file.pack()

        self.search_file_entry = ttk.Entry(root, width=50, style="Custom.TEntry")
        self.search_file_entry.insert(0, "SysSettings.xlsx")
        self.search_file_entry.pack(pady=(0, 10))

        self.search_button = ttk.Button(root, text="Search", command=self.search, style="Custom.TButton")
        self.search_button.pack()

        self.results_text = tk.Text(root, width=100, height=30)
        self.results_text.pack()

    def search_github_repositories(self, query, token, per_page=100, max_results=100):
        url = 'https://api.github.com/search/repositories'
        headers = {'Authorization': f'token {token}'}
        results = []
        page = 1
        
        while len(results) < max_results:
            params = {
                'q': query,
                'per_page': per_page,
                'page': page
            }
            
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                items = response.json().get('items', [])
                if not items:
                    break
                results.extend(items)
            elif response.status_code == 403 and response.headers.get('X-RateLimit-Remaining') == '0':
                reset_time = int(response.headers.get('X-RateLimit-Reset'))
                wait_time = reset_time - int(time.time())
                messagebox.showinfo("Rate Limit Exceeded", f'Rate limit exceeded. Waiting for {wait_time} seconds...')
                dialog = CustomDialog(self.root, title="Enter GitHub Token")
                user_input = dialog.show_token_dialog()
                if user_input.lower() == 'exit':
                    return results[:max_results], 'exit'

                else:
                    token = user_input
                    headers = {'Authorization': f'token {token}'}
                    continue
            else:
                messagebox.showerror("Error", f'Failed to retrieve results: {response.status_code}')
                break
            
            page += 1
            if len(items) < per_page:
                break
        
        return results[:max_results], token

    def search_file_in_repo_root(self, owner, repo, filepath, token):
        url = f'https://api.github.com/repos/{owner}/{repo}/contents/{filepath}'
        headers = {'Authorization': f'token {token}'}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return True, token
        elif response.status_code == 404:
            return False, token
        elif response.status_code == 403 and response.headers.get('X-RateLimit-Remaining') == '0':
            reset_time = int(response.headers.get('X-RateLimit-Reset'))
            wait_time = reset_time - int(time.time())
            messagebox.showinfo("Rate Limit Exceeded", f'Rate limit exceeded. Waiting for {wait_time} seconds...')
            user_input = simpledialog.askstring("Input", "Enter 'exit' to exit the program or provide a new GitHub token:")
            if user_input.lower() == 'exit':
                return 'exit', 'exit'
            else:
                token = user_input
                return self.search_file_in_repo_root(owner, repo, filepath, token)
        else:
            messagebox.showerror("Error", f'Failed to search file in repo {owner}/{repo}: {response.status_code}')
            return False, token

    def search(self):
        self.token = self.token_entry.get()
        self.search_query = self.query_entry.get()
        search_file = 'SysSettings.xlsx'

        # Clear previous results
        self.results_text.delete('1.0', tk.END)

        repos, token = self.search_github_repositories(self.search_query, self.token)
        if token == 'exit':
            self.results_text.insert(tk.END, "Exiting program due to rate limit.\n")
            return

        found_repos = []

        if repos:
            for i, repo in enumerate(repos, 1):
                owner = repo['owner']['login']
                repo_name = repo['name']
                file_exists, token = self.search_file_in_repo_root(owner, repo_name, search_file, self.token)
                if token == 'exit':
                    self.results_text.insert(tk.END, "Exiting program due to rate limit.\n")
                    return
                if file_exists:
                    result = {
                        'name': repo_name,
                        'url': repo['html_url'],
                        'stars': repo['stargazers_count'],
                        'updated_at': repo['updated_at']
                    }
                    found_repos.append(result)
                    self.results_text.insert(tk.END, f"{i}. {repo_name} - {repo['html_url']} - Stars: {repo['stargazers_count']} - Last Updated: {repo['updated_at']}\n")

            if found_repos:
                json_result = json.dumps(found_repos, indent=4)
                self.results_text.insert(tk.END, f"\nJSON Result:\n{json_result}\n")

if __name__ == '__main__':
    root = tk.Tk()
    app = GitHubSearchApp(root)
    root.mainloop()
