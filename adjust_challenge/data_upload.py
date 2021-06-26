import sys, os
from pathlib import Path
from datetime import datetime
import django
import requests

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(BASE_DIR)

os.environ['DJANGO_SETTINGS_MODULE'] = 'adjust_challenge.settings'
django.setup()

from cpi.models import ADCampaigns

DATASET_URL = 'https://gist.githubusercontent.com/kotik/3baa5f53997cce85cc0336cb1256ba8b/raw' \
              '/3c2a590b9fb3e9c415a99e56df3ddad5812b292f/dataset.csv'


def get_data(url: str):
    resp = requests.get(url)
    print(url)
    data = resp.text.splitlines()
    for row in data[1:]:
        row = row.split(',')
        try:
            _ = ADCampaigns(
                date=datetime.strptime(row[0], '%Y-%m-%d').date(),
                channel=row[1],
                country=row[2],
                os=row[3],
                impressions=int(row[4]),
                clicks=int(row[5]),
                installs=int(row[6]),
                spend=float(row[7]),
                revenue=float(row[8]),
            )
            _.save()
        except Exception as e:
            print(row)
            continue

    print(ADCampaigns.objects.all())



if __name__ == '__main__':
    get_data(DATASET_URL)
