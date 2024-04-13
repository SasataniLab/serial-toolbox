import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from .interface_core import SerialInterface
from .connect import PortManager

class Application(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interface = SerialInterface(PortManager.select_port(), terminal=False)
        
        ctk.set_appearance_mode("Dark") # "System"(default) or "Light" or "dark"
        # create main frames
        self.left_frame = ctk.CTkFrame(self)
        self.right_frame = ctk.CTkFrame(self)

        self.left_frame.grid(row=0, column=0, sticky='ns')
        self.right_frame.grid(row=0, column=1, sticky='nsew')

        # in left frame, put the entry field and send button at the top
        self.entry_text = ctk.StringVar()
        self.data_entry = ctk.CTkEntry(self.left_frame, textvariable=self.entry_text)
        self.data_entry.pack(side=ctk.TOP, fill=ctk.X)
        self.data_entry.bind('<Return>', lambda event: self.send_command())

        self.send_button = ctk.CTkButton(self.left_frame, text="Send", command=self.send_command)
        self.send_button.pack(side=ctk.TOP, fill=ctk.X)
        # below that, put the data_text widget
        self.data_text = ctk.CTkTextbox(self.left_frame, height=10, width=50)
        self.data_text.pack(side=ctk.TOP, fill=ctk.BOTH, expand=True)

        # in right frame, put the canvas for the plot
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.plot = self.figure.add_subplot(1, 1, 1)
        
        self.canvas = FigureCanvasTkAgg(self.figure, self.right_frame)
        self.canvas.get_tk_widget().pack(fill=ctk.BOTH, expand=True)
        
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.right_frame.rowconfigure(0, weight=1)
        self.right_frame.columnconfigure(0, weight=1)

        self.update_plot()
        
    def send_command(self):
        command = self.entry_text.get()
        self.data_text.insert("end", "Sent: " + command + "\n")
        self.interface.write_to_port(command)
        self.entry_text.set("")  # Clear the content in the entry text field


    def update_plot(self):
        if len(self.interface.data_list) > 0:
            self.plot.clear()
            self.plot.plot(self.interface.data_list)
            self.canvas.draw()
            # last_received = self.interface.data_list[-1]
            # self.data_text.insert("end", "Received: " + str(last_received) + "\n")

        self.after(100, self.update_plot)
        

def serial_monitor_gui():
    app = Application()
    app.mainloop()
