import piecash
import sys

from piecash_utilities.report import report, execute_report


@report(
    title="My simplest report with a book",
    name="piecash-simple-report-book",
    menu_tip="A simple report that opens a book",
    options_default_section="general",
)
def generate_report(
        book_url,
):
    with piecash.open_book(book_url, readonly=True, open_if_lock=True) as book:
        return """<html>
        <body>
            Hello world from python !<br>
            Book : {book_url}<br>
            List of accounts : {accounts}
        </body>
        </html>""".format(
            book_url=book_url,
            accounts=[acc.fullname for acc in book.accounts],
        )


if __name__ == '__main__':
    execute_report(generate_report, book_url=sys.argv[1])
