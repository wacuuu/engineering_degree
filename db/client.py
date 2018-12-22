from cli.client import *

if __name__ == "__main__":
    while True:
        opt = menu_options()
        if opt == 1:
            if on_create():
                print("Creation ok")
            else:
                print("Creation failed")
        elif opt == 2:
            on_update()
        elif opt == 3:
            if on_delete():
                print("Delete failed")
            else:
                print("Delete ok")
        elif opt == 4:
            on_read()
        else:
            print("No such option")
