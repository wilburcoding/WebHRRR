import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys
import time
import os
import traceback
from datetime import datetime, timezone
from paint.radar2 import cm_reflectivity
from datetime import datetime
from herbie import Herbie
import pytz
from toolbox import EasyMap, pc
from fields import gen_fields
print("\033[32m\033[1mWebHRRR Server\033[0m")
print("\033[90mLoading dependencies...\033[0m")
sys.stdout.write("\033[F")
sys.stdout.write("\033[K")
model = "hrrr"
est = pytz.timezone('US/Eastern')
fields = (gen_fields())
now = datetime.now(timezone.utc)
print(str(now.strftime("%Y-%m-%d %H:00")))
sys.exit(1)
run = input("Runtime (YYYY-MM-DD HH:00): ")
start = int(input("Start hour: "))
end = int(input("End hour: "))
watch = input("Watch Mode (y/n): ")
for i in range(4):
    sys.stdout.write("\033[F")
    sys.stdout.write("\033[K")
for i in range(len(fields)):
    print(fields[i]["name"] + " [" + str(i + 1) + "]")
field = int(input("Enter a field: "))
sinfo = fields[field-1]
count = 1
print("\033[36mDownloading \033[1m[" + str(count) +
      "/" + str(end-start) + "]\033[0m\033[36m...\033[0m")
hour = start

while hour < end:
    try:
        H = Herbie(run, model=model, fxx=hour)
        href = H.xarray(sinfo["xa"])
        ax = EasyMap("50m", crs=href.herbie.crs, dark=True,
                     figsize=[10, 8]).STATES().ax
        vmin = 0.1
        norm = mpl.colors.Normalize(vmin=vmin, vmax=80)
        p = ax.pcolormesh(
            href.longitude,
            href.latitude,
            getattr(href, sinfo["fname"]),
            transform=pc,
            cmap=sinfo["cmap"],
            **sinfo["cmp"]
        )
        plt.colorbar(
            p,
            ax=ax,
            orientation="vertical",
            pad=0.01,
            shrink=0.8
        )

        ti = str(href.valid_time.dt.strftime("%Y-%m-%dT%H:%M:%S").item())
        valid = datetime.strptime(ti, "%Y-%m-%dT%H:%M:%S")
        valid = pytz.utc.localize(valid)
        ax.set_title(
            f"{href.model.upper()}: {getattr(href, sinfo["fname"])  .GRIB_name}\nValid: {valid.astimezone(est).strftime('%I:%M %p EST - %d %b %Y')}",
            loc="left",
        )
        ax.set_title(
            f"Hour: {str(hour)}\nInit: " + href.time.dt.strftime('%Hz - %d %b %Y').item(), loc="right")
        ax.set_extent([-74.5, -71.5, 40, 42])
        plt.tight_layout()
        plt.savefig("output/" + str(hour) + ".png")
        plt.clf()
        count += 1
        for i in range(2):
            sys.stdout.write("\033[F")
            sys.stdout.write("\033[K")
        if (count != end-start+1):
            print("\033[36mDownloading \033[1m[" + str(count) +
                  "/" + str(end-start) + "]\033[0m\033[36m...\033[0m")
        else:
            print("\033[32mData successfully outputted to ./output\033[0m")
        hour += 1
    except Exception as e:
        print(traceback.format_exc())
        if (watch == "y"):
            print(
                "\033[31mData failed to fetch, trying again in 60 seconds \033[0m")
            for i in range(60):
                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
                print(
                    "\033[31mData failed to fetch, trying again in " + str(60-i) + " seconds \033[0m")
                time.sleep(1)
            for i in range(2):

                sys.stdout.write("\033[F")
                sys.stdout.write("\033[K")
        else:
            print(
                "\033[31mAn error occured when downloading the data, the data is likely not available\033[0m")
            sys.exit(1)
