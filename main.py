import myapp


def main():
    try:
        app = myapp.ChatterboxApp()
        app.MainLoop()
    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    __name__ = 'Main'
    main()
