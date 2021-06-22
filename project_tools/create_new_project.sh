if [ -z "$1" ];then
    echo "Usage: bash create_new_project.sh <project_name>"
    exit
fi

git clone git@github.com:kellyxiepei/django_bootstrap.git

PROJECT_NAME=$(echo $1 | tr '[A-Z]' '[a-z]')
mv django_bootstrap $PROJECT_NAME
mv "$PROJECT_NAME/django_bootstrap" "$PROJECT_NAME/$PROJECT_NAME"

rm -rf "./$PROJECT_NAME/.git"

SED=$(command -v gsed)
if test -z "$SED";then
    SED=sed
fi

$SED -i "" "s/django_bootstrap/$PROJECT_NAME/g" `find $PROJECT_NAME -type f`