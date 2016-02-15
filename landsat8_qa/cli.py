import json
import os

import click
import rasterio

from .qa import summary_stats


@click.command('l8qa')
@click.argument('qatif')
@click.option('--outdir', '-o', help="output directory", default=None)
def main(qatif, outdir):
    with rasterio.open(qatif) as src:
        arr = src.read(1)
        profile = src.profile

    base = os.path.basename(qatif)
    summary = summary_stats(arr, basename=base, outdir=outdir, profile=profile)
    click.echo(json.dumps(summary, indent=2))

    if outdir:
        click.echo("QA variables written as uint8 tifs to {}".format(outdir),
                   err=True)


if __name__ == "__main__":
    main()
