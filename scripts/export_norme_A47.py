# coding=utf-8
from __future__ import print_function

import io
import os.path

import click
import jinja2
import sys
from piecash import open_book


@click.group()
def import_export():
    pass


@import_export.command(name="export")
@click.argument("gnucash_file", type=click.Path(exists=True, dir_okay=False))
@click.argument("xml_file", type=click.Path(exists=False, dir_okay=False), default="-")
@click.option("--warn-if-locked", is_flag=True)
def export_norme_A47(gnucash_file, xml_file, warn_if_locked):
    with open_book(gnucash_file, open_if_lock=not warn_if_locked) as book:
        # could add some filtering based on post_date if required
        transactions = book.transactions

        env = jinja2.Environment(trim_blocks=True, lstrip_blocks=True)
        xml = env.from_string(u"""
<?xml version="1.0"?>
<comptabilite>
  <exercice>
    <DateCloture>2016-12-31T00:00:00</DateCloture>
    <journal>
      <JournalCode>Le code du Journal</JournalCode>
      <JournalLib>Le libellé du Journal</JournalLib>
      {% for i, ecriture in enumerate(transactions) %}
      <ecriture>
        <EcritureNum>{{ i }}</EcritureNum>
        <EcritureDate>{{ ecriture.post_date.strftime("%Y-%m-%d") }}</EcritureDate>
        <EcritureLib>{{ ecriture.description }}</EcritureLib>
        <PieceRef>{{ ecriture.num }}</PieceRef>
        <PieceDate>{{ ecriture.post_date.strftime("%Y-%m-%d") }}</PieceDate>
        <ValidDate>{{ ecriture.post_date.strftime("%Y-%m-%d") }}</ValidDate>
        {% for sp in ecriture.splits %}
        <ligne>
          <CompteNum>{{ sp.account.code }}</CompteNum>
          <CompteLib>{{ sp.account.name }}</CompteLib>
          <CompteAuxNum>Le numéro de compte auxiliaire (à blanc si non utilisé)</CompteAuxNum>
          <CompteAuxLib>Le libellé de compte auxiliaire (à blanc si non utilisé)</CompteAuxLib>
          <Montantdevise></Montantdevise>
          <Montant>{{ abs(sp.value) }}</Montant>
          <Sens>{% if sp.value >0 %}c{% else %}d{% endif %}</Sens>
        </ligne>
        {% endfor %}
      </ecriture>
      {% endfor %}
    </journal>
  </exercice>
</comptabilite>
        """).render(transactions=transactions,
                    enumerate=enumerate,
                    abs=abs,
                    )

        if xml_file and xml_file!="-":
            with io.open(xml_file, "w", encoding="utf-8") as f:
                f.write(xml)
        else:
            sys.stdout.write(xml)


if __name__ == '__main__':
    import_export()
