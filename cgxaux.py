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
    def getInterfacePublicIPAddress(self,element,interface):
        # check if element is valid and has interfaces
        site_id = element["site_id"]
        element_id = element["id"]
        # check if the interface is a Internet interface
        if interface["used_for"] in ["public","lan"]:
            # check if pppoe
            if interface["type"] == "pppoe":
                interface_type="dynamic"
            elif not interface["ipv4_config"]:
                # the interface isn't configured we shell skip it
                return "NOT CONFIGURED"
            # check if we have a static ip address
            elif interface["ipv4_config"]["type"] == "static":
                #its a static address
                interface_ip = interface["ipv4_config"]["static_config"]["address"]
                interface_type="static"
            else:
                # its a DHCP address
                interface_type="dynamic"

            # resolve dynamic address
            if interface_type == "dynamic":
                # get interface status
                interface_status = self.cgx.get.interfaces_status(site_id,element_id,interface["id"]).cgx_content
                # if the interface is a bypass pair, we need to look at one which is not a bypass
                if "items" in interface_status:
                    if "bypass" in interface_status["items"][0]["name"]:
                        interface_status = interface_status["items"][1]
                    else:
                        interface_status = interface_status["items"][0]
                if interface_status["operational_state"] == "down":
                    interface_ip = "DOWN"
                else:
                    #check for ipv4 address
                    if interface_status["ipv4_addresses"]:
                        interface_ip = interface_status["ipv4_addresses"][0]
                    elif interface_status["ipv6_addresses"]:
                        interface_ip = interface_status["ipv6_addresses"][0]

            #check if NAT is configured
            if interface["nat_address"]:
                NAT = interface["nat_address"]
            else:
                NAT= None
            if NAT:
                return NAT
            else:
                if not interface_ip:
                    return "NOT CONFIGURED"
                else:
                    return interface_ip
        else:
            return "INVALID INTERFACE TYPE"

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
