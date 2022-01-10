import argparse


def add_arguments(parser: argparse.ArgumentParser):
    """Add subparsers and necessary arguments to the main cli parser

    Args:
        parser (argparse.ArgumentParser): The parser to update
    """
    sub = parser.add_subparsers(help='Operation to execute')

    parser_add_node = sub.add_parser('add_node', help='Add node to blockchain')
    parser_add_node.set_defaults(which='node')
    parser_add_node.add_argument('-p', '--port', default=-1, type=int,
                                 help='Port to listen on')
    parser_add_node.add_argument('-i', '--index', default=-1, type=int,
                                 help='Index of node')
    parser_add_node.add_argument('-c', '--capacity', default=-1, type=int,
                                 help='Blockchain capacity')
    parser_add_node.add_argument('-d', '--difficulty', default=-1, type=int,
                                 help='Blockchain difficulty')
    parser_add_node.add_argument('-n', '--number_nodes', default=-1, type=int,
                                 help='The total number of nodes')

    parser_transaction = sub.add_parser('add_transaction',
                                        help='Add transaction to blockchain')
    parser_transaction.set_defaults(which='transaction')
    parser_transaction.add_argument('-r', '--recipient', default=-1, type=str,
                                 help='Transaction\'s recipient address')
    parser_transaction.add_argument('-s', '--sender', default=-1, type=str,
                                 help='Transaction\'s sender address')
    parser_transaction.add_argument('-a', '--amount', default=-1, type=int,
                                 help='Amount to be sent')

    parser_view = sub.add_parser('view', help='View last transactions\
                                        (transactions of last valid block)')
    parser_view.set_defaults(which='view')
    parser_view.add_argument('-n', '--node', default=-1, type=str,
                                 help='The node\'s address, from which to view\
                                     transactions')

    parser_balance = sub.add_parser('balance', help='Print balance of a\
                                        specific node')
    parser_balance.set_defaults(which='balance')
    parser_balance.add_argument('-n', '--node', default=-1, type=str,
                                 help='The node\'s address, for which to print\
                                     the balance')

    parser_balance = sub.add_parser('broadcast_nodes', help='Broadcast\
                                    bootstrap blockchain and ring node to\
                                    all nodes')
    parser_balance.set_defaults(which='broadcast_nodes')
