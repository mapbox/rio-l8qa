import json
import os

import click
import rasterio

from .qa import summary_stats, write_cloud_mask


@click.command('l8qa')
@click.argument('qatif')
@click.option('--stats', is_flag=True, default=False)
@click.option('--outdir', '-o', help="output directory", default=None)
@click.option('--cloudmask', '-c', help="output uint8 cloud mask")
def main(qatif, stats, outdir, cloudmask):


    if not stats and not outdir and not cloudmask:
        raise click.UsageError(
            "Specify --stats, --cloudmask MASK, or --outdir DIR")

    if outdir:
        stats = True

    with rasterio.open(qatif) as src:
        arr = src.read(1)
        profile = src.profile

    if cloudmask:
        write_cloud_mask(arr, profile=profile, cloudmask=cloudmask)

    if stats:
        base = os.path.basename(qatif)
        summary = summary_stats(arr, basename=base, outdir=outdir, profile=profile)
        click.echo(json.dumps(summary, indent=2))

        if outdir:
            click.echo("QA variables written as uint8 tifs to {}".format(outdir),
                    err=True)


if __name__ == "__main__":
    main()
