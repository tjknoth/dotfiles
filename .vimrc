" Core
filetype indent plugin on
syntax on
set encoding=utf-8
set fileformat=unix

" Buffers & History
set hidden
set history=1000
set undofile
set undodir=~/.vim/undo//
if !isdirectory(expand('~/.vim/undo'))
  call mkdir(expand('~/.vim/undo'), 'p', 0700)
endif

" UI
set number relativenumber
set cursorline
set ruler
set laststatus=2
set showcmd
set showmode
set nowrap
set scrolloff=5
set signcolumn=yes
set colorcolumn=80

" Search
set hlsearch
set incsearch
set ignorecase smartcase

" Indentation
set autoindent
set expandtab
set tabstop=2 shiftwidth=2 softtabstop=2

" Editing behavior
set backspace=indent,eol,start
set nostartofline
set textwidth=80
set mouse=a
set updatetime=300
set notimeout ttimeout ttimeoutlen=200

" Completion
set wildmenu
set wildmode=longest,list,full
set wildignore+=*.swp,*.swo,*.zip,.git
set completeopt=menuone,longest

" Splits
set splitbelow splitright

" Clipboard (use 'unnamed' for macOS, 'unnamedplus' for Linux)
set clipboard=unnamed

" Prompt to save instead of failing
set confirm

" Leader
let mapleader=" "

" Mappings
map Y y$
nnoremap <C-L> :nohl<CR><C-L>

" Quick save
nnoremap <leader>w :w<CR>

" Split navigation
nnoremap <C-h> <C-w>h
nnoremap <C-j> <C-w>j
nnoremap <C-k> <C-w>k
nnoremap <C-l> <C-w>l

" Buffer navigation
nnoremap <leader>bn :bnext<CR>
nnoremap <leader>bp :bprevious<CR>
nnoremap <leader>bd :bdelete<CR>
