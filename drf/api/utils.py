


from api.models import DEPARTMENT_CHOISE, ROLE_CHOISE


def get_department_name_by_id(id: int):
    return dict(DEPARTMENT_CHOISE)[id]

def get_department_id_by_name(name: int):
    department_choise = { d_name: d_id for d_id, d_name in dict(DEPARTMENT_CHOISE).items() }
    return department_choise.get(name, -1)

def get_role_name_by_id(id: int):
    return dict(ROLE_CHOISE)[id]

def get_role_id_by_name(name: str):
    role_choise = { r_name: r_id for r_id, r_name in dict(ROLE_CHOISE).items() }
    return role_choise.get(name, -1)