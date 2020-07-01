import refinitiv.dataplatform as rdp

APP_KEY = ''
RDP_LOGIN = ''
RDP_PASSWORD = ''

session = rdp.open_platform_session(
    APP_KEY, 
    rdp.GrantPassword(
        username = RDP_LOGIN, 
        password = RDP_PASSWORD
    )
)