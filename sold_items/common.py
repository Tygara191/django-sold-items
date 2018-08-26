def is_int(data):
    try:
        int(data)
        return True
    except ValueError:
        return False

def get_clean_params(request, key):
    result_list = []
    all_items = request.GET.get(key)
    if all_items:
        all_items = all_items.split(',')

        for index, item in enumerate(all_items):
            if is_int(all_items[index]):
                try:
                    result_list.append(int(all_items[index]))
                except ValueError:
                    pass

    if len(result_list) > 0:
        return result_list
    else:
        return False