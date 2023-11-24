from db import DB
import argparse
    
parser = argparse.ArgumentParser()

def execute(cmd):
    db = DB(dbName='test', outputRaw=False, logFile='cli.log')
    # input('ok')
    db.runCustom(cmd)
    print(db.outputLast)

def select(table, column):
    if column is None:
        column = '*'
    cmd = f'select {column} from {table};'
    execute(cmd)

functions = {
    'select': select
}

global_parser = argparse.ArgumentParser()
subparsers = global_parser.add_subparsers(
    title="commands", help="SQL operations", dest='commands',
    required=True
)

arg_template = {
    # "dest": "keywords",
    "type": str,
    "nargs": 1,
    "metavar": "KEYWORD",
    "help": "a string value",
    # "required": True
}

select_parser = subparsers.add_parser("select", help="query rows from db")
select_parser.add_argument('--table', **arg_template, required=True)
select_parser.add_argument('--column', **arg_template)
select_parser.set_defaults(name='select')

args = global_parser.parse_args()

# handle no --column flag
if args.column is None:
    args.column = [None]

if __name__ == '__main__':
    functions[args.name](*args.table, *args.column if args.column else None)