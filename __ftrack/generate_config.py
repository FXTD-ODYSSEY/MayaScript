# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-05-25 14:15:45"


import os
import sys

ext_path = [
    r"G:\RedApp\Plugins\Falcon\FalconBridge\Resources/Base/lib/python",
    r"G:\RedApp\Plugins\Falcon\FalconBridge\Resources\Thirdparty\Python37\Lib\site-packages",
    r"G:\RedApp\Plugins\Falcon\FalconBridge\Resources\Base\custom\python",
]
sys.path.extend(ext_path)
os.environ[
    "FALCON_THIRDPARTY_PATH"
] = r"D:/art_proj/UEProject/Plugins/Falcon/FalconBridge/Resources/Thirdparty"

import xlrd2
import sys
import uuid
from mftrack import MFtrack

DIR = os.path.dirname(__file__)
XLSX = os.path.join(DIR,'角色ID查询表.xlsx')
ID = "fd719e80-c1bd-11eb-8218-8661aee28a7b"

def main():

    mft = MFtrack.saml_login()
    book = xlrd2.open_workbook(XLSX)
    sheet = book.sheets()[0]
    folder = mft.query('Folder where id="{}"'.format(ID))[0]
    # status = mft.query('Status where name="{}"'.format('Not started')).one()
    
    id_list = []
    for i in range(1, 29):
        id_ = uuid.uuid1().hex
        character_name = sheet.row(i)[0].value
        character_id = sheet.row(i)[1].value
        character_card = str(sheet.row(i)[2].value).replace(".0", "")
        character_show = str(sheet.row(i)[3].value).replace(".0", "")
        character_monster = str(sheet.row(i)[4].value).replace(".0", "")
        character_lackey = str(sheet.row(i)[5].value).replace(".0", "")
        character_support = str(sheet.row(i)[6].value).replace(".0", "")
        character_battle = str(sheet.row(i)[7].value).replace(".0", "")
        character_story = str(sheet.row(i)[8].value).replace(".0", "")
        character_overhaul = sheet.row(i)[9].value
        character_en_name = sheet.row(i)[10].value
        
        if character_id in id_list or not character_id:
            continue
        id_list.append(character_id)
        
        task = mft.create(
            "Redconfigcharacter",
            {
                "name": character_id,
                "parent": folder,
                "id": id_,
            },
        )
        
        task["custom_attributes"] = {
            "character_name": character_name,
            "character_card": character_card,
            "character_show": character_show,
            "character_monster": character_monster,
            "character_lackey": character_lackey,
            "character_support": character_support,
            "character_battle": character_battle,
            "character_story": character_story,
            "character_overhaul": character_overhaul,
            "character_en_name": character_en_name,
            "character_type": ["主要角色"],
        }

    for i in range(1,25):
        id_ = uuid.uuid1().hex
        character_name = sheet.row(i)[12].value
        character_id = sheet.row(i)[13].value
        character_monster = str(sheet.row(i)[14].value).replace(".0", "")
        character_support = str(sheet.row(i)[15].value).replace(".0", "")
        character_battle = str(sheet.row(i)[16].value).replace(".0", "")
        character_story = str(sheet.row(i)[17].value).replace(".0", "")
        if character_id in id_list or not character_id:
            continue
        id_list.append(character_id)

        task = mft.create(
            "Redconfigcharacter",
            {
                "name": character_id,
                "parent": folder,
                "id": id_,
            },
        )
        
        task["custom_attributes"] = {
            "character_name": character_name,
            "character_monster": character_monster,
            "character_support": character_support,
            "character_battle": character_battle,
            "character_story": character_story,
            "character_type": ["次要角色"],
        }

    for i in range(1,85):
        id_ = uuid.uuid1().hex
        character_name = sheet.row(i)[20].value
        character_id = sheet.row(i)[21].value
        if character_id in id_list or not character_id:
            continue
        id_list.append(character_id)

        task = mft.create(
            "Redconfigcharacter",
            {
                "name": character_id,
                "parent": folder,
                "id": id_,
            },
        )
        
        task["custom_attributes"] = {
            "character_name": character_name,
            "character_type": ["杂鱼角色"],
        }
        
    mft.commit()


if __name__ == "__main__":
    main()

