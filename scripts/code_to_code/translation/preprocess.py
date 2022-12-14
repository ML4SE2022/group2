from parser.utils import (remove_comments_and_docstrings,
                   tree_to_token_index,
                   index_to_code_token,
                   tree_to_variable_index)
from tree_sitter import Language, Parser

parsers={}        
for lang in ['java', 'csharp']:
    if lang == 'csharp':
        lang = 'c_sharp'
    LANGUAGE = Language('parser/my-languages.so', lang)
    parser = Parser()
    parser.set_language(LANGUAGE)

def flatten_ast(root_node, index_to_code, tokenizer):
    root_node_index = root_node.start_point, root_node.end_point
    # prune to closest child
    if len(root_node.children) == 1:
        root_node = prune_single(root_node)
    if len(root_node.children) == 0:
        if root_node_index in index_to_code:
            return ' '.join(tokenizer.tokenize(index_to_code[root_node_index])) + ' '
        else:
            return '<' + root_node.type + ',left> ' + '<' + root_node.type + ',right> '
    else:
        # indentify the parent nodes
        code_tokens = '<' + root_node.type + ',left> '
        for child in root_node.children:
            code_tokens += flatten_ast(child,index_to_code,tokenizer)
        code_tokens += '<' + root_node.type + ',right> '
        return code_tokens

def prune_single(root_node):
    if len(root_node.children) == 1:
        return prune_single(root_node.children[0])
    else:
        return root_node
    
def extract_ast(code, lang, tokenizer):
    #remove comments
    try:
        code=remove_comments_and_docstrings(code,lang)
    except:
        pass
    tree = parser.parse(bytes(code,'utf8'))    
    root_node = tree.root_node  
    tokens_index=tree_to_token_index(root_node)
    code=code.split('\n')
    code_tokens=[index_to_code_token(x,code) for x in tokens_index]
    index_to_code={}
    for idx,(index,c) in enumerate(zip(tokens_index,code_tokens)):
        index_to_code[index]=c
    
    code_tokens = flatten_ast(root_node, index_to_code, tokenizer)
    return code_tokens
