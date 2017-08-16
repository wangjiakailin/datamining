# -*- coding: utf-8 -*-

import sys
import doc2word

from doc2word import settings, analyse, supported_modes as modes
from doc2word.restapi import nlp_rest_api
from doc2word.analyse import idf_generator
from doc2word.debug import Debug
from argparse import ArgumentParser

supported_modes = sorted(modes.keys())


def __handle_pos(pos):
    if pos == '0':
        return ()
    elif isinstance(pos, str):
        return tuple([p.strip() for p in pos.split(',')])
    else:
        return pos


def __handle_gen_idf_path(gen_idf_path):
    return [p.strip() for p in gen_idf_path.split(',')]


parser = ArgumentParser(usage='%s -m doc2word [options]' % sys.executable,
                        description='doc2word command line interface. version %s' % (settings.VERSION, ))
parser.add_argument('-M', '--mode', default=settings.DEFAULT_MODE,
                    choices=tuple(supported_modes),
                    help='Affects the underlying runtime system. currently supported modes: %s'
                         % ','.join(supported_modes))
parser.add_argument('-n', '--num-latest-days', dest='num_latest_days', type=int,
                    default=settings.DEFAULT_NUM_LATEST_DAYS,
                    help='Number of day folders. Files in these folders will be extracted.')
parser.add_argument('-d', '--directory', default=settings.DEFAULT_ROOT,
                    help='Root directory.')
parser.add_argument('-k', '--top-k', dest='top_k', default=settings.DEFAULT_TOP_K, type=int,
                    help='use TOP_K instead of default [%d] as the number of tags to be extracted'
                         % settings.DEFAULT_TOP_K)
parser.add_argument('-a', '--allow-pos', dest='allow_pos', default=settings.DEFAULT_ALLOW_POS,
                    help='''POS sequence, comma [,] separated. eg. n,nr,ns,v,vn;
                    It can be disabled by passing parameter 0. eg. -a 0''')
parser.add_argument('-D', '--debug', action='store_true', default=False,
                    help='Debug information.')
parser.add_argument("-S", '--server', action='store_true', default=False,
                    help='Run the RESTFul API service.')
parser.add_argument('-P', '--port', default=settings.DEFAULT_REST_API_APP_PORT, type=int,
                    help='Port of the RESTFul API service. eg. 18080')
parser.add_argument('-G', '--gen-idf', dest='gen_idf', default=None,
                    help='generate idf dict, root path list, comma [,] separated.')

args = parser.parse_args()

try:
    Debug.debug(debug_flag=args.debug)
except:
    pass

server = args.server
port = args.port
gen_idf = args.gen_idf

analyse.use_default_analyse_settings()

if server:
    nlp_rest_api.app.run(host='0.0.0.0', port=port)
elif gen_idf:
    gen_idf_root_path_list = __handle_gen_idf_path(gen_idf)
    idf_generator.train_idf(gen_idf_root_path_list)
else:
    mode = args.mode
    num_latest_days = args.num_latest_days
    root_path = args.directory
    top_k = args.top_k
    allow_pos = __handle_pos(args.allow_pos)

    doc2word.doc2word(mode=mode, num_latest_days=num_latest_days, root_path=root_path,
                      top_k=top_k, allow_pos=allow_pos)
