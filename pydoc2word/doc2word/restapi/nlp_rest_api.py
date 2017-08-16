# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import make_response
from flask import jsonify

from doc2word import settings, supported_modes

app = Flask(__name__)


@app.route('/api/rest/nlp/extractTags', methods=['GET', 'POST'])
def extract_tags():
    if request.method == 'POST':
        try:
            arg_content = request.form['content']
        except Exception, e:
            try:
                arg_content = request.args['content']
            except Exception, e:
                raise AttributeError('Parameter \'content\' is missing!')
    elif request.method == 'GET':
        try:
            arg_content = request.args['content']
        except Exception, e:
            raise AttributeError('Parameter \'content\' is missing!')

    arg_top_k = int(request.args.get('topK', default=settings.DEFAULT_TOP_K))
    if not request.args.has_key('pos'):
        arg_pos = settings.DEFAULT_ALLOW_POS
    else:
        arg_pos = tuple(request.args['pos'].split(','))

    doc_extractor = supported_modes['local'].doc_extractor(top_k=arg_top_k, allow_pos=arg_pos)
    tags = doc_extractor.extract_tags(content=arg_content)

    return jsonify(
        {
            'code': '0',
            'msg': 'success',
            'result': {
                'tags': [t for t, w in tags],
                'weights': [w for t, w in tags]
            }
        }
    )


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify(
        {
            'code': '1',
            'msg': 'Undefined API.' % error
        }
    ))


@app.errorhandler(500)
def internal_error(error):
    return make_response(jsonify(
        {
            'code': '1',
            'msg': 'Internal error: %s' % error
        }
    ))
