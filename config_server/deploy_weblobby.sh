#!/bin/bash

BASEDIR=/usr/local/pythonenv/weblobby

mkdir -p /root/repositorio/
cd /root/repositorio/
rm -rf weblobbyproject
svn export http://svn.exemplo.com/weblobby/trunk/weblobbyproject

# Exclui arquivos atuais
rm -rf $BASEDIR/weblobbyproject
# Copia os novos
cp -rf weblobbyproject $BASEDIR/weblobbyproject

# Ajustas permissões
chown -R root:www-data /usr/local/pythonenv/weblobby/
chmod -R g+w /usr/local/pythonenv/weblobby/

/etc/init.d/apache2 reload
