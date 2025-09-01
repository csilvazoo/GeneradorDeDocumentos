import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.scrolledtext import ScrolledText
import threading
import os
import queue
from app.logic import run_script
from app.update_requerimientos import update_requerimientos
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service as EdgeService
import sys

def get_app_version():
    try:
        if hasattr(sys, '_MEIPASS'):
            version_path = os.path.join(sys._MEIPASS, 'VERSION')
        else:
            version_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'VERSION')
        version = open(version_path, 'r').read().strip()
        import re
        m = re.match(r"(\d{4})(\d{2})(\d{2})\.(\d+)", version)
        if m:
            return f"{m.group(1)[2:]}.{m.group(2)}.{m.group(3)}.{m.group(4)}"
        return version
    except Exception:
        return "Sin versión"

def main():
    log_queue = queue.Queue()
    root = tk.Tk()
    root.title(f"Generador de Documentos Funcionales")
    root.geometry("600x235")
    frm = ttk.Frame(root, padding=20)
    frm.pack(fill=tk.BOTH, expand=True)
    ttk.Label(frm, text="Funcionalidad:").grid(row=0, column=0, sticky=tk.W)
    funcionalidad_var = tk.StringVar()
    txt_funcionalidad = ttk.Entry(frm, textvariable=funcionalidad_var, width=20)
    txt_funcionalidad.grid(row=0, column=1, sticky=tk.W)
    ver_explorador_var = tk.BooleanVar(value=True)
    chk = ttk.Checkbutton(frm, text="Ver explorador", variable=ver_explorador_var)
    chk.grid(row=1, column=0, columnspan=2, sticky=tk.W)
    user_documents = os.path.join(os.path.expanduser('~'), 'Documents')
    ruta_var = tk.StringVar(value=os.path.join(user_documents, "Funcionalidad.docx"))
    ttk.Label(frm, text="Guardar como:").grid(row=2, column=0, sticky=tk.W)
    entry_ruta = ttk.Entry(frm, textvariable=ruta_var, width=65)
    entry_ruta.grid(row=2, column=1, sticky=tk.W, columnspan=1)
    def seleccionar_ruta():
        ruta = filedialog.asksaveasfilename(
            defaultextension=".docx",
            filetypes=[("Documentos Word", "*.docx")],
            initialdir=user_documents,
            initialfile="Funcionalidad.docx",
            title="Guardar documento como"
        )
        if ruta:
            ruta_var.set(ruta)
    btn_examinar = ttk.Button(frm, text="Examinar...", command=seleccionar_ruta)
    btn_examinar.grid(row=2, column=1, sticky=tk.E, padx=(0,0))
    # Centrar y distribuir los botones: Generar a la izquierda, Actualizar al centro, Abrir a la derecha
    btns_frame = ttk.Frame(frm)
    btns_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky="ew")
    btns_frame.columnconfigure(0, weight=1)
    btns_frame.columnconfigure(1, weight=1)
    btns_frame.columnconfigure(2, weight=1)
    btn = ttk.Button(btns_frame, text="Generar Documento")
    btn.grid(row=0, column=0, sticky="w")
    btn_update = ttk.Button(btns_frame, text="Actualizar Documento", command=lambda: on_update())
    btn_update.grid(row=0, column=1)
    open_btn = ttk.Button(btns_frame, text="Abrir Documento", state="disabled")
    open_btn.grid(row=0, column=2, sticky="e")

    def abrir_doc_custom(ruta):
        if os.path.exists(ruta):
            try:
                os.startfile(ruta)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el documento:\n{e}")
        else:
            messagebox.showerror("Error", "El archivo no existe en la ruta seleccionada.")
    open_btn.config(command=lambda: abrir_doc_custom(ruta_var.get()))    
    # Crear la barra de progreso pero ocultarla inicialmente
    progress = ttk.Progressbar(frm, mode="indeterminate")
    progress.grid(row=4, column=0, columnspan=2, sticky="ew", pady=5)
    progress.grid_remove()  # Oculta la barra al iniciar
    progress['value'] = 0
    progress.update_idletasks()
    status_label = ttk.Label(frm, text="", foreground="blue")
    status_label.grid(row=5, column=0, columnspan=2, pady=(0,5))
    success_label = ttk.Label(frm, text="", foreground="green")
    success_label.grid(row=8, column=0, columnspan=2, pady=(5,0))
    # Eliminar etiqueta duplicada y dejar solo una
    log_label = ttk.Label(frm, text="Detalle de ejecución:")
    log_label.grid(row=5, column=0, columnspan=2, sticky=tk.W)
    txt_log = ScrolledText(frm, height=15, width=100, state="disabled", bg="#ffffff", bd=0, highlightthickness=0)
    txt_log.grid(row=7, column=0, columnspan=2, sticky="nsew", pady=(0,10))
    txt_log.grid_remove()
    frm.rowconfigure(7, weight=1)
    frm.columnconfigure(1, weight=1)
    def toggle_log():
        if txt_log.winfo_viewable():
            txt_log.grid_remove()
            ver_detalle_btn.config(text="Ver detalle")
            root.geometry("600x245")
        else:
            txt_log.grid(row=7, column=0, columnspan=2, sticky="nsew", pady=(0,10))
            ver_detalle_btn.config(text="Ocultar detalle")
            root.geometry("600x400")
    ver_detalle_btn = ttk.Button(frm, text="Ver detalle", command=toggle_log)
    ver_detalle_btn.grid(row=6, column=0, columnspan=2, pady=(0,10))
    def update_log():
        while not log_queue.empty():
            msg = log_queue.get_nowait()
            txt_log.configure(state="normal")
            txt_log.insert(tk.END, msg + "\n")
            txt_log.see(tk.END)
            txt_log.configure(state="disabled")
        root.after(200, update_log)
    update_log()
    def on_run():
        num = funcionalidad_var.get().strip()
        if not num.isdigit():
            messagebox.showerror("Error", "Ingrese un número de funcionalidad válido.")
            return
        btn.config(state="disabled")
        progress['value'] = 0
        progress.grid()  # Mostrar la barra al iniciar acción
        progress.start()
        txt_log.configure(state="normal")
        txt_log.delete(1.0, tk.END)
        txt_log.configure(state="disabled")
        success_label.config(text="", foreground="green")
        open_btn.config(state="disabled")
        status_label.config(text="Generando Documento", foreground="blue")
        root.geometry("600x245")
        ruta_docx = ruta_var.get()
        def task():
            run_script(num, ver_explorador_var.get(), log_queue, ruta_docx)
            progress.stop()
            progress['value'] = 0
            progress.grid_remove()  # Ocultar la barra al terminar
            btn.config(state="normal")
            log_content = ""
            try:
                with log_queue.mutex:
                    log_content = "\n".join(list(log_queue.queue))
            except Exception:
                pass
            if not log_content:
                log_content = txt_log.get("1.0", tk.END)
            status_label.config(text="")
            if os.path.exists(ruta_docx) and "No existe funcionalidad o no tiene requerimientos asociados." not in log_content:
                status_label.config(text="Documento generado exitosamente.", foreground="green")
                open_btn.config(state="normal")
                # Abrir el documento generado automáticamente
                abrir_doc_custom(ruta_docx)
            else:
                status_label.config(text="Documento NO generado.", foreground="red")
                open_btn.config(state="disabled")
                root.after(5000, lambda: status_label.config(text=""))
        threading.Thread(target=task, daemon=True).start()
    btn.config(command=on_run)
    root.geometry("600x235")

    def on_update():
        num = funcionalidad_var.get().strip()
        if not num.isdigit():
            messagebox.showerror("Error", "Ingrese un número de funcionalidad válido.")
            return
        ruta_docx = filedialog.askopenfilename(
            defaultextension=".docx",
            filetypes=[("Documentos Word", "*.docx")],
            initialdir=user_documents,
            title="Seleccionar documento a actualizar"
        )
        if not ruta_docx:
            return
        resp = messagebox.askyesno("Confirmar actualización", f"¿Está seguro que desea actualizar el documento?\n\n{ruta_docx}")
        if not resp:
            return
        btn_update.config(state="disabled")
        progress['value'] = 0
        progress.grid()  # Mostrar la barra al iniciar acción
        progress.start()
        txt_log.configure(state="normal")
        txt_log.delete(1.0, tk.END)
        txt_log.configure(state="disabled")
        success_label.config(text="", foreground="green")
        open_btn.config(state="disabled")
        status_label.config(text="Actualizando Documento", foreground="blue")
        root.geometry("600x245")
        def task():
            options = Options()
            options.add_argument("--start-maximized")
            if not ver_explorador_var.get():
                options.add_argument("--headless")
            if getattr(sys, 'frozen', False):
                driver_path = os.path.join(sys._MEIPASS, "msedgedriver.exe")
            else:
                driver_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "msedgedriver.exe")
            service = EdgeService(driver_path)
            driver = webdriver.Edge(service=service, options=options)
            try:
                update_requerimientos(num, ruta_docx, driver, log_queue)
            except Exception as e:
                log_queue.put(f"ERROR: {e}")
            finally:
                driver.quit()
                progress.stop()
                progress['value'] = 0
                progress.grid_remove()  # Ocultar la barra al terminar
                btn_update.config(state="normal")
                log_content = ""
                try:
                    with log_queue.mutex:
                        log_content = "\n".join(list(log_queue.queue))
                except Exception:
                    pass
                if not log_content:
                    log_content = txt_log.get("1.0", tk.END)
                status_label.config(text="")
                if os.path.exists(ruta_docx) and "No hay nuevos requerimientos para agregar" not in log_content:
                    status_label.config(text="Documento actualizado exitosamente.", foreground="green")
                    open_btn.config(state="normal")
                    # Abrir el documento actualizado automáticamente
                    abrir_doc_custom(ruta_docx)
                else:
                    status_label.config(text="Documento NO actualizado.", foreground="red")
                    open_btn.config(state="disabled")
                    root.after(5000, lambda: status_label.config(text=""))
        threading.Thread(target=task, daemon=True).start()

    # Cambiar el icono de la ventana principal
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'resources', 'icons', 'Zoo.ico')
    try:
        root.iconbitmap(icon_path)
    except Exception:
        pass  # Si falla, no rompe la app
    # Label de versión más alto, justo después de ver detalle
    version_label = ttk.Label(frm, text=f"Versión: {get_app_version()}", foreground="gray")
    version_label.grid(row=8, column=0, columnspan=2, sticky=tk.E, pady=(2, 10))

    root.mainloop()
