#!/usr/bin/env sh
# Modified from illustration2vec's get_models.sh
# This scripts downloads the pre-trained models.

DIR="$( cd "$(dirname "$0")" ; pwd -P )"
cd $DIR

echo "Downloading pre-trained models..."
wget http://illustration2vec.net/models/tag_list.json.gz -O data/i2v_tag_list.json.gz
wget http://illustration2vec.net/models/illust2vec_tag_ver200.caffemodel -O data/data/i2v_model.caffemodel
gunzip data/i2v_tag_list.json.gz

echo "Done."
