def except_handler(message):
    def decorate(f):
        def applicator(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except:
                print('Возникла ошибка ' + message)
                return

        return applicator

    return decorate
