# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = "timmyliang"
__email__ = "820472580@qq.com"
__date__ = "2021-08-19 10:34:39"

import os
import imp
import json
import unreal
from collections import OrderedDict

# NOTE 获取 init_unreal.py 脚本的路径
DIR = os.path.dirname(__file__)
CONTENT = os.path.dirname(DIR)
CONFIG = os.path.join(CONTENT, "_config")
# NOTE 利用 imp 加载脚本 (等于与 import 指定路径的脚本)
menu_py = os.path.join(CONFIG, "menu.py")
MENU_MODULE = imp.load_source("__menu__", menu_py) if os.path.exists(menu_py) else None

menus = unreal.ToolMenus.get()
FORMAT_ARGS = {"Content": CONTENT}

# NOTE 字符串映射到 Unreal 对象
COMMAND_TYPE = {
    "COMMAND": unreal.ToolMenuStringCommandType.COMMAND,
    "PYTHON": unreal.ToolMenuStringCommandType.PYTHON,
    "CUSTOM": unreal.ToolMenuStringCommandType.CUSTOM,
}

INSERT_TYPE = {
    "AFTER": unreal.ToolMenuInsertType.AFTER,
    "BEFORE": unreal.ToolMenuInsertType.BEFORE,
    "DEFAULT": unreal.ToolMenuInsertType.DEFAULT,
    "FIRST": unreal.ToolMenuInsertType.FIRST,
}

MENU_TYPE = {
    "BUTTON_ROW": unreal.MultiBoxType.BUTTON_ROW,
    "MENU": unreal.MultiBoxType.MENU,
    "MENU_BAR": unreal.MultiBoxType.MENU_BAR,
    "TOOL_BAR": unreal.MultiBoxType.TOOL_BAR,
    "UNIFORM_TOOL_BAR": unreal.MultiBoxType.UNIFORM_TOOL_BAR,
    "VERTICAL_TOOL_BAR": unreal.MultiBoxType.VERTICAL_TOOL_BAR,
}

ENTRY_TYPE = {
    "BUTTON_ROW": unreal.MultiBlockType.BUTTON_ROW,
    "EDITABLE_TEXT": unreal.MultiBlockType.EDITABLE_TEXT,
    "HEADING": unreal.MultiBlockType.HEADING,
    "MENU_ENTRY": unreal.MultiBlockType.MENU_ENTRY,
    "NONE": unreal.MultiBlockType.NONE,
    "TOOL_BAR_BUTTON": unreal.MultiBlockType.TOOL_BAR_BUTTON,
    "TOOL_BAR_COMBO_BUTTON": unreal.MultiBlockType.TOOL_BAR_COMBO_BUTTON,
    "WIDGET": unreal.MultiBlockType.WIDGET,
}

ACTION_TYPE = {
    "BUTTON": unreal.UserInterfaceActionType.BUTTON,
    "CHECK": unreal.UserInterfaceActionType.CHECK,
    "COLLAPSED_BUTTON": unreal.UserInterfaceActionType.COLLAPSED_BUTTON,
    "NONE": unreal.UserInterfaceActionType.NONE,
    "RADIO_BUTTON": unreal.UserInterfaceActionType.RADIO_BUTTON,
    "TOGGLE_BUTTON": unreal.UserInterfaceActionType.TOGGLE_BUTTON,
}

def handle_menu(data):
    """
    handle_menu 递归生成菜单
    """
    menu = data.get("menu")
    if not menu:
        return
    
    # NOTE 解析 section 配置
    for section, config in data.get("section", {}).items():
        # NOTE 兼容简单的字符串命名的配置
        config = config if isinstance(config, dict) else {"label": config}
        config.setdefault("label", "untitle")
        # NOTE 如果存在 insert_type 需要将字符串转换大写 (这样 json 配置就不用区分大小写了)
        insert = INSERT_TYPE.get(config.get("insert_type", "").upper())
        insert and config.update({"insert_type":insert})
        insert_name = config.get("insert_name")
        config["insert_name"] = insert_name if insert_name else "None"
        # NOTE 添加 section 
        menu.add_section(section, **config)

    # NOTE 解析 property 配置
    for prop, value in data.get("property", {}).items():
        # NOTE owner 不知道作用是啥
        if prop == "menu_owner" or value == "":
            continue
        elif prop == "menu_type":
            value = MENU_TYPE.get(value.upper())
        menu.set_editor_property(prop, value)

    # NOTE 解析 entry 配置
    for entry_name, config in data.get("entry", {}).items():
        label = config.get("label", "untitle")
        prop = config.get("property", {})
        for k in prop.copy():
            v = prop.pop(k)
            if v and k in ["name", "tutorial_highlight_name"]:
                prop[k] = v
            # NOTE 将字符串选项映射到 Unreal Python 的类型
            if k == "insert_position":
                position = INSERT_TYPE.get(v.get("position", "").upper())
                v["position"] = (
                    position if position else unreal.ToolMenuInsertType.FIRST
                )
                v["name"] = v.get("name", "")
                prop[k] = unreal.ToolMenuInsert(**v)
            elif k == "type":
                typ = ENTRY_TYPE.get(str(v).upper())
                prop[k] = typ if typ else unreal.MultiBlockType.MENU_ENTRY
            elif k == "user_interface_action_type":
                typ = ACTION_TYPE.get(str(v).upper())
                typ and prop.update({k: typ})
            elif k == "script_object":
                # NOTE 获取 MENU_MODULE 有没有相关的类
                script_class = getattr(MENU_MODULE, v, None)
                if script_class and issubclass(
                    script_class, unreal.ToolMenuEntryScript
                ):
                    script_object = script_class()
                    context = unreal.ToolMenuContext()
                    # NOTE 检查类是否配置 get_label 没有设置则采用 json 配置的名称
                    script_label = str(script_object.get_label(context))
                    if not script_label:

                        # NOTE 生成一个动态类来设置名称
                        @unreal.uclass()
                        class RuntimeScriptClass(script_class):
                            label = unreal.uproperty(str)

                            @unreal.ufunction(override=True)
                            def get_label(self, context):
                                return self.label

                        script_object = RuntimeScriptClass()
                        script_object.label = label
                    prop[k] = script_object

        prop.setdefault("name", entry_name)
        prop.setdefault("type", unreal.MultiBlockType.MENU_ENTRY)
        entry = unreal.ToolMenuEntry(**prop)
        entry.set_label(label)
        
        typ = COMMAND_TYPE.get(config.get("type", "").upper(), 0)
        # NOTE 命令支持特殊字符替换 例如 {Content}
        command = config.get("command", "").format(**FORMAT_ARGS)
        entry.set_string_command(typ, "", string=command)
        menu.add_menu_entry(config.get("section", ""), entry)

    # NOTE 递归解析 sub_menu
    for entry_name, config in data.get("sub_menu", {}).items():
        init = config.get("init", {})
        owner = menu.get_name()
        section_name = init.get("section", "")
        name = init.get("name", entry_name)
        label = init.get("label", "")
        tooltip = init.get("tooltip", "")
        sub_menu = menu.add_sub_menu(owner, section_name, name, label, tooltip)
        config.setdefault("menu", sub_menu)
        handle_menu(config)


def read_json(json_path):
    import codecs

    try:
        with codecs.open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f, object_pairs_hook=OrderedDict)
    except:
        import traceback

        traceback.print_exc()
        data = {}
    return data


def read_config_json(config):
    return read_json(os.path.join(CONFIG, "%s.json" % config))


def create_menu():
    # NOTE Read menu json settings
    menu_json = read_config_json("menu")
    fail_menus = {}
    for tool_menu, config in menu_json.items():
        # NOTE 如果菜单不存在添加到失败列表里面
        menu = menus.find_menu(tool_menu)
        if not menu:
            fail_menus.update({tool_menu: config})
            continue
        # NOTE 设置 menu 方便在 handle_menu 里面获取当前处理的菜单
        config.setdefault("menu", menu)
        handle_menu(config)

    menus.refresh_all_widgets()

    return fail_menus


fail_menus = create_menu()