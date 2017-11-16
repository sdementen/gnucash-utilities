import csv

import click
import piecash


def abort_if_false(ctx, param, value):
    if not value:
        ctx.abort()


@click.group()
def import_export():
    pass


@import_export.command(name="export")
@click.argument("gnucash_file", type=click.Path(exists=True, dir_okay=False))
@click.argument("csv_file", type=click.Path(exists=False, dir_okay=False), default="-")
@click.option("--delimiter", "-d", default=";")
@click.option("--date_format", "-df", default="%d/%m/%Y")
@click.option("--warn-if-locked", is_flag=True)
def export_csv(gnucash_file, csv_file, delimiter, date_format, warn_if_locked):
    with click.open_file(csv_file, mode="w") as file:
        writer = csv.DictWriter(file,
                                fieldnames=["guid",
                                            "post_date",
                                            "description",
                                            "notes",
                                            "from_account",
                                            "to_account",
                                            "value",
                                            "currency",
                                            ],
                                delimiter=delimiter.encode())
        writer.writeheader()
        with piecash.open_book(gnucash_file, open_if_lock=not warn_if_locked) as b:
            for tr in b.transactions:
                tr_dct = dict(guid=tr.guid,
                              post_date=tr.post_date.strftime(date_format),
                              description=tr.description,
                              notes=tr.notes)
                splits = tr.splits
                if len(splits) == 2:
                    sp_from = splits[0 if splits[0].value < 0 else 1]
                    sp_to = splits[1 if splits[0].value < 0 else 0]
                    tr_dct.update(dict(from_account=sp_from.account.fullname,
                                       to_account=sp_to.account.fullname,
                                       value=sp_to.value,
                                       currency=tr.currency.mnemonic))
                writer.writerow(tr_dct)


@import_export.command(name="import")
@click.option('--yes', is_flag=True, callback=abort_if_false,
              expose_value=False,
              prompt='Are you sure you want to import transactions in the GnuCash book?')
def import_csv(uri, delimiter, date_format):
    print("This is a test script")


if __name__ == '__main__':
    import_export()
