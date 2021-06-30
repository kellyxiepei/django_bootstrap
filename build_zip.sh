TIMESTAMP=`date +%s`
DIRNAME="/Users/xiewangyi/Downloads/django_bootstrap_$TIMESTAMP"
cp -R . $DIRNAME

SITE_PACKAGES_DIR=`python -c 'import site; print(site.getsitepackages()[0])'`

cp -R $SITE_PACKAGES_DIR $DIRNAME

cd $DIRNAME
zip -q -r $DIRNAME.zip *

rm -rf $DIRNAME