from xml.etree import ElementTree


def read_gui_rpc_password(GUI_RPC_PASSWD_FILE='/etc/boinc-client/gui_rpc_auth.cfg'):
    """ Read password string from GUI_RPC_PASSWD_FILE file, trim the last CR
        (if any), and return it
    """
    try:
        with open(GUI_RPC_PASSWD_FILE, 'r') as f:
            buf = f.read()
            if buf.endswith('\n'):
                return buf[:-1]  # trim last CR
            else:
                return buf
    except IOError:
        # Permission denied or File not found.
        pass


def setattrs_from_xml(obj, xml, attrfuncdict={}):
    """ Helper to set values for attributes of a class instance by mapping
        matching tags from a XML file.
        attrfuncdict is a dict of functions to customize value data type of
        each attribute. It falls back to simple int/float/bool/str detection
        based on values defined in __init__(). This would not be needed if
        Boinc used standard RPC protocol, which includes data type in XML.
    """
    if not isinstance(xml, ElementTree.Element):
        xml = ElementTree.fromstring(xml)
    for e in list(xml):
        if hasattr(obj, e.tag):
            attr = getattr(obj, e.tag)
            attrfunc = attrfuncdict.get(e.tag, None)
            if attrfunc is None:
                if isinstance(attr, bool):
                    attrfunc = parse_bool
                elif isinstance(attr, int):
                    attrfunc = parse_int
                elif isinstance(attr, float):
                    attrfunc = parse_float
                elif isinstance(attr, str):
                    attrfunc = parse_str
                elif isinstance(attr, list):
                    attrfunc = parse_list
                else:
                    attrfunc = lambda x: x
            setattr(obj, e.tag, attrfunc(e))
        else:
            print("class missing attribute '%s': %r" % (e.tag, obj))
    return obj


def parse_bool(e):
    """ Helper to convert ElementTree.Element.text to boolean.
        Treat '<foo/>' (and '<foo>[[:blank:]]</foo>') as True
        Treat '0' and 'false' as False
    """
    if e.text is None:
        return True
    else:
        return bool(e.text) and not e.text.strip().lower() in ('0', 'false')


def parse_int(e):
    """ Helper to convert ElementTree.Element.text to integer.
        Treat '<foo/>' (and '<foo></foo>') as 0
    """
    # int(float()) allows casting to int a value expressed as float in XML
    return 0 if e.text is None else int(float(e.text.strip()))


def parse_float(e):
    """ Helper to convert ElementTree.Element.text to float. """
    return 0.0 if e.text is None else float(e.text.strip())


def parse_str(e):
    """ Helper to convert ElementTree.Element.text to string. """
    return "" if e.text is None else e.text.strip()


def parse_list(e):
    """ Helper to convert ElementTree.Element to list. For now, simply return
        the list of root element's children
    """
    return list(e)
