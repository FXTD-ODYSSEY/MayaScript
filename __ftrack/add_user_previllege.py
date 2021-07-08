# -*- coding: utf-8 -*-
"""
fail to run
"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-06-01 09:49:55"


import os
import sys
import json
import uuid

ext_path = [
    r"G:\RedApp\Plugins\Falcon\FalconBridge\Resources/Base/lib/python",
    r"G:\RedApp\Plugins\Falcon\FalconBridge\Resources\Thirdparty\Python37\Lib\site-packages",
    r"G:\RedApp\Plugins\Falcon\FalconBridge\Resources\Base\custom\python",
]
sys.path.extend(ext_path)
os.environ[
    "FALCON_THIRDPARTY_PATH"
] = r"D:/art_proj/UEProject/Plugins/Falcon/FalconBridge/Resources/Thirdparty"

from mftrack import MFtrack

ID = "f1bf7fe0-b6bd-11eb-ba40-fe58234e3653"


def print_member(member):
    print(member)
    print(dir(member))
    data = {}
    for k in member.keys():
        data[k] = str(type(member[k]))
    print(json.dumps(data, indent=4))


def main():

    mft = MFtrack.saml_login()
    # Retrieve a project
    project = mft.query('Project where id="{}"'.format(ID)).first()

    # Set to hold all users part of the project team
    project_team = set()

    # Add all allocated groups and users
    for allocation in project["allocations"]:

        # Resource may be either a group or a user
        resource = allocation["resource"]

        # If the resource is a group, add its members
        if isinstance(resource, mft.types["Group"]):

            for membership in resource["memberships"]:
                user = membership["user"]
                project_team.add(user)

        # The resource is a user, add it.
        else:
            user = resource
            project_team.add(user)

    # projects = mft.query('Project where id="{}"'.format(ID)).all()[:]
    # print(projects)
    user_role = mft.query('SecurityRole where name is "User"').one()
    for i,user in enumerate(project_team):
        name = user["username"]
        if i > 1:
            break
        print(name)
        from mftrack import UserSecurityRole
        role = mft.create(
                "UserSecurityRole",
                {
                    "projects": [project],
                    "user": user,
                    "security_role": user_role,
                },
            )
        # user["user_security_roles"] = [role]
        # role["is_all_open_projects"] = True
        
        # role_projects = role["user_security_role_projects"]
        # role_projects.append(project)
        
        # if not len(role_projects):
        #     id_ = uuid.uuid1().hex
        #     print(user["username"])
            

    mft.commit()

    # print(project_team)

    # users = mft.query("User")
    # user = users.first()
    # for key in user.keys():
    #     if key == "memberships":
    #         memberships = user[key]
    #         print(memberships)
    #         for k in memberships:
    #             print(k)

    # print(memberships)
    # print(dir(memberships))

    # print("keys",user.keys())
    # print("values",user.values())

    # folder = mft.query('Folder where id="{}"'.format(ID))[0]
    # status = mft.query('Status where name="{}"'.format('Not started')).one()


if __name__ == "__main__":
    main()
