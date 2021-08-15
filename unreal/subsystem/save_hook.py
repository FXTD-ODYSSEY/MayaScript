# -*- coding: utf-8 -*-
"""

"""

from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

__author__ = 'timmyliang'
__email__ = '820472580@qq.com'
__date__ = '2021-07-22 19:08:16'

import unreal



@unreal.uclass()
class OnAssetSaveValidator(unreal.EditorValidatorBase):

    @unreal.ufunction(override=True)
    def can_validate_asset(self,asset):
        print("can_validate_asset",asset)
        return super(OnAssetSaveValidator,self).can_validate_asset(asset)
        


validator = OnAssetSaveValidator()
validator.set_editor_property("is_enabled",True)
validate_subsystem = unreal.get_editor_subsystem(unreal.EditorValidatorSubsystem)
validate_subsystem.add_validator(validator)