import tkinter as tk
from tkinter import messagebox, scrolledtext

from process import Process
import schaduler


class SRTFGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SRTF Scheduler")
        self.geometry("500x600")

        # Number of processes input
        tk.Label(self, text="Number of processes:").pack(pady=5)
        self.np_var = tk.StringVar()
        tk.Entry(self, textvariable=self.np_var).pack()
        tk.Button(self, text="Create Inputs", command=self.create_process_inputs).pack(pady=10)

        # Frame to hold dynamic AT/BT entries
        self.inputs_frame = tk.Frame(self)
        self.inputs_frame.pack(pady=5, fill="x")

        # Run button & output area
        tk.Button(self, text="Run SRTF", command=self.run_srtf).pack(pady=10)
        self.output = scrolledtext.ScrolledText(self, height=15)
        self.output.pack(fill="both", padx=10, pady=5)

        # keep lists of entry widgets
        self.arrival_entries = []
        self.burst_entries = []

    def create_process_inputs(self):
        # clear old entries
        for widget in self.inputs_frame.winfo_children():
            widget.destroy()
        self.arrival_entries.clear()
        self.burst_entries.clear()

        try:
            n = int(self.np_var.get())
            if n <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a positive integer for number of processes.")
            return

        # header
        header = tk.Frame(self.inputs_frame)
        tk.Label(header, text="Process").grid(row=0, column=0, padx=5)
        tk.Label(header, text="Arrival Time").grid(row=0, column=1, padx=5)
        tk.Label(header, text="Burst Time").grid(row=0, column=2, padx=5)
        header.pack()

        # one row per process
        for i in range(1, n + 1):
            #row = tk.Frame(self.inputs_frame)
            tk.Label(header, text=f"P{i}").grid(row=i, column=0)
            at = tk.Entry(header, width=7)
            bt = tk.Entry(header, width=7)
            at.grid(row=i, column=1, padx=5)
            bt.grid(row=i, column=2, padx=5)
            header.pack(pady=2)
            self.arrival_entries.append(at)
            self.burst_entries.append(bt)

    def run_srtf(self):
        # build Process list from entries
        procs = []
        for i, (at_e, bt_e) in enumerate(zip(self.arrival_entries, self.burst_entries), start=1):
            try:
                at = schaduler.validate_int(at_e.get())
                bt = schaduler.validate_int(bt_e.get())
                if at is None or bt is None:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Error", f"Invalid input for P{i}.")
                return
            procs.append(Process(f"P{i}", at, bt))

        # run the algorithm
        gant = schaduler.srtf(procs)
        filtered = schaduler.filter_gant(gant)
        avgs = schaduler.avgs(procs)

        # display results
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, "Gantt Chart:\n")
        for pid, st, en in filtered:
            self.output.insert(tk.END, f"  {pid}: {st} → {en}\n")
        self.output.insert(tk.END, "\nPer-Process Stats:\n")
        for p in procs:
            self.output.insert(tk.END,
                               f"  {p.id} — WT: {p.waiting_time()}, TT: {p.turnaround_time()}, RT: {p.response_time()}\n"
                               )
        self.output.insert(tk.END,
                           "\nAverages:\n" +
                           f"  Waiting Time: {avgs[0]:.2f}\n" +
                           f"  Turnaround Time: {avgs[1]:.2f}\n" +
                           f"  Response Time: {avgs[2]:.2f}\n"
                           )


if __name__ == "__main__":
    app = SRTFGui()
    app.mainloop()