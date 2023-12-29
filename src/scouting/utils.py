def is_user_in_group(user_groups, group_name):
    return any(group.name == group_name for group in user_groups)
