from typing import Optional

import ckantoolkit as tk

import ckan.plugins.interfaces as interfaces


class ILollipop(interfaces.Interface):
    def lollipop_set(self):
        """Set the cookie associated with ckanext-lollipop

        :rtype: bool
        """
        return True

    def lollipop_update(self):
        """Update the cookie associated with ckanext-lollipop

        :rtype: bool
        """
        return True

    def lollipop_clear(self):
        """Clear the cookie associated with ckanext-lollipop

        :rtype: bool
        """
        return True

    def lollipop_required(self):
        """Return true if the page requires a CAPTCHA to be completed to access

        :rtype: bool
        """
        return True
    
    def lollipop_process(self, context, data_dict):
        """Process the submitted CAPTCHA form

        :rtype: bool
        """
        return True
