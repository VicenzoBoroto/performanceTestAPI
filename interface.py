import tkinter as tk
import subprocess

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.test_type_var = tk.StringVar()
        self.test_type_var.set("API")

        self.test_type_label = tk.Label(self, text="Selecione o tipo de teste:")
        self.test_type_label.pack()

        self.api_rb = tk.Radiobutton(self, text="API", variable=self.test_type_var, value="API", command=self.show_api_options)
        self.api_rb.pack()

        self.db_rb = tk.Radiobutton(self, text="Banco de Dados", variable=self.test_type_var, value="DB", command=self.show_db_options)
        self.db_rb.pack()

        self.url_label = tk.Label(self, text="URL:")
        self.url_label.pack()
        self.url_entry = tk.Entry(self)
        self.url_entry.pack()

        self.req_label = tk.Label(self, text="Quantidade de Requisições:")
        self.req_label.pack()
        self.req_entry = tk.Entry(self)
        self.req_entry.pack()

        self.db_url_label = tk.Label(self, text="URL do Banco de Dados:")
        self.db_url_label.pack()
        self.db_url_entry = tk.Entry(self)

        self.show_api_options()

        self.test_button = tk.Button(self, text="Realizar Teste", command=self.run_test)
        self.test_button.pack()

    def show_api_options(self):
        self.req_label.pack_forget()
        self.req_entry.pack_forget()
        self.db_url_label.pack_forget()
        self.db_url_entry.pack_forget()
        self.req_label.pack()
        self.req_entry.pack()

    def show_db_options(self):
        self.req_label.pack_forget()
        self.req_entry.pack_forget()
        self.db_url_label.pack_forget()
        self.db_url_entry.pack_forget()
        self.db_url_label.pack()
        self.db_url_entry.pack()

    def run_test(self):
        if self.test_type_var.get() == "API":
            url = self.url_entry.get()
            reqs = self.req_entry.get()
            subprocess.call(["python", "requestAPI.py", url, reqs])
        elif self.test_type_var.get() == "DB":
            url = self.db_url_entry.get()
            subprocess.call(["python", "requestSQL.py", url])

root = tk.Tk()
app = Application(master=root)
app.mainloop()
