import cloudgenix

class CloudgenixAUX:
    def __init__(self):
        """
        init - use the cgx object that was created by the calling main
        """
        self.cgx = cloudgenix.API()
        self.out = ""

    def setToken(self,token):
        if not self.cgx.interactive.use_token(token):
            ValueError("Invalid Token")
    def getSites(self):
        """
        getSites - returns a list of sites
        """
        res = self.cgx.get.sites()
        if not res:
            raise ValueError("Get get sites", res.cgx_content)
        return res.cgx_content["items"]
    def getObjectList(self,obj):
        """
        getObjectList - returns a list of using the API call for objects
        """
        if obj=="sites":
            res = self.cgx.get.sites()
        elif obj=="elements":
            res = self.cgx.get.elements()
        elif obj=="machines":
            res = self.cgx.get.machines()
        if not res:
            raise ValueError(f"Get get {obj}", res.cgx_content)
        return res.cgx_content["items"]
    def output(self,out):
        """
        add a string to the output
        """
        self.out += str(out) + "\n"
    def getItem(self,object, item):
        """
        Return a dict item
        """
        if item in object and type(object) is dict:
            return object[item]
        else:
            return "ERR"
    def getSiteNameByID(self,site_id):
        for site in self.cgx.get.sites().cgx_content["items"]:
            if site["id"] == site_id:
                return site["name"]
        # stop if wasn't found
        return None
    def getElementByName(self,element_name):
        for element in self.cgx.get.elements().cgx_content["items"]:
            if element["name"] == element_name:
                return element
        # stop if wasn't found
        return None
    def getInterfacesByElementName(self,element_name):
        """
        returns a list of interfaces for an element
        """
        element = self.getElementByName(element_name)
        if not element:
            raise ValueError(f"Can't find {element_name}")

        element_id=element["id"]
        site_id=element["site_id"]
        res = self.cgx.get.interfaces(site_id,element_id)
        if not res:
            raise ValueError(f"Error retrieving interfaces for {element_name}", res.cgx_content)
        return res.cgx_content["items"]
    def getInterfacesByElement(self,element):
        """
        returns a list of interfaces for an element
        """

        element_id=element["id"]
        site_id=element["site_id"]
        res = self.cgx.get.interfaces(site_id,element_id)
        if not res:
            raise ValueError(f"Error retrieving interfaces for {element_name}", res.cgx_content)
        return res.cgx_content["items"]
        

    def getPublicAddressesByElementName(self,element_name):
        element = slef.getElementByName(element_name)
        element_id=element["id"]
        site_id=element["site_id"]