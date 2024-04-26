__all__ = ['NOAAs3']


class NOAAs3:
    def __init__(self, bucket='noaa-goes16', workdir='.'):
        """
        Create a NOAA s3 navigation object.

        Arguments
        ---------
        bucket : str
            Usually noaa-goes16 (GOES-East), noaa-goes17 (GOES-West), or
            noaa-goes18 (GOES-West current)
        workdir : str
            Root path for downloading files to.

        Example Usage
        -------------

        from goesutils import NOAAs3
        import pandas as pd

        nav = NOAAs3('noaa-goes16')
        dates = pd.date_range('2023-09-21 12', '2023-09-21 18', freq='h')
        remotekeys = nav.findfiles('ABI-L2-AODC', dates)
        print(len(remotekeys))
        # 84
        print(remotekeys[0])
        # ABI-L2-AODC/2023/264/12/OR_ABI-L2-AODC-M6_G16_s20232641201172_e20232641203545_c20232641205547.nc
        print(remotekeys[1])
        # ABI-L2-AODC/2023/264/12/OR_ABI-L2-AODC-M6_G16_s20232641206172_e20232641208545_c20232641211006.nc

        Example of Notebook Graphical User Interface
        --------------------------------------------

        # In[0]
        from noaas3 import NOAAs3
        # In[1]
        nav = NOAAs3('noaa-goes16')
        nav.form
        # In[2]
        nav.findfiles_from_form()
        """
        import boto3
        from botocore import UNSIGNED
        from botocore.config import Config

        cfg = Config(signature_version=UNSIGNED)
        self.s3 = s3 = boto3.resource('s3', config=cfg)
        self.bucket = s3.Bucket(bucket)
        self.workdir = workdir

    def get_shortnames(self):
        """
        Find all short names available from bucket (e.g., ABI-L2-AODC)
        Short names are defined in more detail at
        https://docs.opendata.aws/noaa-goes16/cics-readme.html

        Returns
        -------
        Prefix : list
            List of Prefixes (including traling /)
        """
        result = self.bucket.meta.client.list_objects_v2(
            Bucket=self.bucket.name, Delimiter='/'
        )
        return [r['Prefix'] for r in result.get('CommonPrefixes')]

    def findfiles(self, short_name, dates):
        """
        Arguments
        ---------
        short_name : str
            One of the items in get_shortnames
        dates : iterable
            List or other iterable of date objects that support strftime

        Returns
        -------
        remotekeys : list
            List of remote keys that can be retrieved from S3 bucket.
        """
        import pandas as pd

        if short_name.endswith('/'):
            short_name = short_name[:-1]

        remotekeys = []
        dates = pd.to_datetime(dates)
        for date in dates:
            prefix = f'{short_name}/{date:%Y/%j/%H}/'
            bfiles = self.bucket.objects.filter(Prefix=prefix, Delimiter='/')
            inpaths = sorted([b.key for b in bfiles])
            remotekeys.extend(inpaths)
        return remotekeys

    def getfiles(
        self, remotekeys=None, short_name=None, dates=None, workdir=None
    ):
        """
        Arguments
        ---------
        remotekeys : list or None
            List of keys from findfiles to download.
        short_name : str or None
        dates : list or None
            If remotekeys is None, then use short_name and dates with findfiles
            to get remotekeys
        workdir : str
            Working root directory for downloading files. Defaults to
            self.workdir

        Returns
        -------
        localpaths : list
            List of local paths where remotekeys have been stored
        """
        import os

        if workdir is None:
            workdir = self.workdir

        localpaths = []
        if remotekeys is None:
            remotekeys = self.findfiles(short_name=short_name, dates=dates)

        for remotekey in remotekeys:
            print(remotekey)
            localpath = f'{workdir}/s3.{self.bucket.name}/{remotekey}'
            os.makedirs(os.path.dirname(localpath), exist_ok=True)
            if not os.path.exists(localpath):
                self.bucket.download_file(remotekey, localpath)
            localpaths.append(localpath)

        return localpaths

    @property
    def form(self):
        """
        ipywidgets form object for Graphical User Interface
        """
        import pandas as pd
        if not hasattr(self, '_form'):
            from ipywidgets import Layout, Box, Dropdown, Label, DatePicker
            from datetime import date

            form_item_layout = Layout(
                display='flex', flex_flow='row',
                justify_content='space-between'
            )

            prodd = Dropdown(
                options=[k[:-1] for k in self.get_shortnames()],
                description='Product'
            )
            prodd.value = 'ABI-L2-AODC'
            startd = date.today() - pd.to_timedelta('7d')
            datesa = DatePicker(description='Start Date', value=startd)
            hrs = list(range(0, 24))
            hoursa = Dropdown(options=hrs, description='Start Hour')
            hoursa.value = 17
            dateea = DatePicker(value=startd, description='End Date')
            hourea = Dropdown(options=hrs, description='End Hour')
            hourea.value = 17
            form = Box([
                Box([Label(value='GOES Options')], layout=form_item_layout),
                Box([prodd], layout=form_item_layout),
                Box([datesa, dateea], layout=form_item_layout),
                Box([hoursa, hourea], layout=form_item_layout),
            ], layout=Layout(
                display='flex', flex_flow='column', border='solid 2px',
                align_items='stretch', width='50%'
            ))
            self._form = form

        return self._form

    def findfiles_from_form(self):
        """
        Same as findfiles, but arguments are taken from the form object
        """
        import pandas as pd

        children = self.form.children
        short_name = children[1].children[0].value
        startd = children[2].children[0].value
        endd = children[2].children[1].value
        starth = children[3].children[0].value
        endh = children[3].children[1].value
        dates = pd.date_range(
            pd.to_datetime(startd) + pd.to_timedelta(starth, unit='h'),
            pd.to_datetime(endd) + pd.to_timedelta(endh, unit='h'),
            freq='h'
        )
        return self.findfiles(short_name, dates)

    def getfiles_from_form(self):
        """
        Same as getfiles, but arguments are taken from the form object
        """
        return self.getfiles(remotekeys=self.findfiles_from_form)
