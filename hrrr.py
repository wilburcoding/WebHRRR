import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import matplotlib as mpl
import sys
import time
import os
import traceback
from datetime import datetime, timezone, timedelta
from paint.radar2 import cm_reflectivity
from herbie import Herbie
import pytz
from toolbox import EasyMap, pc
from fields import gen_fields
print("\033[32m\033[1mWebHRRR Server\033[0m")
print("\033[90mLoading dependencies...\033[0m")
sys.stdout.write("\033[F")
sys.stdout.write("\033[K")
while True:
    countd = 0
    model = "hrrr"
    est = pytz.timezone('US/Eastern')
    fields = (gen_fields())
    now = datetime.now(timezone.utc)
    latest = (str(now.strftime("%Y-%m-%d %H:00")))

    run = latest
    start = 1
    end = 49 if int(now.hour) % 6 == 0 else 19
    watch = "y"

    hour = start
    l = False
    while (l is False):
        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            lf = latest.replace(" ", ",").replace(":", "-")
            newpath = dir_path + "\\runs\\" + lf
            if not os.path.exists(newpath):
                H = Herbie(latest, model=model, fxx=hour)
                href = H.xarray(":REFC:").longitude
                l = True
            else:
                if (len(os.listdir(newpath + "\\cape")) < (48 if int(now.hour) % 6 == 0 else 18)):
                    l = True
                else:
                    l = False
                    now = now - timedelta(hours=1, minutes=0)
                    latest = (str(now.strftime("%Y-%m-%d %H:00")))
        except:
            l = False
            now = now - timedelta(hours=1, minutes=0)
            latest = (str(now.strftime("%Y-%m-%d %H:00")))
    end = 49 if int(now.hour) % 6 == 0 else 19

    
    for i in range(len(fields)):
        sinfo = fields[i]
        count = 1
        hour = 1
        end = 49 if int(now.hour) % 6 == 0 else 19
        print("Downloading " + str(latest) + " HRRR run (" + sinfo["name"] + ")")
        print("\033[36mDownloading \033[1m[" + str(count) +
              "/" + str(end-start) + "]\033[0m\033[36m...\033[0m")
        while hour < end:
            try:
                H = Herbie(latest, model=model, fxx=hour)
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
                dir_path = os.path.dirname(os.path.realpath(__file__))
                lf = latest.replace(" ", ",").replace(":", "-")
                newpath = dir_path + "\\runs\\" + lf 
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                newpath+="\\"+ sinfo["fname"]
                if not os.path.exists(newpath):
                    os.makedirs(newpath)
                plt.savefig("runs\\" + lf + "\\"+sinfo["fname"] + "\\" + str(hour) + ".png")
                plt.clf()
                count += 1
                for i in range(2):
                    sys.stdout.write("\033[F")
                    sys.stdout.write("\033[K")
                if (count != end-start+1):
                    print("\033[36mDownloading \033[1m[" + str(count) +
                          "/" + str(end-start) + "]\033[0m\033[36m...\033[0m")
                else:
                    print("\033[32mData successfully outputted\033[0m")
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
