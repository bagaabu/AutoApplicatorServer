from app.utils.const import user_struct


def rerange_search2db(stage_list, key_list):
    seach_dict = {}
    for stage in stage_list:
        if stage == 'all':
            seach_dict['personal-info'] = 'all'
            seach_dict['score'] = 'all'
            seach_dict['exp'] = 'all'
            seach_dict['school'] = 'all'
        else:
            seach_dict[stage] = 'all'
    for key in key_list:
        if user_struct[key] not in seach_dict:
            seach_dict[user_struct[key]] = {}
        seach_dict[user_struct[key]][key] = 1
    return seach_dict


def rerange_up2db(info_dict):
    upload_list = {}
    if 'userID' not in info_dict:
        raise Exception("userID is needed!")
    userID = info_dict.pop('userID')
    for item in info_dict.items():
        stage = user_struct[item]
        if stage not in upload_list:
            upload_list[stage] = {'userID':userID}
        upload_list[stage][item] = info_dict[item]
    return upload_list

