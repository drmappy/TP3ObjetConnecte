import tkinter as tk

def main():
    root = tk.Tk()
    root.title("")
    
    
    def ajouter_intervalle():
        print("+0.1 seconde d'intervalle")

    def diminuer_intervalle():
        print("-0.1 seconde d'intervalle")

    def stop():
        print("button 3")

    btn_frame = tk.Frame(root)
    btn_frame.pack(side=tk.BOTTOM, fill=tk.X)

    btn_forward = tk.Button(btn_frame, text="+0.1 seconde d'intervalle", width=16, height=3, command=ajouter_intervalle, borderwidth=10, wraplength=75)
    btn_left = tk.Button(btn_frame, text="-0.1 seconde d'intervalle", width=16, height=3, command=diminuer_intervalle, borderwidth=10, wraplength=75)
    btn_clear = tk.Button(btn_frame, text="Arrêt propre de la surveillance", width=16, height=3, command=stop, borderwidth=10, wraplength=75)

    btn_forward.pack(side=tk.LEFT, padx=8, pady=6)
    btn_left.pack(side=tk.LEFT, padx=8, pady=6)
    btn_clear.pack(side=tk.LEFT, padx=8, pady=6)

    root.mainloop()

if __name__ == "__main__":
    main()