from fastapi import HTTPException
from typing import List


code_err_prefix = "ae"

class CodeError:
    value_error = f"{code_err_prefix}000006"
    generic_error_code = f"{code_err_prefix}000000"
    already_user_code = f"{code_err_prefix}000001"
    not_found = f"{code_err_prefix}000004"
    unauthorized = f"{code_err_prefix}000005"
    
# Errors Genericos ----------------------------------------------------------------------------------------------
def error_internal_server(loc=[], msg="Value error", exceptions: List[Exception] = []) -> HTTPException:
    details = [e.detail[0] for e in exceptions if isinstance(e, HTTPException)]
    return HTTPException(status_code=503, detail=[
        {
            "loc": loc,
            "msg": msg,
            "type": CodeError.value_error
        },
        *details])
def generic_error(loc=[], exceptions: List[Exception] = [],status_code = 500,type_=CodeError.generic_error_code,msg='Generic Error') -> HTTPException:
    details = [e.detail[0] for e in exceptions if isinstance(e, HTTPException)]
    return HTTPException(status_code=status_code, detail=[
        {
            "loc": loc,
            "msg": msg,
            "type": type_
        },
        *details])

# Errors Rota User -----------------------------------------------------------------------------------------------
def error_user_already_registered(loc=[], exceptions: List[Exception] = []) -> HTTPException:
    details = [e.detail[0] for e in exceptions if isinstance(e, HTTPException)]
    return HTTPException(status_code=409, detail=[
        {
            "loc": loc,
            "msg": "User already registered",
            "type": CodeError.already_user_code
        },
        *details
    ])

def erro_not_found(loc=[], msg ="Not found", exceptions: List[Exception] = [],type_ = CodeError.not_found) -> HTTPException:
    details = [e.detail[0] for e in exceptions if isinstance(e, HTTPException)]
    return HTTPException(status_code=404, detail=[
        {
            "loc": loc,
            "msg": msg,
            "type": type_
        },
        *details
    ])

def erro_unauthorized(loc=[], msg ="Unauthorized", exceptions: List[Exception] = []) -> HTTPException:
    details = [e.detail[0] for e in exceptions if isinstance(e, HTTPException)]
    return HTTPException(status_code=401, detail=[
        {
            "loc": loc,
            "msg": msg,
            "type": CodeError.unauthorized
        },
        *details
    ])