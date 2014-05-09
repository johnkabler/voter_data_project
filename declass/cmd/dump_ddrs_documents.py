"""
Dump the DDRS Documents to flat files.
"""
import argparse
import declass.ddrs as ddrs

def _cli():
    parser = argparse.ArgumentParser(
        description=globals()['__doc__'],
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        '-o', '--outdir', required=True,
        help='Directory to write formatted files.')

    parser.add_argument(
        '-i', '--indir', required=False,
        help='Directory to read formatted files.')

    parser.add_argument(
        '-s', '--source', required=True,
        help='Source to get the documents from either {db, file}.')

    parser.add_argument(
        '-l', '--limit', type=int,
        help='Only retrieve LIMIT number of documents')

    parser.add_argument(
        '--output_spec', required=True,
        help="""Specifies the format to write out the files.
            clean -> Remove all the formatting.
            nofoot -> Remove all the formatting and footers.
            raw -> Original text with markup.""")
    args = parser.parse_args()

    dbCon = ddrs.make_db_connect()
    if args.source == "db":
        query = "SELECT id, body FROM Document"
        if args.limit:
            query += " LIMIT %d" % args.limit
        rows = dbCon.run_query(query)
        documents = (ddrs.Document(row["id"], row["body"])
                     for row in rows)
    elif args.source == "file":
        documents = ddrs.Document.fetch_from_files(args.indir)
        
    ddrs.Document.write_to_files(args.outdir, documents, args.output_spec)


if __name__ == '__main__':
    _cli()


