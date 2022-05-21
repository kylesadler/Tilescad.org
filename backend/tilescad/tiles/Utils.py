def domCom(dom):
    if dom[-1] == '*':
        return dom[:-1]
    return dom + '*'