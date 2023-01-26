def get_ajax_result_dict(result='false', msg='This is default message!', additional_data=None):
    """
        We use this function in all JSONResponse functions to unify responses
        result (str): Response flag, true | false
        msg (str): Response message
        additional_data (dict): Extra data for result dict
    """
    result = {'result': result, 'msg': msg}
    if additional_data is not None:
        result.update(additional_data)
    return result


def is_ajax(request):
    """
        Check the request is ajax
    """
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
