import pyblish.api


class ValidateRigContents(pyblish.api.InstancePlugin):
    """Ensure rig has the appropriate object sets"""

    order = pyblish.api.ValidatorOrder
    families = ["rig"]

    def process(self, instance):
        assert "controls_SEL" in instance, "%s is missing a controls set" % instance
        assert "pointcache_SEL" in instance, "%s is missing a pointcache set" % instance
