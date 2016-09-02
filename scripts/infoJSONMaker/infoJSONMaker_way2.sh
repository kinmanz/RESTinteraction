#!/bin/bash
#Author: Luchko Serega

#Эта задача только на Bash
#плюс в том что не требует Логин и Пароль
#для запуска вставить в Command Line Runner in TeamCity
#Перед использованием надо загрузить файл с JSON под
#главную папку проекта, поля под замену помечать
#как _VERSION_, _DATE_ и тд.

#если не хотите создавать JSON файл то достаточно будет
#создать строку с default JSON.
#скрипт простой, легко понять и изменять.

#download default JSON from file
json_string=$(<fileName.info.json)
echo "$json_string"

#get fields
VERSION=%major_version%.%patch_version%
DATE=`date +%%Y-%%m-%%d:%%H:%%M:%%S`
VCS_BRANCH=%project_branch_tag%
BUILD_NUMBER=%build.number%

#debug info
echo BUILD_NUMBER: $BUILD_NUMBER
echo VERSION: $VERSION
echo DATE: $DATE
echo VCS_BRANCH: ${VCS_BRANCH#*heads/}

#set fields
result_string=$json_string
result_string=${result_string//_DATE_/$DATE};
result_string=${result_string//_VERSION_/$VERSION};
result_string=${result_string//_VCS_BRANCH_/${VCS_BRANCH#*heads/}};
result_string=${result_string//_BUILD_NUMBER_/$BUILD_NUMBER};

#write to file
echo "$result_string" > "User_Part/fileName.info.json"

#debug info
json_string=$(<User_Part/fileName.info.json)
echo "$json_string"

