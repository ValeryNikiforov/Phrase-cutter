#!/bin/bash

export KALDI_ROOT=$HOME/kaldi

export PATH=$PWD/utils:$KALDI_ROOT/src/bin:$KALDI_ROOT/tools/openfst/bin:$KALDI_ROOT/src/fstbin:$KALDI_ROOT/src/gmmbin:$KALDI_ROOT/src/featbin:$KALDI_ROOT/src/lm:$KALDI_ROOT/src/sgmmbin:$KALDI_ROOT/src/sgmm2bin:$KALDI_ROOT/src/fgmmbin:$KALDI_ROOT/src/latbin:$KALDI_ROOT/src/nnetbin:$KALDI_ROOT/src/nnet2bin:$KALDI_ROOT/src/online2bin:$KALDI_ROOT/src/ivectorbin:$KALDI_ROOT/src/lmbin:$KALDI_ROOT/src/chainbin:$KALDI_ROOT/src/nnet3bin:$PWD:$PATH:$KALDI_ROOT/tools/sph2pipe_v2.5
export LC_ALL=C

online2-wav-nnet3-latgen-faster \
      --word-symbol-table=exp/tdnn/graph/words.txt --frame-subsampling-factor=3 --frames-per-chunk=51 \
      --acoustic-scale=1.0 --beam=12.0 --lattice-beam=6.0 --max-active=10000 \
      --config=exp/tdnn/conf/online.conf \
      exp/tdnn/final.mdl exp/tdnn/graph/HCLG.fst ark:decoder-test.utt2spk scp:decoder-test.scp ark:- |
    lattice-lmrescore --lm-scale=-1.0 ark:- 'fstproject --project_output=true data/lang_test_rescore/G.fst |' ark:- |
    lattice-lmrescore-const-arpa ark:- data/lang_test_rescore/G.carpa ark:- |
    lattice-align-words data/lang_test_rescore/phones/word_boundary.int exp/tdnn/final.mdl ark:- ark:- |
    lattice-to-ctm-conf --frame-shift=0.03 --acoustic-scale=0.08333 ark:- - |
    local/int2sym.pl -f 5 data/lang_test_rescore/words.txt - -
