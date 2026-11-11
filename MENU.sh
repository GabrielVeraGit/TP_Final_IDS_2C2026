#!/bin/bash
func_menu(){
    echo "Crear Entornos Virtuales e Instalar dependencias ------- 1  (API & APLICATIVO)"
    echo "Crear .env e ingresar las variables de entorno --------- 2  (API & APLICATIVO)"
    echo "Crear Estructura_General de la DB MySQL ---------------- 3  (API)"
    echo "ELIMINAR Estructura de la DB MySQL --------------------- 4  (API)"
    echo "Lanzar API & APLICATIVO -------------------------------- 5  "
    echo "Salir -------------------------------------------------- 0"
}

instalar_dependencias(){
    
    ./API_BACKEND/.venv/bin/python3 -m ensurepip --default-pip #reparar/instalar pip de forma local si por alguna razón no se creó al armar el entorno virtual
    ./API_BACKEND/.venv/bin/python3 -m pip install --upgrade pip #actualiza a la última versión disponible de pip

    ./APLICATIVO_FRONTEND/.venv/bin/python3 -m ensurepip --default-pip
    ./APLICATIVO_FRONTEND/.venv/bin/python3 -m pip install --upgrade pip

    #instalar las dependencias del proyecto
    if [[ (-f "./API_BACKEND/requirements.txt") && (-f "./APLICATIVO_FRONTEND/requirements.txt") ]]; then
        echo -n "Instalando dependencias... "
        ./API_BACKEND/.venv/bin/python3 -m pip install -r ./API_BACKEND/requirements.txt
        ./APLICATIVO_FRONTEND/.venv/bin/python3 -m pip install -r ./APLICATIVO_FRONTEND/requirements.txt
        echo "dependencias EXITO!"
    else
        echo "Alerta: No se encontró los archivos requirements.txt"
        rm -rf ./API_BACKEND/.venv
        rm -rf ./APLICATIVO_FRONTEND/.venv
    fi
}
crear_entorno_virtual(){
    if [[ ! -d "./API_BACKEND/.venv" && ! -d "./APLICATIVO_FRONTEND/.venv" ]]; then
        echo -n "Creando ENTORNOS VIRTUALES... "
        python3 -m venv ./API_BACKEND/.venv
        python3 -m venv ./APLICATIVO_FRONTEND/.venv
        echo "venv's EXITO!"
        
        instalar_dependencias

    else
        echo "Ya fueron creados"
    fi
}

crear_ingresar_env(){
    password_incorrecta="si"
    email_incorrecto="si"
    if [[ -f "./API_BACKEND/.env" && -f "./APLICATIVO_FRONTEND/.env" ]];then
        echo "Ya existen"
    else
        echo "Inicializando las variables .env de la Base de Datos"

        read -p "[default=root] DB_USER=" db_user
        if [[ -z "${db_user}" ]]; then
            db_user="root"
        fi

        while [[ "${password_incorrecta}" == "si" ]];do
            read -s -p "DB_PASSWORD=" db_password
            echo ""
            if [[ -n "${db_password}" ]]; then
                password_incorrecta="no"
            fi
        done

        # Expresión regular estándar y compatible con Bash para validar emails
        regex_email="^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        while [[ "${email_incorrecto}" == "si" ]];do
            read -p "EMAIL_REMITENTE=" email
            if [[ "$email" =~ $regex_email ]]; then
                email_incorrecto="no"
            else
                echo "El email NO es válido"
            fi
        done
 
        regex_password="^[a-z]{16}$"
        password_incorrecta="si"
        while [[ "${password_incorrecta}" == "si" ]];do
            read -p "EMAIL_REMITENTE=" pass_remitente
            if [[ "$pass_remitente" =~ $regex_password ]]; then
                password_incorrecta="no"
            else
                echo "La contraseña NO es válida. Debe tener 16 letras minúsculas y sin espacios."
            fi
        done
        cp ./.env.example ./API_BACKEND/.env
        sed -i "s/DB_USER=tu_usuario_aqui/DB_USER=${db_user}/" ./API_BACKEND/.env
        sed -i "s/DB_PASSWORD=tu_contrasenia_aqui/DB_PASSWORD=${db_password}/" ./API_BACKEND/.env
        sed -i "s/EMAIL_REMITENTE=tu_email_aqui/EMAIL_REMITENTE=${email}/" ./API_BACKEND/.env
        sed -i "s/PASSWORD_REMITENTE=codigo_16_caracteres/PASSWORD_REMITENTE=${pass_remitente}/" ./API_BACKEND/.env

        grep "PORT_APLICATIVO_FRONTEND" ./.env.example >> ./APLICATIVO_FRONTEND/.env
        echo "EXITO!"

    fi

}

crear_estructura_db(){
    if [[ -f "./API_BACKEND/.env" && $(source ./API_BACKEND/.env; echo "$DB_ESTRUCTURA_CREADA") == "false" ]];then
        echo -n "CREANDO la estructura de la base de datos..."

        salida=$(
            source ./API_BACKEND/.env
            export MYSQL_PWD="${DB_PASSWORD}"
            mysql -h "${DB_HOST}" -u "${DB_USER}" < ./API_BACKEND/db/init_db.sql
            salida=$?
            unset MYSQL_PWD
            echo $salida
        )
        if [[ ${salida} -eq 0 ]];then
            sed -i "s/DB_ESTRUCTURA_CREADA=false/DB_ESTRUCTURA_CREADA=true/" ./API_BACKEND/.env
            echo "EXITO!"
        else
            echo "ERROR! Revise si el motor db MySQL esta corriendo, o su Usuario/Password es correcto. Salida: ${salida}"
        fi

    else
        echo "Archivo ./API_BACKEND/.env no existe o la estructura DB ya fue creada"
    fi
}

eliminar_estructura_db(){
    if [[ -f "./API_BACKEND/.env" && $(source ./API_BACKEND/.env; echo "$DB_ESTRUCTURA_CREADA") == "true" ]];then
        read -p "¿Desea eliminarla la estructura DB? (si/no): " borrar
        if [[ "${borrar,,}" == "si" ]]; then
            echo -n "ELIMINANDO la estructura de la base de datos..."
            salida=$(
                source ./API_BACKEND/.env
                export MYSQL_PWD="${DB_PASSWORD}"
                mysql -h "${DB_HOST}" -u "${DB_USER}" -e "DROP DATABASE IF EXISTS ${DB_NAME};"
                salida=$?
                unset MYSQL_PWD
                echo $salida
            )

            if [[ ${salida} -eq 0 ]];then
                sed -i "s/DB_ESTRUCTURA_CREADA=true/DB_ESTRUCTURA_CREADA=false/" ./API_BACKEND/.env
                echo "EXITO!"
            else
                echo "ERROR! Revise si el motor db MySQL esta corriendo, o su Usuario/Password es correcto. Salida: ${salida}"
            fi
        fi
    else
        echo "Archivo ./API_BACKEND/.env no existe o la estructura DB NO EXISTE."
    fi
}


comprobar_api_aplicativo(){

    if [[ -d "./API_BACKEND/.venv" && -f "./API_BACKEND/.env" && -d "./APLICATIVO_FRONTEND/.venv" ]];then

        db_estructura_creada=$(source ./API_BACKEND/.env; echo "$DB_ESTRUCTURA_CREADA")
        db_vivo=$(
                source ./API_BACKEND/.env
                export MYSQL_PWD="${DB_PASSWORD}"
                mysqladmin -h "${DB_HOST}" -u "${DB_USER}" ping &>/dev/null
                salida=$?
                unset MYSQL_PWD
                echo $salida
                )
        if [[ "${db_estructura_creada}" == "true" && "${db_vivo}" -eq 0 ]]; then
            lanzar_web="si"
        else
            echo "La estructura del DB, no fue creada o conexion perdida con el motor"
        fi
    else
        echo "ERROR! procure haber hecho las anteriores opciones (1, 2 y 3)"
    fi
}

lanzar_api_aplicativo(){

    echo "Iniciando..."

    ./API_BACKEND/.venv/bin/python3 ./API_BACKEND/app.py & 
    PID_API=$!

    ./APLICATIVO_FRONTEND/.venv/bin/python3 ./APLICATIVO_FRONTEND/app.py & 
    PID_APLICATIVO=$!

    echo "Mostrando informacionen tiempo real (Presiona Ctrl+C para detener ambos)..."
    
    #si presiona ctrl+c ejecutamos "comandos" 
    trap "kill $PID_API $PID_APLICATIVO 2>/dev/null; echo -e '\nServidores detenidos.'; return" INT
   
    wait -n $PID_API $PID_APLICATIVO #-n espera hasta q uno se detenga
    
    kill $PID_API $PID_APLICATIVO 2>/dev/null
    
    trap - INT


}

script_menu_continua="si"
while [[ ${script_menu_continua} == "si" ]];do
    func_menu
    echo ""
    read -p "Ingrese una op -> " opcion
    case "$opcion" in
        "1")
            crear_entorno_virtual
            ;;
        "2")
            crear_ingresar_env
            ;;
        "3")
            crear_estructura_db
            ;;
        "4")
            eliminar_estructura_db
            ;;
        "5")
            lanzar_web="no"
            comprobar_api_aplicativo
            if [[ ${lanzar_web} == "si" ]];then
                lanzar_api_aplicativo
            fi

            ;;
        "0")
            script_menu_continua="no"
            ;;
        *)
            echo "OP no valida"
            ;;
    esac
    sleep 0.4
    read -p "   press to continue .."
    clear
done


#source .venv/bin/activate
