# Import CloudGenix SDK
#import cloudgenix
import json

# this translate json to python. Easier to copy paste from json results
true = True
false = False
null = None


# get site information and find the site ID that belongs to the site name
cgx = None

def initmyCGX(cgx_object):
    global cgx
    cgx = cgx_object

def getSiteID(site_name):

    sites = cgx.get.sites()
    if not sites.cgx_status:
        print(sites.response)
        raise RuntimeError("API call error")

    # locate the and extract the site ID
    sites = sites.cgx_content['items']
    site_id = "nada"
    for site in sites:
        if site["name"] == site_name:
            site_id = site["id"]
            break

    # stop if site wasn't found
    if site_id=="nada":
        raise ValueError("Site %s not found" % (site_name))
    else:
        return site_id


def getMachineID(device_serial):
    machines = cgx.get.machines()
    if not machines.cgx_status:
        print(machines.response)
        raise RuntimeError("API call error")

    machines = machines.cgx_content['items']

    device_id="nada"
    for device in machines:
        if device["sl_no"]== device_serial:
            device_id = device["id"]
            break

    if device_id=="nada":
        raise ValueError("Machine SN: %s not found" % device_serial)
    else:
        return device_id


def getElementIDbyMachineID(device_id):
    machines = cgx.get.machines(machine_id=device_id)
    if not machines.cgx_status:
        print(machines.response)
        raise ValueError("Can't find element for device %s" % device_id )
    return machines.cgx_content["em_element_id"]



def getInterfaces(site,e_id):
    interfaces = cgx.get.interfaces(site,e_id)
    if not interfaces.cgx_status:
        print(interfaces.response)
        raise ValueError("Can't retrieve interfaces for %s %s" % (site,e_id))
    return interfaces.cgx_content["items"]


def getInterfaceByName(site,element,ifName):
    interfaces = getInterfaces(site,element)
    int_json = None
    for interface in interfaces:
        if interface["name"] == ifName:
            int_json = interface
            break

    # stop if wan wasn't found
    return int_json

def getSiteNameByID(site_id):
    int_json = None
    for site in cgx.get.sites().cgx_content["items"]:
        if site["id"] == ifName:
            int_json = interface
            break

    # stop if wan wasn't found
    return int_json

def getLanNetworkByPrefix(site,prefix):
    lans = cgx.get.lannetworks(site)
    if not lans.cgx_status:
        print(lans.response)
        raise ValueError("Can't retrieve LAN networks for %s" % (site))
    lan_json = None
    for lan in lans.cgx_content["items"]:
        if lan["ipv4_config"]["default_routers"] == [prefix]:
            lan_json = lan
            break
    return lan_json

def getIPSecProfileByName(name):
    ipsecprofiles = cgx.get.ipsecprofiles()
    if not ipsecprofiles.cgx_status:
        print(ipsecprofiles.cgx_content)
        raise ValueError("Can't retrieve IPSec profiles")
    ipsec_json = None
    for ipsec in ipsecprofiles.cgx_content["items"]:
        if ipsec["name"] == name:
            ipsec_json = ipsec
            break
    return ipsec_json

def getServiceEndpointByName(name):
    serviceendpoints = cgx.get.serviceendpoints()
    if not serviceendpoints.cgx_status:
        print(serviceendpoints.cgx_content)
        raise ValueError("Can't retrieve service endpoints")
    sep_json = None
    for sep in serviceendpoints.cgx_content["items"]:
        if sep["name"] == name:
            sep_json = sep
            break
    return sep_json

def getWanNetworkIDByNameAndType(wanType,wanName):
    wannetworks = cgx.get.wannetworks()
    if not wannetworks.cgx_status:
        print(wannetworks.response)
        raise ValueError("Can't retrieve wannetworks " )
    wannetworks= wannetworks.cgx_content["items"]
    wan_id = "nada"
    for wan in wannetworks:
        if wan["name"] == wanName and wanType in wan["type"]:
            wan_id = wan["id"]
            break

    # stop if wan wasn't found
    if wan_id=="nada":
        raise ValueError("wan %s - %s not found" % (wanType, wanName))
    else:
        return wan_id


def getWanInterfaceLabelIDByNameAndType(wanType,wanName):
    wanlabels = cgx.get.waninterfacelabels()
    if not wanlabels.cgx_status:
        print(wanlabels.response)
        raise ValueError("Can't retrieve wanlabels " )
    wanlabels= wanlabels.cgx_content["items"]
    wan_id = "nada"
    for wan in wanlabels:
        if wan["name"] == wanName and wanType in wan["label"]:
            wan_id = wan["id"]
            break

    # stop if wan wasn't found
    if wan_id=="nada":
        raise ValueError("wan %s - %s not found" % (wanType, wanName))
    else:
        return wan_id



def getWanInterfaceIDByNetworkLabel(site_id,wanNetwork,wanLabel):
    wanInterfaces = cgx.get.waninterfaces(site_id)
    if not wanInterfaces.cgx_status:
        print(wanInterfaces.response)
        raise ValueError("Can't retrieve waninterfaces " )
    wanInterfaces= wanInterfaces.cgx_content["items"]
    wan_id = "nada"
    for wan in wanInterfaces:
        if wan["label_id"] == wanLabel and wan["network_id"] == wanNetwork:
            wan_id = wan["id"]
            break

    # stop if wan wasn't found
    if wan_id=="nada":
        raise ValueError("wan %s -  %s not found" % (wanNetwork, wanLabel))
    else:
        return wan_id


def getPolicySetByName(policyName):
    policysets = cgx.get.policysets()
    if not policysets.cgx_status:
        print(policysets.response)
        raise ValueError("Can't retrieve policysets" )
    policysets= policysets.cgx_content["items"]
    policy_id = "nada"
    for policy in policysets:
        if policy["name"] == policyName:
            policy_id = policy["id"]
            break
    # stop if wan wasn't found
    if policy_id=="nada":
        raise ValueError("policy %s not found" % (policyName))
    else:
        return policy_id

def getSecurityPolicySetByName(securitypolicyName):
    securitypolicysets = cgx.get.securitypolicysets()
    if not securitypolicysets.cgx_status:
        print(securitypolicysets.response)
        raise ValueError("Can't retrieve securitypolicysets" )
    securitypolicysets= securitypolicysets.cgx_content["items"]
    securitypolicy_id = "nada"
    for securitypolicy in securitypolicysets:
        if securitypolicy["name"] == securitypolicyName:
            securitypolicy_id = securitypolicy["id"]
            break
    # stop if wan wasn't found
    if securitypolicy_id=="nada":
        raise ValueError("securitypolicy %s not found" % (securitypolicyName))
    else:
        return securitypolicy_id

def getImageByName(imageName):
    images = cgx.get.element_images()
    if not images.cgx_status:
        raise ValueError("Can't retrieve images: %s",images.cgx_content )
    images= images.cgx_content["items"]
    image_id = "nada"
    for image in images:
        if image["version"] == imageName:
            image_id = image["id"]
            break
    # stop if wan wasn't found
    if image_id=="nada":
        raise ValueError("image %s not found" % (imageName))
    else:
        return image_id
def getImageNameByID(imageID):
    images = cgx.get.element_images()
    if not images.cgx_status:
        raise ValueError("Can't retrieve images: %s",images.cgx_content )
    images= images.cgx_content["items"]
    image_name = "nada"
    for image in images:
        if image["id"] == imageID:
            image_name = image["version"]
            break
    # stop if wan wasn't found
    if image_name=="nada":
        raise ValueError("image %s not found" % (imageID))
    else:
        return image_name
def getContextByName(contextName):
    contexts = cgx.get.networkcontexts()
    if not contexts.cgx_status:
        raise ValueError("Can't retrieve contexts: %s",contexts.cgx_content )
    contexts= contexts.cgx_content["items"]
    context_id = "nada"
    for context in contexts:
        if context["name"] == contextName:
            context_id = context["id"]
            break
    # stop if wan wasn't found
    if context_id=="nada":
        raise ValueError("context %s not found" % (contextName))
    else:
        return context_id


def getSecurityZonesIDsDict():
    zones = cgx.get.securityzones()
    if not zones.cgx_status:
        raise ValueError("Can't get security zones",zones.cgx_content )
    zones= zones.cgx_content["items"]
    zonesdict={}
    for zone in zones:
        zonesdict[zone["name"]] = zone["id"]
    return zonesdict

def getOverlayID():
    overlays = cgx.get.wanoverlays()
    if not overlays.cgx_status:
        raise ValueError("Can't retrieve overlays:",overlays.cgx_content )
    overlays= overlays.cgx_content["items"]
    overlay_id = "nada"
    for overlay in overlays:
        if overlay["name"] == "zbfw_overlay":
            overlay_id = overlay["id"]
            break
    # stop if wan wasn't found
    if overlay_id=="nada":
        raise ValueError("overlay %s not found" % ("zbfw_overlay"))
    else:
        return overlay_id

def isMachineClaimed(device_id):
    machines = cgx.get.machines(machine_id=device_id)
    if not machines.cgx_status:
        raise ValueError("Cant fetch machine",device_id)
    device = machines.cgx_content
    # if the device is claimed keep it element_id and move on to the next step
    return device["machine_state"] == "claimed"

def getWanInterface(site_id,wannetwork_id,interfacelabel_id):
    res = cgx.get.waninterfaces(site_id)
    if not res:
        raise ValueError ("Can't get WAN interface list",site_id)
    waninterface_json=None
    for waninterface in res.cgx_content["items"]:
        if waninterface["network_id"]==wannetwork_id and waninterface["label_id"] == interfacelabel_id:
            waninterface_json=waninterface
            break
    return waninterface_json



def getStaticRouteByPrefix(site_id,element_id,prefix):
    routes = cgx.get.staticroutes(site_id,element_id)
    if not routes:
        raise ValueError ("Can't fetch static routes for site %s for element %s",site_id,element_id)
    route_json=None
    for route in routes.cgx_content["items"]:
        if route["destination_prefix"]==prefix:
            route_json = route
            break
    return route_json
def getTrapByHost(site_id,element_id,host):
    traps = cgx.get.snmptraps(site_id,element_id)
    if not traps:
        raise ValueError ("Can't fetch snmp traps for site %s for element %s",site_id,element_id)
    trap_json=None
    for trap in traps.cgx_content["items"]:
        if trap["server_ip"]==host:
            trap_json = trap
            break
    return trap_json
def getZoneBindByZoneID(site_id,zone_id):
    zones = cgx.get.sitesecurityzones(site_id)
    if not zones:
        raise ValueError ("Can't fetch sitesecurity zones for site %s ",site_id)
    zone_json=None
    for zone in zones.cgx_content["items"]:
        if zone["zone_id"]==zone_id:
            zone_json = zone
            break
    return zone_json

def getNTP(element_id):
    ntp = cgx.get.ntp(element_id)
    if not ntp:
        raise ValueError ("Can't fetch NTP for element %s",element_id)
    return ntp.cgx_content["items"][0]
def getNATByName(site_id,element_id,name):
    extensions = cgx.get.element_extensions(site_id,element_id)
    if not extensions:
        raise ValueError ("Can't fetch site extensions for site and element ",site_id, element_id)
    extension_json=None
    for extension in extensions.cgx_content["items"]:
        if extension["name"]==name and extension["namespace"]=="natpolicy/interface":
            extension_json = extension
            break
    return extension_json

def getNetflowByName(site_id,element_id,name):
    extensions = cgx.get.element_extensions(site_id,element_id)
    if not extensions:
        raise ValueError ("Can't fetch site extensions for site and element ",site_id, element_id)
    extension_json=None
    for extension in extensions.cgx_content["items"]:
        if extension["name"]==name and extension["namespace"]=="netflowv5/interface":
            extension_json = extension
            break
    return extension_json
