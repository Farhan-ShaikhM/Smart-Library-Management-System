from customtkinter import CTk
from Login_Module.loginGUI import LoginGUI

if __name__ == "__main__":
    root = CTk()
    app = LoginGUI(root)
    root.mainloop()

#DO NOT TOUCH "app = " in any file even if it doesn't have any usage, it is a runtime usage