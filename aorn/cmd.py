# -*- coding: utf-8 -*-

'''Commandline module
'''

from __future__ import with_statement, division, absolute_import, print_function

import sys
import importlib
import inspect
import argparse

from aorn.samplesstore import STDIN_FILE, SamplesStore


TEST_AUDIO = 'audio'
TEST_NON_AUDIO = 'non-audio'
CODE_PASS = 0
CODE_FAIL = 1
CODE_ROW = 2
CODE_ERR = 253

CMD_EPILOG = '''
Method has a form of: module.class:param1:param2:...
If more methods at once are selected a simple voting is performed.
Exit codes:
\t{} - selected test passed;
\t{} - selected test failed;
\t{} - selected tests gave a row;
\t{} - other error;
'''.format(CODE_PASS, CODE_FAIL, CODE_ROW, CODE_ERR)
METHODS_SEP = ','
ARGS_SEP = ':'
BUILTIN_METHODS = [
    'aorn.methods.thr',
    'aorn.methods.zcs',
]


class ArgumentParser(argparse.ArgumentParser):
    '''Custom ArgumentParser class
    '''
    def exit(self, status=0, message=None):
        if message:
            self._print_message(message, sys.stderr)
        raise SystemExit(CODE_PASS if status == 0 else CODE_ERR)


def get_options(cmd_args):
    '''Gets options from command line args
    '''
    parser = ArgumentParser(description='Detects audio or non-audio',
        epilog=CMD_EPILOG)
    parser.add_argument('-m', '--methods', dest='methods', required=True,
        help='use method(s) to detect audio/non-audio'
            ' (built-in: {})'.format((METHODS_SEP + ' ').join(BUILTIN_METHODS)))
    parser.add_argument('-f', '--filename', dest='filename',
        help='16-bit PCM (native) samples source (filename or `{}` for STDIN)'
        .format(STDIN_FILE))
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-t', '--test-what', dest='test_what',
        choices=[TEST_AUDIO, TEST_NON_AUDIO], help='detect audio or non-audio')
    group.add_argument('--methods-info', dest='methods_info',
        action='store_true', help='print method(s) usage info')
    return parser.parse_args(args=cmd_args)


def init_test(method, dry_run=False):
    '''Initializes test method class
    '''
    try:
        method_path, method_args = method.split(ARGS_SEP, 1)
    except ValueError:
        method_path = method
        method_args = None
    method_mod, method_cls = method_path.rsplit('.', 1)
    try:
        importlib.import_module(method_mod)
    except ImportError:
        return None
    mod = sys.modules[method_mod]
    try:
        cls = eval(method_cls, mod.__dict__)
        if inspect.isclass(cls):
            args = ()
            kwargs = {'dry_run': dry_run}
            if method_args is not None:
                args = method_args.split(ARGS_SEP)
            return cls(*args, **kwargs)
    except NameError:
        pass
    return None


def cmd_main(cmd_args):
    '''Main method
    '''
    options = get_options(cmd_args)

    samples_store = SamplesStore()
    if not options.methods_info:
        samples_store.load_samples(options.filename)

    votes = {}.fromkeys([TEST_AUDIO, TEST_NON_AUDIO], 0)
    for method in options.methods.split(METHODS_SEP):
        tester = init_test(method, dry_run=bool(options.methods_info))
        if tester is None:
            print('No method for {!r}'.format(method))
            sys.exit(CODE_ERR)
        else:
            if options.methods_info:
                print('Method: {}\n{}'.format(method, tester.get_doc()))
            else:
                tester.analyze(samples_store)
                if tester.is_audio() is True:
                    votes[TEST_AUDIO] += 1
                elif tester.isnt_audio() is True:
                    votes[TEST_NON_AUDIO] += 1

    if not options.methods_info:
        if votes[TEST_AUDIO] == votes[TEST_NON_AUDIO]:
            sys.exit(CODE_ROW)
        if (options.test_what == TEST_AUDIO and
            votes[TEST_AUDIO] > votes[TEST_NON_AUDIO]) or \
            (options.test_what == TEST_NON_AUDIO and
                votes[TEST_NON_AUDIO] > votes[TEST_AUDIO]):
            sys.exit(CODE_PASS)
        else:
            sys.exit(CODE_FAIL)

    sys.exit(CODE_PASS)


def main():
    '''Setuptools' main() function
    '''
    cmd_main(sys.argv[1:])


if __name__ == '__main__':
    main()


# vim: ts=4:sw=4:et:fdm=indent:ff=unix
