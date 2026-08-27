import os, sys, py_compile

files_to_fix = {
    'backend/agents/verifier.py': '\"',
    'backend/agents/drafter.py': 'i',
    'backend/agents/analyzer.py': 'i',
    'backend/agents/graph_lookup.py': '\"',
    'backend/agents/retriever.py': 'f',
    'backend/agents/state.py': 'f',
    'backend/api/chat_router.py': 'i',
    'backend/api/documents.py': '\"',
    'backend/api/user_router.py': 'f',
    'backend/auth/database.py': 'f',
    'backend/auth/jwt_handler.py': 'i',
    'backend/main.py': 'f',
    'backend/rag/pipeline.py': 'i',
    'backend/rag/chroma_store.py': 'i',
    'backend/knowledge/legal_graph.py': '\"',
    'backend/agents/intent_router.py': '\"',
    'backend/utils/language_utils.py': 'i',
    'backend/utils/placeholder_utils.py': 'i',
    'setup.ps1': '['
}

for path, char in files_to_fix.items():
    with open(path, 'rb') as f:
        content = f.read()
    
    content = char.encode('utf-8') + content
    
    with open(path, 'wb') as f:
        f.write(content)

print('All files fixed.')

check_files = list(files_to_fix.keys())
check_files.remove('setup.ps1')
check_files.append('backend/agents/graph.py')

errors = []
for f in check_files:
    try:
        py_compile.compile(f, doraise=True)
    except py_compile.PyCompileError as e:
        errors.append(f)
        print(f'SYNTAX ERROR: {f} -- {e}')

if errors:
    print('Syntax errors remain.')
    sys.exit(1)
print('SYNTAX CHECKS PASSED.')
