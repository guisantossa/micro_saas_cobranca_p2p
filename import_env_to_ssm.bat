@echo off
setlocal ENABLEDELAYEDEXPANSION

set PREFIX=/cobraii/prod

for /f "usebackq tokens=1,* delims==" %%A in (".env.prod") do (
    set key=%%A
    set value=%%B
    echo Enviando !key!=!value!

    aws ssm put-parameter ^
        --name "!PREFIX!/!key!" ^
        --value "!value!" ^
        --type "String" ^
        --overwrite ^
        --region us-east-2
)

echo ✅ Finalizado
pause
