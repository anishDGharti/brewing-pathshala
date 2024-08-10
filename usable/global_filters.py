
from user_auths.models import User



def filter_user(request, filter_query):
    query_set = User.objects.all()
    if not filter_query:
        return query_set
    filter_map = {
        'students': {'is_student': True, 'is_deleted':False},
        'all': {},
        'active': {'is_active': True,'is_deleted':False},
        'inactive': {'is_active': False,'is_deleted':False},
        'staffs': {'is_staff': True,'is_deleted':False},
        'deleted_users': {'is_deleted': True},
        'normal_users': {'is_normal_user': True,'is_deleted':False},  # Replace with actual field name
        'superusers': {'is_superuser': True,'is_deleted':False},
    }

    

    if filter_query in filter_map:
        return query_set.filter(**filter_map[filter_query])

    return None