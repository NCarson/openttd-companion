
def tr(s): return s
def _set(value, doc):
    return property(lambda x:value, doc=tr(doc))


class Config:
    
    openttd_cmd = _set("~/public/openttd-13.0/build/openttd -D", #FIXME
        "Openttd command|The path of the execute with startup options.")

    udp_host = _set("127.0.0.1", 
        "UDP host|Host name for *this* (not the openttd service) UDP service.")

    udp_port = _set(3978,
        "UDP port|Port number for *this* (not the openttd service) UDP service.")

    udp_buffer_size = _set(1024, 
        "UDP packet size|The maximum per packet of *this* "\
        + "(not the oppentd service) UDP service.")

    udp_allow_stdin = _set(True,
        "terminal keyboard access|Allow the GUI to send commands to the openttd server.")

    script_ids = _set("",
        "script ids|Which game script ids (comma delineated list) to watch")

#print(Config.__dict__['udp_allow_stdin'].__doc__)
#config = Config()
#print(config.udp_allow_stdin)


