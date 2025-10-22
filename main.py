from customtkinter import CTk
from Login_Module.loginGUI import LoginGUI

if __name__ == "__main__":
    root = CTk()
    app = LoginGUI(root)
    root.mainloop()