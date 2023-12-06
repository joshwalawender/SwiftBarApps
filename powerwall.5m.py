#!/Users/joshw/anaconda3/envs/py39/bin/python
#
# <xbar.title>Powerwall</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>Josh Walawender</xbar.author>
# <xbar.desc>Show the current status of my Powerwall</xbar.desc>
#
from tesla_powerwall import Powerwall

powerwall = Powerwall(
    endpoint='192.168.4.129',
    timeout=10,
    http_session=None,
    verify_ssl=False,
    disable_insecure_warning=True
)
powerwall.login("d4ee2cg_QLwNjbm6")
assert powerwall.is_authenticated()

powerwallmode = powerwall.get_operation_mode()
meters = powerwall.get_meters()
pwcharge = powerwall.get_charge()
batt_draw = meters.battery.instant_power/1000
print(f"PW:{pwcharge:.0f}% ({-batt_draw:+.1f} kW)")
print('---')
print(f"Battery Charge Level: {pwcharge:6.1f} %")
print(f"Solar Generation:     {meters.solar.instant_power/1000:6.2f} kW")
print(f"Home Power Use:       {meters.load.instant_power/1000:6.2f} kW")
print(f"Drawing from Battery: {batt_draw:+6.2f} kW")
print(f"Drawing from Grid:    {meters.site.instant_power/1000:+6.2f} kW")
print(f"Powerwall Mode:  {powerwallmode.value}")
