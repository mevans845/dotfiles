cd ~/quip
source settings/vim/quip.vim
map <leader>f :call FindDefinition()<cr>
map <leader>m :Grr <cword><cr>
map <leader><space> :80vsp<cr>

let g:syntastic_javascript_checkers = ['eslint']
let g:syntastic_javascript_eslint_args = '--config=ext/eslint/eslintrc.yml --ignore-path=ext/eslint/eslintignore --rulesdir=ext/eslint/rules --ext=.jsx,.js'
let g:syntastic_python_checkers = ['flake8']
let g:syntastic_python_flake8_post_args='--ignore=F841,F401,E129,E128,E127,E125,N802,N806,E228 --max-line-length=80 --builtins=run,finish,write_task'

