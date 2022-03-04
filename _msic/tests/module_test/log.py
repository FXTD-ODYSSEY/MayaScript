import inspect



def get_logger():
    call_frame = inspect.currentframe().f_back
    print(call_frame)
    print(dir(call_frame))
    module_name  = call_frame.f_globals.get("__name__")
    print(module_name)

    
if __name__ == '__main__':
    get_logger()

