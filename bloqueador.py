import os
from tkinter import Tk, Label, Entry, Button, Listbox, Scrollbar, END, messagebox

hosts_pasta = r"C:\Windows\System32\drivers\etc\hosts"
redirec_ip = "127.0.0.1"

def bloqueador():
    link = entrada_site.get().strip()
    if not link:
        messagebox.showwarning("Erro", "Coloque uma URL válida.")
        return

    try:
        with open(hosts_pasta, "r+") as arquivo:
            conteudo = arquivo.readlines()
            for linha in conteudo:
                if link in linha:
                    messagebox.showinfo("Erro", f"O site {link} já está bloqueado.")
                    return

            arquivo.write(f"{redirec_ip} {link}\n")
        messagebox.showinfo("Sucesso", f"O site {link} foi bloqueado com sucesso.")
        entrada_site.delete(0, END)
        listar_sites()
    except PermissionError:
        messagebox.showerror("Erro", "Execute o programa como administrador para alterar o arquivo hosts.")

def listar_sites():
    try:
        with open(hosts_pasta, "r") as arquivo:
            linhas = arquivo.readlines()

            bloqueados = [linha.strip() for linha in linhas if linha.startswith(redirec_ip)]
            lista_sites.delete(0, END)
            for site in bloqueados:
                lista_sites.insert(END, site)
    except FileNotFoundError:
        messagebox.showerror("Erro", "Arquivo não encontrado.")

def desbloquear_sites():
    try:
        selecionado = lista_sites.get(lista_sites.curselection())  
        dominio = selecionado.split(" ")[1]  

        with open(hosts_pasta, "r") as arquivo:
            linhas = arquivo.readlines()

        with open(hosts_pasta, "w") as arquivo:
            for linha in linhas:
                if not linha.strip().startswith(f"{redirec_ip} {dominio}"):
                    arquivo.write(linha)

        messagebox.showinfo("Sucesso", f"O site {dominio} foi desbloqueado.")
        listar_sites()

    except IndexError:
        messagebox.showwarning("Erro", "Selecione um site para desbloquear.")  
    except PermissionError:
        messagebox.showerror("Erro", "Execute o programa como administrador!")  


# Configuração da interface gráfica
janela = Tk()
janela.title("Bloqueador de Sites")
janela.geometry("500x600")
janela.configure(bg="#ffe4e1")

Label(janela, text="Bloqueador de Sites", font=("Arial", 18, "bold"), bg="#ffe4e1", fg="#ff1493").pack(pady=10)

Label(janela, text="Digite a URL do site para bloquear:", font=("Arial", 12), bg="#ffe4e1", fg="#ff69b4").pack(pady=5)

entrada_site = Entry(janela, width=40, font=("Arial", 12), bg="#ffe4e1", fg="#800080", insertbackground="#ff1493")
entrada_site.pack(pady=5)

Button(janela, text="Bloquear Site", command=bloqueador, bg="#ff69b4", fg="white", font=("Arial", 12), activebackground="#ff1493", activeforeground="white").pack(pady=10)

Label(janela, text="Sites Bloqueados:", font=("Arial", 12), bg="#ffe4e1", fg="#ff69b4").pack(pady=5)

scrollbar = Scrollbar(janela)
lista_sites = Listbox(janela, width=50, height=15, font=("Arial", 12), bg="#fff0f5", fg="#800080", yscrollcommand=scrollbar.set, selectbackground="#ff1493", selectforeground="white")
lista_sites.pack(pady=5)
scrollbar.pack(side="right", fill="y")
scrollbar.config(command=lista_sites.yview)

Button(janela, text="Listar Sites", command=listar_sites, bg="#ff1493", fg="white", font=("Arial", 12), activebackground="#ff69b4", activeforeground="white").pack(pady=5)

Button(janela, text="Desbloquear Site", command=desbloquear_sites, bg="#db7093", fg="white", font=("Arial", 12), activebackground="#ff1493", activeforeground="white").pack(pady=5)

listar_sites()
janela.mainloop()
