import tkinter


def main():
    motor_interface_grafica: tkinter.Tk = tkinter.Tk()
    motor_interface_grafica.title("gerenciador broker")
    motor_interface_grafica.resizable(False, False)

    motor_interface_grafica.mainloop()


if __name__ == "__main__":
    main()
